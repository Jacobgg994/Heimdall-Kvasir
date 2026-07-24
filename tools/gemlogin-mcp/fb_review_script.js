async function run() {
    const fs = require('fs');
    const path = require('path');

    // โครงสร้าง parameter ที่ส่งเข้ามาจาก UI
    const config = {
        geminiApiKey: typeof gemini_api_key !== 'undefined' ? gemini_api_key : '',
        pagesFilePath: typeof fb_pages_file !== 'undefined' ? fb_pages_file : '',
        instructions: typeof review_instructions !== 'undefined' ? review_instructions : 'เขียนรีวิวเชิงบวก ให้ข้อมูลน่าสนใจและสุภาพ',
        temp: parseFloat(typeof temperature !== 'undefined' ? temperature : '0.8') || 0.8
    };

    console.log("[INIT] เริ่มต้นสคริปต์รีวิวเพจ Facebook ด้วย AI Gemini");
    console.log(`[CONFIG] หน้าเพจจากไฟล์: ${config.pagesFilePath}`);

    if (!config.pagesFilePath || !fs.existsSync(config.pagesFilePath)) {
        throw new Error(`ไม่พบไฟล์รายชื่อเพจตามพาธที่กำหนด: ${config.pagesFilePath}`);
    }

    if (!config.geminiApiKey) {
        throw new Error("กรุณาระบุ Gemini API Key ใน Parameters");
    }

    // ฟังก์ชันในการจองเพจแบบปลอดภัย (Concurrency-safe check & lock)
    // เพื่อหลีกเลี่ยงการหยิบเพจซ้ำเมื่อรันหลายโปรไฟล์พร้อมกัน
    const lockFilePath = config.pagesFilePath + '.lock';
    const doneFilePath = config.pagesFilePath + '.done';

    // รอคิวเพื่อเข้าเช็คไฟล์แบบ concurrency-safe (Simple Mutex)
    async function acquireLock(retries = 30) {
        for (let i = 0; i < retries; i++) {
            try {
                // ถ้าไม่มี lock file ให้เขียนสร้าง
                if (!fs.existsSync(lockFilePath)) {
                    fs.writeFileSync(lockFilePath, 'locked', 'utf8');
                    return true;
                }
            } catch (e) {
                // เกิดข้อผิดพลาดในการเขียน หรือไฟล์โดนสร้างไปก่อนหน้าแล้ว
            }
            await page.waitForTimeout(500 + Math.random() * 500); // รอแบบสุ่ม 0.5 - 1 วินาที
        }
        return false;
    }

    function releaseLock() {
        try {
            if (fs.existsSync(lockFilePath)) {
                fs.unlinkSync(lockFilePath);
            }
        } catch (e) {
            console.error("[LOCK] ไม่สามารถปลดล็อคไฟล์ได้:", e.message);
        }
    }

    let targetPage = '';
    const hasLock = await acquireLock();
    if (!hasLock) {
        throw new Error("ไม่สามารถทำการจองคิวการรันได้เนื่องจากติดการใช้งานไฟล์โดยโปรไฟล์อื่นอยู่");
    }

    try {
        const pages = fs.readFileSync(config.pagesFilePath, 'utf8')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line !== "");

        let donePages = [];
        if (fs.existsSync(doneFilePath)) {
            donePages = fs.readFileSync(doneFilePath, 'utf8')
                .split('\n')
                .map(line => line.trim())
                .filter(line => line !== "");
        }

        // ค้นหาเพจที่ยังไม่เคยรีวิว
        for (const p of pages) {
            if (!donePages.includes(p)) {
                targetPage = p;
                // บันทึกการล็อคจองทันทีเพื่อไม่ให้คนอื่นมาเคลมซ้ำ
                fs.appendFileSync(doneFilePath, targetPage + '\n', 'utf8');
                break;
            }
        }
    } finally {
        releaseLock();
    }

    if (!targetPage) {
        console.log("[COMPLETED] ไม่มีเพจใหม่ให้รีวิวแล้ว สิ้นสุดการทำงาน");
        return;
    }

    console.log(`[CLAIMED] ทำการเลือกเพจ: ${targetPage}`);

    // ดึงชื่อเพจหรือปรับ URL ให้เป็น Reviews URL
    let reviewUrl = targetPage;
    if (!reviewUrl.startsWith('http://') && !reviewUrl.startsWith('https://')) {
        reviewUrl = 'https://www.facebook.com/' + reviewUrl;
    }
    
    // จัดการ URL ให้เข้าสู่หน้า /reviews
    if (reviewUrl.includes('profile.php')) {
        reviewUrl = reviewUrl + '&sk=reviews';
    } else {
        reviewUrl = reviewUrl.replace(/\/$/, '') + '/reviews';
    }

    console.log(`[NAVIGATION] เปิดหน้าเพจ: ${reviewUrl}`);
    await page.goto(reviewUrl, { waitUntil: 'networkidle2', timeout: 60000 });

    // ตรวจสอบภาษาของปุ่มหรือเช็คการมีอยู่
    const selectors = {
        recommendBtn: '//div[@role="button"]//span[text()="Yes" or text()="ใช่" or text()="แนะนำ" or text()="Recommend" or contains(text(), "ใช่")]',
        textBox: '//textarea | //div[@contenteditable="true"]',
        postBtn: '//div[@aria-label="Post" or @aria-label="โพสต์" or @aria-label="แชร์" or @aria-label="Share" or @role="button"]//span[text()="Post" or text()="โพสต์" or text()="Share" or text()="แชร์"]'
    };

    console.log("[WAIT] รอตรวจพบปุ่มแนะนำ...");
    let recommendBtnEl = null;
    try {
        await page.waitForXPath(selectors.recommendBtn, { visible: true, timeout: 15000 });
        const els = await page.$x(selectors.recommendBtn);
        if (els && els.length > 0) recommendBtnEl = els[0];
    } catch (e) {
        console.log("[WARN] ไม่พบปุ่ม Yes/ใช่ แนะนำแบบทั่วไป กำลังทดสอบซีเลคเตอร์ทางเลือก...");
    }

    if (!recommendBtnEl) {
        // ลองหาปุ่ม Yes/ใช่ แบบไม่เจาะจง
        const fallbackEls = await page.$x('//span[text()="Yes" or text()="ใช่"]');
        if (fallbackEls && fallbackEls.length > 0) {
            recommendBtnEl = fallbackEls[0];
        }
    }

    if (!recommendBtnEl) {
        throw new Error("ไม่พบปุ่มสำหรับให้คำแนะนำเพจนี้ (คุณอาจจะเคยรีวิวไปแล้ว หรือเพจไม่ได้เปิดระบบรับรีวิว)");
    }

    // คลิกปุ่มเพื่อแนะนำเพจ
    console.log("[ACTION] คลิกปุ่มแนะเพจ...");
    await recommendBtnEl.click();
    await page.waitForTimeout(3000);

    // เรียก Gemini API สร้างรีวิวที่ไม่ซ้ำกัน
    console.log("[AI] เรียกใช้งาน Gemini AI เพื่อสร้างข้อความรีวิว...");
    
    // ตั้ง Prompt ให้ Gemini สร้างรีวิว
    const promptText = `คุณเป็นลูกค้าจริงๆ เขียนรีวิวแนะนำให้ร้านค้า/ธุรกิจนี้เป็นภาษาไทยที่สุภาพเป็นธรรมชาติที่สุด ไม่สแปม ไม่พูดเหมือนสคริปต์
รายละเอียดของเพจนี้/ธุรกิจนี้: "${targetPage}"
คำสั่งเพิ่มเติม/ข้อมูลบริการ: "${config.instructions}"
เงื่อนไขสำคัญ:
1. เขียนข้อความรีวิว 1 ย่อหน้าความยาวประมาณ 50 - 100 คำ (ต้องมีความยาวรวมมากกว่า 30 ตัวอักษรขึ้นไป)
2. เขียนให้น่าอ่าน ลื่นไหล ไม่ซ้ำกับใคร และเป็นภาษาธรรมชาติ
3. ห้ามพิมพ์เครื่องหมายคำพูดคลุมข้อความผลลัพธ์ นำเสนอเฉพาะข้อความที่จะใช้โพสต์รีวิวเท่านั้น`;

    let reviewContent = "";
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${config.geminiApiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: promptText
                    }]
                }],
                generationConfig: {
                    temperature: config.temp
                }
            })
        });

        if (!response.ok) {
            const errBody = await response.text();
            throw new Error(`Gemini API Error: Status ${response.status} - ${errBody}`);
        }

        const data = await response.json();
        if (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts[0]) {
            reviewContent = data.candidates[0].content.parts[0].text.trim();
        } else {
            throw new Error("Gemini API ส่งค่ากลับมาไม่สมบูรณ์");
        }
    } catch (apiErr) {
        console.error("[AI ERROR] ไม่สามารถสร้างเนื้อหาด้วย Gemini ได้:", apiErr.message);
        // Fallback ในกรณีที่ API พัง
        reviewContent = "บริการดีมากครับ ประทับใจการใส่ใจลูกค้าและการตอบแชทที่รวดเร็ว แนะนำเลยครับสำหรับใครที่หาบริการด้านนี้อยู่";
    }

    console.log(`[AI RESULT] รีวิวที่จะนำไปลง:\n"${reviewContent}"`);

    // กรอกรีวิวลงในช่อง
    console.log("[WAIT] รอช่องพิมพ์ข้อความแสดงตัว...");
    await page.waitForXPath(selectors.textBox, { visible: true, timeout: 15000 });
    const [textBoxEl] = await page.$x(selectors.textBox);
    
    if (!textBoxEl) {
        throw new Error("ไม่สามารถระบุช่องสำหรับพิมพ์รีวิวได้");
    }

    await textBoxEl.click({ clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.waitForTimeout(500);

    // ทยอยพิมพ์ทีละตัวให้ดูเป็นธรรมชาติ
    await textBoxEl.type(reviewContent, { delay: 40 });
    await page.waitForTimeout(3000);

    // คลิกปุ่มโพสต์รีวิว
    console.log("[ACTION] รอและคลิกปุ่มแชร์รีวิว (Post/Share)...");
    const [postBtnEl] = await page.$x(selectors.postBtn);
    if (postBtnEl) {
        await postBtnEl.click();
        console.log("[SUCCESS] คลิกปุ่มโพสต์เรียบร้อย");
    } else {
        // ลองซีเลคเตอร์ fallback สำหรับปุ่มโพสต์
        const fallbackPostBtn = await page.$x('//div[@role="button" and (contains(., "Post") or contains(., "โพสต์") or contains(., "Share") or contains(., "แชร์"))]');
        if (fallbackPostBtn && fallbackPostBtn.length > 0) {
            await fallbackPostBtn[0].click();
            console.log("[SUCCESS] คลิกปุ่มโพสต์ด้วยซีเลคเตอร์สำรองเรียบร้อย");
        } else {
            console.warn("[WARN] ไม่พบปุ่มแชร์/โพสต์อัตโนมัติ กรุณาตรวจสอบหรือดำเนินการแบบแมนนวลต่อ");
        }
    }

    // หน่วงเวลาเพื่อเสร็จสิ้นกระบวนการโพสต์
    await page.waitForTimeout(8000);
    console.log(`[COMPLETED] รีวิวเพจ ${targetPage} เรียบร้อยแล้ว!`);
}
run();

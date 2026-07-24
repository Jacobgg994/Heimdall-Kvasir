async function run() {
    const config = {
        videoDir: video_source_path,
        captionsFile: captions_file_path,
        hashtagsFile: hashtags_file_path,
        postLimit: parseInt(number_param_4) || 1,
        isRandom: is_random_mode_,
        selectors: {
            fileInput: 'input[type="file"]',
            descriptionField: '//div[@contenteditable="true"]',
            postButton: '//button[div[text()="Post"]] | //button[contains(., "Post")]'
        }
    };
    console.log(`[INIT] Preparing to post ${config.postLimit} videos...`);
    const fs = require('fs');
    const path = require('path');
    const getLines = (filePath) => {
        if (!filePath || !fs.existsSync(filePath)) return [];
        return fs.readFileSync(filePath, 'utf8').split('\n').map(l => l.trim()).filter(l => l !== "");
    };
    const captions = getLines(config.captionsFile);
    const hashtags = getLines(config.hashtagsFile);
    let videos = fs.readdirSync(config.videoDir).filter(f => /\.(mp4|mov|webm)$/i.test(f));
    if (videos.length === 0) throw new Error("ERROR: No video files found in directory.");
    for (let i = 0; i < config.postLimit; i++) {
        if (videos.length === 0) break;
        console.log(`[STEP ${i + 1}/${config.postLimit}] Starting new upload...`);
        try {
            const idx = config.isRandom ? Math.floor(Math.random() * videos.length) : 0;
            const videoName = videos.splice(idx, 1)[0];
            const videoPath = path.join(config.videoDir, videoName);
            if (!page.url().includes('tiktok.com/upload')) {
                await page.goto('https://www.tiktok.com/upload?lang=en', { waitUntil: 'networkidle2', timeout: 60000 });
            }
            await page.waitForSelector(config.selectors.fileInput, { timeout: 30000 });
            const inputHandle = await page.$(config.selectors.fileInput);
            await inputHandle.uploadFile(videoPath);
            await page.waitForXPath(config.selectors.descriptionField, { timeout: 60000 });
            const [descField] = await page.$x(config.selectors.descriptionField);
            await descField.click({ clickCount: 3 });
            await page.keyboard.press('Backspace');
            const caption = captions.length > 0 ? captions[Math.floor(Math.random() * captions.length)] : "";
            const hashtag = hashtags.length > 0 ? hashtags[Math.floor(Math.random() * hashtags.length)] : "";
            const text = `${caption} ${hashtag}`.trim();
            if (text) {
                await descField.type(text, { delay: 50 });
            }
            await page.waitForTimeout(5000);
            await page.waitForXPath(config.selectors.postButton, { visible: true });
            const [postBtn] = await page.$x(config.selectors.postButton);
            await page.waitForFunction((el) => !el.disabled, { timeout: 60000 }, postBtn);
            await postBtn.click();
            console.log(`[SUCCESS] Posted: ${videoName}`);
            if (i < config.postLimit - 1) {
                await page.waitForTimeout(15000);
                await page.goto('https://www.tiktok.com/upload?lang=en');
            }
        } catch (err) {
            console.error(`[FAILED] Error at video #${i + 1}: ${err.message}`);
            await page.goto('https://www.tiktok.com/upload?lang=en').catch(() => {});
        }
    }
    console.log(`[COMPLETED] Successfully processed the session.`);
}
run();
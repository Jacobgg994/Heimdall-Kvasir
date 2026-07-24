async function run() {
    const config = {
        targets: typeof target_urls === 'string' ? target_urls.split('\n').filter(l => l.trim()) : [],
        minWatch: parseInt(min_watch_sec) || 60,
        maxWatch: parseInt(max_watch_sec) || 120,
        interactionChance: parseInt(interaction_rate) || 20,
        searchMode: search_mode,
        selectors: {
            consentAccept: '//button[@aria-label="Accept all"] | //button[contains(., "Accept")]',
            searchBar: 'input#search',
            videoTitle: '#video-title',
            likeBtn: 'button[aria-label^="like this video"]',
            subBtn: 'ytd-subscribe-button-renderer button'
        }
    };

    console.log(`[INIT] Starting YouTube Booster with ${config.targets.length} targets.`);

    for (const target of config.targets) {
        try {
            console.log(`[PROCESS] Target: ${target}`);
            
            if (config.searchMode) {
                await page.goto('https://www.youtube.com/', { waitUntil: 'networkidle2' });
                // Handle consent
                const [accept] = await page.$x(config.selectors.consentAccept);
                if (accept) await accept.click();

                await page.waitForSelector(config.selectors.searchBar);
                await page.type(config.selectors.searchBar, target);
                await page.keyboard.press('Enter');
                await page.waitForNavigation({ waitUntil: 'networkidle2' });
                
                // Click first video result
                await page.waitForSelector(config.selectors.videoTitle);
                await page.click(config.selectors.videoTitle);
            } else {
                const url = target.startsWith('http') ? target : `https://www.youtube.com/results?search_query=${encodeURIComponent(target)}`;
                await page.goto(url, { waitUntil: 'networkidle2' });
                if (url.includes('results?')) {
                    await page.waitForSelector(config.selectors.videoTitle);
                    await page.click(config.selectors.videoTitle);
                }
            }

            // Watch
            const watchTime = Math.floor(Math.random() * (config.maxWatch - config.minWatch + 1) + config.minWatch);
            console.log(`[WATCHING] duration: ${watchTime}s`);
            
            // Random scrolling during watch
            const scrollInterval = setInterval(async () => {
                await page.evaluate(() => window.scrollBy(0, Math.random() * 300));
            }, 15000);

            await page.waitForTimeout(watchTime * 1000);
            clearInterval(scrollInterval);

            // Random Interaction
            if (Math.random() * 100 < config.interactionChance) {
                console.log(`[ACTION] Attempting Like/Sub...`);
                try {
                    const like = await page.$(config.selectors.likeBtn);
                    if (like) await like.click();
                    await page.waitForTimeout(2000);
                    const sub = await page.$(config.selectors.subBtn);
                    if (sub) await sub.click();
                } catch (e) {}
            }

            console.log(`[SUCCESS] Completed target: ${target}`);

        } catch (err) {
            console.error(`[ERROR] Failed target ${target}: ${err.message}`);
        }
    }
    console.log(`[FINISHED] Session complete.`);
}
run();
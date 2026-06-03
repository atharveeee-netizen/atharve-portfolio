const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser for screenshot...");
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 900 });
        
        console.log("Navigating to http://localhost:5173/...");
        await page.goto('http://localhost:5173/', { waitUntil: 'networkidle0', timeout: 30000 });
        
        console.log("Scrolling to USP section...");
        await page.evaluate(() => {
            const el = document.querySelector('.section_cta-cards');
            if (el) {
                el.scrollIntoView();
                // Scroll a bit more to trigger GSAP scroll trigger
                window.scrollBy(0, 300);
            }
        });
        
        console.log("Waiting for animations to complete...");
        await new Promise(resolve => setTimeout(resolve, 4000));
        
        const savePath = 'C:\\Users\\noobg\\.gemini\\antigravity\\brain\\5ba9ce6d-5fff-42c1-8e5b-34f1727bf606\\live_screenshot.png';
        await page.screenshot({ path: savePath });
        console.log(`Screenshot saved successfully to ${savePath}`);
        
        await browser.close();
    } catch (err) {
        console.error("Screenshot error:", err);
    }
})();

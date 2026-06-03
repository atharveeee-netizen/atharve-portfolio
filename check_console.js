const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();
        
        page.on('console', msg => {
            console.log(`[BROWSER LOG] ${msg.type().toUpperCase()}: ${msg.text()}`);
        });
        
        page.on('pageerror', error => {
            console.log(`[BROWSER ERROR]: ${error.stack || error.message}`);
        });

        page.on('requestfailed', request => {
            console.log(`[REQUEST FAILED]: ${request.url()} - ${request.failure().errorText}`);
        });

        console.log("Navigating to localhost:5173...");
        await page.goto('http://localhost:5173/', { waitUntil: 'domcontentloaded', timeout: 30000 });
        
        console.log("Waiting 3 seconds to let animations run...");
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        await browser.close();
        console.log("Done checking console.");
    } catch (err) {
        console.error("Puppeteer Script Error:", err);
    }
})();

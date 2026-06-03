const puppeteer = require('puppeteer');

const pages = [
  'http://localhost:5173/',
  'http://localhost:5173/about.html',
  'http://localhost:5173/how-it-works.html',
  'http://localhost:5173/projects.html',
  'http://localhost:5173/contact.html'
];

(async () => {
    let hasError = false;
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();
        
        page.on('console', msg => {
            if (msg.type() === 'error') {
                console.log(`[BROWSER ERROR LOG] ${msg.text()}`);
                hasError = true;
            } else {
                console.log(`[BROWSER LOG] ${msg.type().toUpperCase()}: ${msg.text()}`);
            }
        });
        
        page.on('pageerror', error => {
            console.log(`[BROWSER EXCEPTION]: ${error.stack || error.message}`);
            hasError = true;
        });
 
        page.on('requestfailed', request => {
            console.log(`[REQUEST FAILED]: ${request.url()} - ${request.failure().errorText}`);
            hasError = true;
        });

        for (const url of pages) {
            console.log(`\nNavigating to ${url}...`);
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            console.log("Waiting 2 seconds to let animations run...");
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
        
        await browser.close();
        console.log("\nDone checking all pages.");
        if (hasError) {
            console.log("Verdict: Site has console errors!");
        } else {
            console.log("Verdict: Site is 100% clean of errors!");
        }
    } catch (err) {
        console.error("Puppeteer Script Error:", err);
    }
})();

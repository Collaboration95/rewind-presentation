// Records 3 s of a data: URL with Playwright's built-in video recorder at 1920x1080 (writes only under /tmp/rewind-video/in).
import { chromium } from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, recordVideo: { dir: '/tmp/rewind-video/in/pw', size: { width: 1920, height: 1080 } } });
const p = await ctx.newPage();
await p.goto('data:text/html,<body style="font:64px Arial;background:%23fff"><h1>Playwright recording test</h1><div id=c></div><script>let n=0;setInterval(()=>c.textContent=++n,100)</script>');
await p.waitForTimeout(3000);
await ctx.close(); await b.close();
console.log('done');

/* Measure only. Loads each payload in the composition, reports beats whose
   lines wrapped past their own breaks, encodes nothing. Answers "which of
   the reels already out there have this" without a 40 minute re-render. */
import { readFileSync, readdirSync } from 'fs';
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { createServer } from 'http';
import { extname, join } from 'path';

const MIME = { '.html':'text/html', '.css':'text/css', '.jpg':'image/jpeg',
  '.jpeg':'image/jpeg', '.png':'image/png', '.webp':'image/webp',
  '.mp4':'video/mp4', '.webm':'video/webm', '.woff2':'font/woff2' };
const DIR = process.argv[2] || '.';
const srv = createServer((req,res) => {
  const f = join(DIR, decodeURIComponent(req.url.split('?')[0]));
  let body;
  try { body = readFileSync(f); }
  catch { res.writeHead(404); res.end(); return; }
  res.writeHead(200,{'Content-Type':MIME[extname(f).toLowerCase()]||'application/octet-stream'});
  res.end(body);
});
await new Promise(r => srv.listen(0, r));
const ORIGIN = `http://127.0.0.1:${srv.address().port}`;
const browser = await chromium.launch();

const files = readdirSync(DIR).filter(n => n.endsWith('.json')
  && !['package.json','package-lock.json'].includes(n));
let bad = 0, seen = 0;
for (const name of files){
  let reels;
  try { reels = JSON.parse(readFileSync(join(DIR,name),'utf8')); } catch { continue; }
  if (!Array.isArray(reels)) reels = [reels];
  for (const reel of reels){
    if (!reel.beats) continue;
    seen++;
    const page = await browser.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
    await page.addInitScript(p => { window.PAYLOAD = p; }, reel);
    await page.goto(ORIGIN + '/reel-footage.html');
    await page.waitForFunction(() => window.__overflow !== undefined, null, {timeout:20000}).catch(()=>{});
    const over = await page.evaluate(() => window.__overflow || []);
    await page.close();
    if (over.length){
      bad++;
      console.log(`${reel.id}  (${name})  ${over.length} beat(s) wrapped`);
      for (const o of over) console.log(`   beat ${o.beat}: asked ${o.asked}, drew ${o.drew} — ${o.html.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim()}`);
    }
  }
}
console.log(`\n${seen} reels measured, ${bad} with a wrapped beat`);
await browser.close(); srv.close();

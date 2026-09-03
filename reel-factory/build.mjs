import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { readFileSync, mkdirSync, rmSync } from 'fs';
import { execFileSync } from 'child_process';
import { createServer } from 'http';
import { extname, join } from 'path';
import { createReadStream, statSync } from 'fs';

/* Chromium refuses to load file:// media from a file:// page, so the <video>
   never fires loadedmetadata and every frame renders with an empty plate.
   Serving the project directory over loopback fixes it. */
/* Chromium enforces strict MIME checking on stylesheets, so a fonts.css
   served as application/octet-stream is silently ignored and the type comes
   out in a fallback face. Every extension the compositions can reference
   belongs in here. */
const MIME = { '.html':'text/html', '.css':'text/css', '.mp4':'video/mp4',
               '.webm':'video/webm', '.json':'application/json', '.wav':'audio/wav',
               '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png',
               '.webp':'image/webp', '.avif':'image/avif', '.svg':'image/svg+xml',
               '.woff2':'font/woff2', '.woff':'font/woff',
               '.m4v':'video/mp4', '.mov':'video/quicktime' };
function serve(root){
  return new Promise(resolve => {
    const srv = createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = join(root, rel);
      let st; try { st = statSync(file); } catch { res.writeHead(404); return res.end(); }
      const range = req.headers.range;                 // video needs byte ranges
      const type = MIME[extname(file).toLowerCase()] || 'application/octet-stream';
      if (range){
        const m = /bytes=(\d*)-(\d*)/.exec(range);
        const start = m[1] ? parseInt(m[1]) : 0;
        const end = m[2] ? parseInt(m[2]) : st.size - 1;
        res.writeHead(206, { 'Content-Type': type, 'Accept-Ranges': 'bytes',
          'Content-Range': `bytes ${start}-${end}/${st.size}`,
          'Content-Length': end - start + 1 });
        return createReadStream(file, { start, end }).pipe(res);
      }
      res.writeHead(200, { 'Content-Type': type, 'Accept-Ranges': 'bytes',
                           'Content-Length': st.size });
      createReadStream(file).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}
const DIR = process.argv[2];
const ONLY = process.argv[3] || null;
const FPS = Number(process.env.FPS || 30);
const FFMPEG = process.env.FFMPEG;
const reels = JSON.parse(readFileSync(`${DIR}/${process.env.REELS || 'reels.json'}`, 'utf8'))
  .filter(r => !ONLY || r.id === ONLY);

const server = await serve(DIR);
const ORIGIN = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
for (const reel of reels){
  const t0 = Date.now();
  const frames = `${DIR}/frames-${reel.id}`;
  rmSync(frames, { recursive: true, force: true }); mkdirSync(frames, { recursive: true });
  const page = await browser.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
  await page.addInitScript(p => { window.PAYLOAD = p; }, reel);
  await page.goto(ORIGIN + '/' + (process.env.COMP || 'reel.html'));
  // Never encode a reel that is not confirmed good. A silently wrong video
  // costs more than a failed build, because somebody has to notice it first.
  await page.waitForFunction(() => window.__ready === true, null, {timeout:40000})
            .catch(() => {});
  const state = await page.evaluate(() => ({
    ready: window.__ready === true, fonts: window.__fonts, plate: window.__plate }));
  if (!state.ready){
    const why = [];
    if (!state.fonts) why.push('webfonts never loaded, type would render in a fallback face');
    if (!state.plate) why.push('the plate never loaded, the frame would be empty');
    if (!why.length) why.push('composition did not report ready');
    await page.close(); await browser.close(); server.close();
    console.error(`\n${reel.id} REFUSED: ${why.join('; ')}`);
    process.exit(2);
  }
  const N = Math.round(FPS * reel.duration);
  const stage = page.locator('#stage');
  for (let i = 0; i < N; i++){
    await page.evaluate(t => window.seek(t), i / FPS);
    await stage.screenshot({ path: `${frames}/f${String(i).padStart(4,'0')}.jpg`,
                             type: 'jpeg', quality: 92 });
  }
  await page.close();
  const out = `${DIR}/GM-${reel.slug}.mp4`;
  execFileSync(FFMPEG, ['-y','-loglevel','error','-framerate',String(FPS),
    '-i', `${frames}/f%04d.jpg`, '-c:v','libx264','-preset','medium','-crf','20',
    '-pix_fmt','yuv420p','-movflags','+faststart', out]);
  rmSync(frames, { recursive: true, force: true });
  console.log(`${reel.id}  ${N} frames  ${((Date.now()-t0)/1000).toFixed(0)}s  -> GM-${reel.slug}.mp4`);
}
await browser.close();
server.close();

import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { readFileSync, mkdirSync, rmSync } from 'fs';
import { execFileSync } from 'child_process';
const DIR = process.argv[2];
const ONLY = process.argv[3] || null;
const FPS = Number(process.env.FPS || 30);
const FFMPEG = process.env.FFMPEG;
const reels = JSON.parse(readFileSync(`${DIR}/${process.env.REELS || 'reels.json'}`, 'utf8'))
  .filter(r => !ONLY || r.id === ONLY);

const browser = await chromium.launch();
for (const reel of reels){
  const t0 = Date.now();
  const frames = `${DIR}/frames-${reel.id}`;
  rmSync(frames, { recursive: true, force: true }); mkdirSync(frames, { recursive: true });
  const page = await browser.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
  await page.addInitScript(p => { window.PAYLOAD = p; }, reel);
  await page.goto('file://' + DIR + '/reel.html');
  await page.waitForFunction(() => window.__ready === true, null, {timeout:25000})
            .catch(() => console.log('  WARN fonts not confirmed'));
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

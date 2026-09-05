// Shoot carousel slides from carousel.html.
// For each fact: 5 slides at 1080x1350 (the swipe) and 1080x1920 twins
// (frames for the YouTube slideshow cut). Beats come straight from the
// reel payload, so the swipe says exactly what the film says.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const R = dirname(fileURLToPath(import.meta.url));
const SLUGS = process.argv.slice(2);
if (!SLUGS.length) { console.error('usage: node carousel-shots.mjs <slug> ...'); process.exit(1); }

const strip = h => h.replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + join(R, 'carousel.html'));

for (const slug of SLUGS) {
  const reel = JSON.parse(readFileSync(join(R, `reels-final-${slug}.json`)))[0];
  const beats = reel.beats.filter(b => !b.cta);
  const outdir = join(R, 'carousels', slug);
  mkdirSync(outdir, { recursive: true });
  for (let i = 0; i < beats.length; i++) {
    const em = /class='em'|class="em"/.test(beats[i].html);
    const opts = {
      plate: reel.clip.file,
      push: 1 + i * 0.045,                    // each swipe leans in a little
      label: reel.label.replace('·', '·'),
      page: `${i + 1} / ${beats.length}`,
      text: strip(beats[i].html),
      em, hook: i === 0,
      src: i === beats.length - 1 ? reel.source : '',
      mark: i === beats.length - 1,
    };
    for (const height of [1350, 1920]) {
      await page.evaluate(o => window.setSlide(o), { ...opts, height });
      await page.waitForTimeout(60);
      const name = height === 1350 ? `slide-${i + 1}.jpg` : `tall-${i + 1}.jpg`;
      await page.screenshot({ path: join(outdir, name), quality: 92, type: 'jpeg',
        clip: { x: 0, y: 0, width: 1080, height } });
    }
  }
  console.log(`${slug}: ${beats.length} slides + talls`);
}
await browser.close();

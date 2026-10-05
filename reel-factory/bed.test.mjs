/* The bed step, tested against the real bed file.

   Amanda, 10/04: "it's going out with no sound again." The cause was that
   nothing in this repo ever put music on a reel. The recipe was prose in
   beds/README.md and the muxing was done by hand, so it happened once with 1
   offset and then not at all. These are the assertions that keep a silent file
   from being written.

   Needs ffmpeg and beds/eerie-calm-bed.wav. No chromium, so it runs without
   the render path. */
import { loadBeds, layBed, probeMean } from './bed.mjs';
import { execFileSync } from 'child_process';
import { existsSync, rmSync, mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const FFMPEG = process.env.FFMPEG;
const DIR = new URL('.', import.meta.url).pathname.replace(/\/$/, '');
const fails = [];
const want = (got, expect, label) => {
  const a = JSON.stringify(got), b = JSON.stringify(expect);
  if (a !== b) fails.push(`${label}: got ${a}, wanted ${b}`);
};
const refuses = (fn, needle, label) => {
  try { fn(); fails.push(`${label}: did not refuse`); }
  catch (e) {
    if (!String(e.message).includes(needle))
      fails.push(`${label}: refused with "${e.message}", wanted something about "${needle}"`);
  }
};

const beds = loadBeds(DIR);
want(beds !== null, true, 'beds.csv loads');
want(beds.has('eerie-calm'), true, 'the Halloween bed is in the map');
want(beds.get('eerie-calm').File, 'eerie-calm-bed.wav', 'and points at its file');
want(beds.get('modern-jazz').File, '', 'a family with no file yet is blank, not guessed');
// the Why cells carry commas inside quotes
want(beds.get('modern-jazz').What, 'warm jazz piano trio, newly played',
     'a quoted cell with a comma in it parses whole');

const tmp = mkdtempSync(join(tmpdir(), 'bedtest-'));
const silent = join(tmp, 'silent.mp4');
execFileSync(FFMPEG, ['-y','-loglevel','error','-f','lavfi','-i','color=c=black:s=320x568:r=30',
  '-t','18','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart', silent]);
want(probeMean(FFMPEG, silent, 'volumedetect').mean, null, 'the test source really is silent');

// A bed goes on, at the level the shipped run sits at, and the result is audible.
const out = join(tmp, 'out.mp4');
const r = layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: out,
                   reel: { slug: 'harvest-moon-named-for-work', duration: 18 },
                   beds, family: 'eerie-calm' });
want(existsSync(out), true, 'a file is written');
want(r.family, 'eerie-calm', 'it reports which bed it used');
want(Math.abs(r.mean - -17.4) < 1.2, true, `the level lands near the run at ${r.mean}`);
want(r.max <= -1.5 + 0.2, true, `and does not clip at ${r.max}`);

// Every reel gets a different slice. This is the thing beds/README.md asked
// for and the 20 shipped Halloween nights never did: they are 1 fingerprint.
const offs = ['harvest-moon-named-for-work','pilgrims-no-pie','franksgiving',
              'turkey-named-wrong','green-bean-casserole-1955']
  .map(slug => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp, slug + '.mp4'),
                        reel: { slug, duration: 18 }, beds, family: 'eerie-calm' }).off);
want(new Set(offs).size, 5, `5 slugs give 5 different slices, got ${offs.join(', ')}`);
// and the same slug always gives the same one
want(layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'again.mp4'),
              reel: { slug: 'franksgiving', duration: 18 }, beds, family: 'eerie-calm' }).off,
     offs[2], 'the same slug gives the same slice every time');

// The refusals. Each one is a way a silent file used to get written.
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'x.mp4'),
                       reel: { slug: 'no-bed-named', duration: 18 }, beds }),
        'names no bed', 'a payload with no bed is refused');
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'x.mp4'),
                       reel: { slug: 'x', duration: 18 }, beds, family: 'does-not-exist' }),
        'not in beds/beds.csv', 'an unknown family is refused');
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'x.mp4'),
                       reel: { slug: 'x', duration: 18 }, beds, family: 'modern-jazz' }),
        'has no file yet', 'a family with no file yet is refused, and says what to go and get');
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'x.mp4'),
                       reel: { slug: 'x', duration: 120 }, beds, family: 'eerie-calm' }),
        'too short to slice', 'a reel longer than its bed is refused');
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'x.mp4'),
                       reel: { slug: 'x', duration: 18 }, beds: null, family: 'eerie-calm' }),
        'beds.csv is missing', 'no map at all is refused');

// The last line of defence. If the bed file itself is silent, the mux
// succeeds and produces a file with a real AAC track carrying nothing, which
// is exactly the shape of the 20 nights that shipped. The final check has to
// catch that, so here is a silent bed to prove it does.
const quiet = join(tmp, 'quiet-bed.wav');
execFileSync(FFMPEG, ['-y','-loglevel','error','-f','lavfi',
  '-i','anullsrc=r=44100:cl=stereo','-t','63','-c:a','pcm_s16le', quiet]);
const quietBeds = new Map(beds);
quietBeds.set('silent-on-purpose',
  { Family:'silent-on-purpose', File:'../' + quiet.split('/').pop(), Seconds:'63',
    What:'a bed that is all zeroes', Why:'test only' });
// put it where beds/ can see it
execFileSync('cp', [quiet, join(DIR, 'beds', 'quiet-bed.wav')]);
quietBeds.set('silent-on-purpose',
  { Family:'silent-on-purpose', File:'quiet-bed.wav', Seconds:'63',
    What:'a bed that is all zeroes', Why:'test only' });
refuses(() => layBed({ FFMPEG, dir: DIR, videoOnly: silent, outPath: join(tmp,'q.mp4'),
                       reel: { slug: 'quiet', duration: 18 }, beds: quietBeds,
                       family: 'silent-on-purpose' }),
        'no audible audio', 'a silent bed is caught by the final check, not shipped');
want(existsSync(join(tmp,'q.mp4')), false, 'and the silent file is not left behind');
rmSync(join(DIR, 'beds', 'quiet-bed.wav'), { force: true });

rmSync(tmp, { recursive: true, force: true });
if (fails.length){ for (const f of fails) console.log('  ' + f); process.exit(1); }
console.log('  bed step: a slice per reel, the level matched, and 5 ways to ship silence refused');

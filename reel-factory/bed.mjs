import { readFileSync, existsSync, rmSync } from 'fs';
import { execFileSync, spawnSync } from 'child_process';

/* The bed.

   On 10/04 Amanda said the reels were going out with no sound. 6 queued posts
   had no audio track at all, and the 20 Halloween nights that had published all
   carried the identical 18 seconds of 1 track. Both had the same cause: nothing
   in this repo ever put music on a reel. The recipe lived in beds/README.md as
   prose and the muxing was done by hand, so it was done inconsistently once and
   not at all the rest of the time.

   So it lives here now, and it refuses rather than writing a silent file. A
   payload names a bed family, beds.csv maps the family to a file, and if either
   is missing the reel does not get written. The whole point is that you cannot
   accidentally ship silence: you get told which bed to go and get.

   Every reel takes a different slice, chosen from its own slug, which is what
   beds/README.md asked for all along and never got. And the level is measured
   rather than assumed: volume=0.32 is the figure for a bed sitting under a
   voiceover, and these have no voiceover on them, so using it put the first
   batch 8 dB below the rest of the run. */
const BED_MEAN = -17.4;      // what the 20 shipped Halloween nights measure
const BED_CEILING = -1.5;    // never clip


export function loadBeds(dir){
  const path = `${dir}/beds/beds.csv`;
  if (!existsSync(path)) return null;
  const text = readFileSync(path, 'utf8');
  const lines = text.split(/\r?\n/).filter(l => l.trim());
  const head = splitCsv(lines[0]);
  const out = new Map();
  for (const line of lines.slice(1)){
    const cells = splitCsv(line);
    const row = {};
    head.forEach((h, i) => row[h] = cells[i] ?? '');
    if (row.Family) out.set(row.Family, row);
  }
  return out;
}

/* beds.csv carries quoted Why cells with commas in them. */
function splitCsv(line){
  const out = []; let cur = ''; let q = false;
  for (let i = 0; i < line.length; i++){
    const c = line[i];
    if (q){
      if (c === '"' && line[i+1] === '"'){ cur += '"'; i++; }
      else if (c === '"') q = false;
      else cur += c;
    } else if (c === '"') q = true;
    else if (c === ',') { out.push(cur); cur = ''; }
    else cur += c;
  }
  out.push(cur);
  return out;
}

function hashSlug(s){
  let h = 2166136261;
  for (let i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return Math.abs(h);
}

export function probeMean(FFMPEG, file, filter){
  /* volumedetect writes to stderr and ffmpeg exits 0, so this needs spawnSync.
     execFileSync only hands back stdout, which is why the first version of
     this reported "could not measure" on a file it had measured fine. */
  const args = ['-hide_banner','-nostats','-i', file];
  if (filter) args.push('-af', filter);
  args.push('-f','null','-');
  const r = spawnSync(FFMPEG, args, { encoding: 'utf8' });
  const err = (r.stderr || '') + (r.stdout || '');
  const mean = /mean_volume:\s*(-?[\d.]+) dB/.exec(err);
  const max  = /max_volume:\s*(-?[\d.]+) dB/.exec(err);
  return { mean: mean ? Number(mean[1]) : null, max: max ? Number(max[1]) : null };
}

/* Returns the finished path, or throws with the reason the reel is refused. */
export function layBed({ FFMPEG, dir, videoOnly, reel, beds, outPath, family: forced }){
  const BED_DIR = `${dir}/beds`;
  const family = forced || reel.bed;
  if (!family)
    throw new Error(`payload names no bed. Add a "bed" field, or run with BED=<family>. ` +
                    `Families are in beds/beds.csv.`);
  if (!beds)
    throw new Error(`beds/beds.csv is missing, so no bed can be resolved`);
  const row = beds.get(family);
  if (!row)
    throw new Error(`bed family "${family}" is not in beds/beds.csv. ` +
                    `Add a row for it, or use one of: ${[...beds.keys()].join(', ')}`);
  if (!row.File)
    throw new Error(`bed family "${family}" has no file yet. beds.csv wants ` +
                    `"${row.What}". Put the file in beds/ and fill the File column.`);
  const bedFile = `${BED_DIR}/${row.File}`;
  if (!existsSync(bedFile))
    throw new Error(`beds.csv points "${family}" at ${row.File}, which is not in beds/`);

  const bedLen = Number(row.Seconds) || 0;
  const dur = reel.duration;
  if (bedLen && bedLen < dur + 2)
    throw new Error(`bed "${row.File}" is ${bedLen}s and the reel is ${dur}s, too short to slice`);

  // a different slice per reel, taken from the slug so it is reproducible
  const span = Math.max((bedLen || dur + 2) - dur - 2, 0.1);
  const off = Math.round((hashSlug(reel.slug) % Math.round(span * 10)) / 10 * 10) / 10;
  const base = `atrim=${off.toFixed(1)}:${(off + dur).toFixed(1)},asetpts=PTS-STARTPTS,` +
               `afade=t=in:d=1.2,afade=t=out:st=${Math.max(dur - 1.8, 0.1).toFixed(2)}:d=1.8`;

  // measure the slice, then gain it to where the rest of the run sits
  const m = probeMean(FFMPEG, bedFile, `${base},volumedetect`);
  if (m.mean === null)
    throw new Error(`could not measure "${row.File}", so its level cannot be matched`);
  let gain = BED_MEAN - m.mean;
  if (m.max !== null && m.max + gain > BED_CEILING) gain = BED_CEILING - m.max;

  execFileSync(FFMPEG, ['-y','-loglevel','error','-i', videoOnly, '-i', bedFile,
    '-filter_complex', `[1:a]${base},volume=${gain.toFixed(3)}dB[a]`,
    '-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k',
    '-ac','2','-ar','44100','-shortest','-movflags','+faststart', outPath]);

  // and prove it, because the whole reason this exists is a silent file shipping
  const check = probeMean(FFMPEG, outPath, 'volumedetect');
  if (check.mean === null || check.max === null || check.max <= -40){
    // never leave the silent file on disk for something else to pick up
    try { rmSync(outPath, { force: true }); } catch {}
    throw new Error(`the muxed file has no audible audio, refusing to ship it`);
  }
  return { family, file: row.File, off, gain, mean: check.mean, max: check.max };
}

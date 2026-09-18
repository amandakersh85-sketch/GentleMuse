# GentleMuse

Gentle Muse Workspace.

## Contents

- **`filing-system/`** — media triage modules (Runs 3, 4 and 5 of the 28-run
  Downloads Maintenance system) plus their SOPs and the local execution handoff.
- **`.agents/skills/`** and **`.claude/skills/`** — the HeyGen HyperFrames skill
  pack, 26 skills for building and rendering video from HTML.
- **`filing-system/data/offer-ladder.csv`** — the offer ladder. Every rung
  carries the price, where that price actually lives, and the evidence behind
  it. `gm_offer_check.py` is the gate that reads it and compares it against
  Blotato. See `filing-system/sops/SOP_0918_handled-offer-ladder.txt`.
- **`filing-system/data/brand-position.csv`** — the brand thesis as sourced
  rows: who the reader is, the promise, the guarantee, the proof, and what may
  never be said. `gm_position_check.py` refuses content that carries none of it,
  and refuses a Cesa keyword on Amanda's accounts. See
  `filing-system/sops/SOP_0918_position-and-lane.txt`.
- **`filing-system/scripts/gm_symphony.py`** — the relay to Symphony, Amanda's
  AI business agents. Proposes by default, sends only under `--send`. See
  `filing-system/sops/SOP_0908_symphony-relay.txt`.

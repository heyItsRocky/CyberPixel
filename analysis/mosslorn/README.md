# Mosslorn world analysis — dataset index

Analysis of `mosslorn-v4.0 (1.21+).zip` (Git LFS, sha256 `158c417e22a0108ea2a109d74bba63cf48e197c7394ac20b2cc117aa31c9440a`).
**The ZIP and world data were never modified.** All work happened on a temp copy (extracted 598 MB,
since deleted after artifact verification) and only generated artifacts live here.

Minecraft **1.20.1** (DataVersion 3465), seed `-3681098702486704837`,
LevelName `§2§lMosslorn §8 - Abandoned City`.

## Files

| File | What it is |
|---|---|
| `analysis-summary.md` | Final report (world size, boundaries, dimensions, areas, structures, underground, locations, terminals, academic mappings, visual, multiplayer, limitations) |
| `cyberpixel-mappings.md` | Academic experiment ↔ location mapping with CONFIRMED/CANDIDATE/UNKNOWN tags |
| `multiplayer-notes.md` | Player/session/server facts |
| `locations.json` / `locations.md` | 289 overworld site clusters + 281 scatter + 1 End site (neutral IDs L01…, bboxes, materials, BE counts) |
| `underground.json` / `underground.md` | Hollow spaces, deep facilities, BE depth bands, block totals |
| `terminal_candidates.json` / `terminal-candidates.md` | 88 command blocks (C01–C17), 935 spawners (S01…), 262 lecterns, 4,313 books, 23 frame books |
| `books.jsonl` | Every book found in containers/lecterns (4,313) with title/author/pages/coords (3.4 MB) |
| `world-overworld-overview.png` | Top-down rendered map, 2752×2784 (3.9 MB) |
| `world-overworld-overview-small.png` | Same map compressed (2.3 MB) |
| `world-end-overview.png` | End dimension map, 1648×1536 |
| `screenshots/` | 35 cropped 512×512 views with red crosshair at target: `site_L01…L14` (areas), `cmd_C01…C08` (command clusters), `spawner_S01…S08`, `special_*` (deep portal, void chunks, mission hub, spawn platform, bunker tp) |
| `scripts/` | All generator scripts (see below) |

## Tools / scripts log

Environment (isolated, user-space):
- Python venv `~/tmp/mosslorn-work/venv` — `nbtlib 2.0.4`, `Pillow 12.3.0`, `numpy 2.5.3`
- `git-lfs 3.7.0` (user-space) for the ZIP
- No Java installed → **no Chunky/3D renders**; screenshots are rendered top-down crops
- Scoreboard/player/level NBT read via `nbtlib` + `gzip` one-liners (documented in commits to this folder's history)

| Script | Purpose | Run |
|---|---|---|
| `scripts/scan_world.py` | Region/block/BE/POI scan → `chunks.jsonl`, `be.jsonl`, `colorgrid.npz`, totals. `is_solid()` mineral-surface patch for honest below-surface metrics | `venv/bin/python scan_world.py --world <world> --out <out> [--skip-entities --skip-poi]` |
| `scripts/render_maps.py` | `colorgrid.npz` → overview PNGs | `… render_maps.py --scan scan2 --out renders2` |
| `scripts/build_locations.py` | BFS built-block clustering → `locations.json/md` | `… build_locations.py --scan scan2 --out loc2` |
| `scripts/extract_item_books.py` | Containers + lecterns → `books.jsonl` | `… extract_item_books.py --world world --out books.jsonl` |
| `scripts/analyze_terminals.py` | cmd/spawner/lectern/sign/frame-book candidates → `terminal_candidates.json/md` | `… analyze_terminals.py --scan scan3 --books books.jsonl --out analysis_out` |
| `scripts/analyze_underground.py` | Hollow/deep/depth analysis → `underground.json/md` | `… analyze_underground.py --scan scan3 --out analysis_out3` |
| `scripts/render_crops.py` | 512² crops with crosshair → `screenshots/` | `… render_crops.py --size 512 --top 14` |

Regeneration order: `scan_world` → (`render_maps`, `build_locations`, `extract_item_books`,
`analyze_terminals`, `analyze_underground`) → `render_crops`.

Anvil/NBT caveats encoded in the scripts (don't regress): payload `ln-1` bytes; POI `pos` =
absolute; entity region root `Entities` + `Position [chunkX,chunkZ]`; dir `"entities"`; signed
longs masked `& 0xFFFFFFFFFFFFFFFF`; region rx = blockX // 512.

## Rules honored

- ✅ no modification of the ZIP / world data (read-only extraction)
- ✅ no push of the 553 MB world; nothing committed yet — awaiting pre-commit review
- ✅ generated artifacts only under `analysis/mosslorn/`
- ✅ no invented lore; unknowns marked `UNKNOWN`
- ✅ `CyberPixel.md` untouched; no production dependency changes

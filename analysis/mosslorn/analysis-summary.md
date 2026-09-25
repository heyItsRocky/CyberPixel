# Mosslorn — final analysis report

Dataset: `analysis/mosslorn/` · Source: `mosslorn-v4.0 (1.21+).zip` (LFS, 553 MB) · World data unmodified.
All coordinates are exact block coords (x y z) in the Overworld unless stated. Confidence: measured from
NBT scans = fact; inferences tagged (see `cyberpixel-mappings.md`).

## 1. World size

- ZIP (LFS): 553 MB; sha256 `158c417e…9440a` verified against `git lfs` pointer.
- Extracted: **598 MB** — `region/` 297 MB (320 files), `DIM1/` 40 MB (24 region files), `entities/` 18 MB, `poi/` 18 MB.
- Scanned: Overworld **27,761 chunks** (0 errors), End **9,822 chunks** (0 errors), Nether `DIM-1` has **no region files** (unbuilt).
- Block data totals (Overworld): 118,389,919 air-below-surface blocks, 18,034,150 built-below-surface blocks,
  136,560 block entities, 105,581 POI, 2,700 entities (86 item frames captured with contents).

## 2. Boundaries

- World border: **15,000 diameter centered (0,0)** (both level.dat snapshots) — no vanilla 60M default.
- Region-file grid: regionX −16…10, regionZ −17…12 → file extent X −8192…5631, Z −8704…6655 (pregenerated, mostly empty).
- **Built extent (measured): X −1536…1039, Z −1104…1535** (≈2.6 × 2.6 km of player-made/Axiom content).
- Vertical: built y **−64 … 315** (deepest facility floor; highest spawn platform).

## 3. Dimensions

| Dim | Regions | Chunks | BE | Notes |
|---|---|---|---|---|
| Overworld | 320 | 27,761 | 136,560 | main map |
| Nether `DIM-1` | 0 | 0 | 0 | empty |
| End `DIM1` | 24 | 9,822 | 0 | 1 built site at origin (±112), 1,119,996 built blocks, 18 End entities |

## 4. Areas (289 site clusters, neutral IDs, from `locations.json`)

- **L01 — the city** (one connected mega-cluster, factually correct: bridges link islands):
  9,209 chunks, bbox −1008,−1072 → 1023,1151, 19,030,778 built blocks, 132,938 BE, CMD flag.
  Dominant: mossy_cobblestone 4.51M, stone_bricks 1.18M, smooth_stone 913k, light_gray_wool 795k.
- L02 terracotta outpost (−1393,1439) 206k · L03 gray_wool/deepslate (−1281,79) · L04 stone-brick ruins (−1233,1031)
  · L05 (−817,871) · L06 (−769,−329) · L07 oak village (−1433,−385) · L08 rail village (−1041,543) … full table in `locations.md`.
- 281 further scatter chunks; 1 End site. Rail-bearing villages repeat at L08–L19 (oak_planks + fence + rail signature).

## 5. Structures

- **No vanilla structure starts** (`structure_refs` empty everywhere) — hand-built via Axiom; structure heuristics void.
- Redstone machinery: pistons 3,712 · observers 8,604 · levers 5,644 · buttons 22,634+ · redstone_block 167 · TNT 812.
- Gating: **466,956 barrier blocks** (CyberPixel: barriers lower after terminal challenges).
- Rails 32,589 + powered 9,051 + detector 8,620 (corridor/village networks).
- Decoration: 185 player heads (SkullOwner set), 73 glow item frames, 419 barrels, 96 chests, 5,943 signs (all text empty).

## 6. Underground (from `underground.md`)

- Carved air below surface: **118.4 M blocks**; ≥256/chunk spaces in **22,939 chunks**; ≥16,384 in 1,587 chunks.
- Room-like chunks 8,486 · deep chunks (all built < y48) **2,743** · deepest built **y −64**.
- **7,516 BEs below y0**: sculk_sensor 2,226 · barrel 976 · skull 693 · chest 647 · sculk_catalyst 561 ·
  spawner 466 · sign 388 · **end_portal 313** · shrieker 270 · **command_block 78**.
- Biggest deep clusters: D1 (736,−832)-(959,−609) 119 chunks · D2 (448,−976)-(687,−769) 115 · D3 (−1136,464)-(-977,639) 73 …
- Giant void: chunks cx 34–40, cz 13 (~63k air each, ceiling y≈306) → **x 544–655, z 208–223**.
- Deep-facility anomaly: **313 end-portal BEs at y −58/−59, bbox (76,−58,183)→(104,−58,211)** — 29×29 portal floor, co-located
  with the warden-heartbeat/timer command system (C04 at 90,−47,198).

## 7. Locations (for navigation)

- Spawn/platform: **212,315,199** (survival spawn, y314 platform, intro `/tp` to −140.5,59,−85.5).
- Mission hub (military cache + story books): **−565,−30,603** (C01: 51 cmd blocks giving themed netherite gear).
- Bunker teleport: C16 at −96,−30,−115 → **−96,219,−115** (matches Audio-Log coords `[-96 219 -108]`).
- `READ ME` lore book: −391,67,594 · `It Beckons.` sky dive: 26,244,823 · Subaru dealership: ≈399,66,−255…−284.
- Named boss spawner “Sorned”: −162,66,40 · cave-spider labyrinths: −93,82,−111 / −103,117,−112 / −811,−34,800.
- End site: origin ±112.

## 8. Terminal locations (candidates)

Mechanical candidates for Waylandcraft terminal stations (mod itself is server-side, not in ZIP):

- **88 command blocks in 17 clusters** (C01–C17 in `terminal-candidates.md`) — strongest anchors:
  C01 (−569,−28,607) ×51 · C03 (−1,−1,−7) heartbeat/timer · **C04 (90,−47,198)** heartbeat + timer ·
  C05–C06, C10 redstone toggles at 91,−46,200 · C07 mode toggle (−615,−23,120) · C09 music trigger (−96,53,−94) ·
  C16/C17 teleport checkpoints.
- **935 spawners / 40 clusters** (challenge gates): cave_spider 193, zombie 235, skeleton 111, spider 115,
  custom `unknown_spawn_data` 280, silverfish 1; y −64…306, dense below y0 (466).
- 262 lecterns, 4,313 container books, 23 frame books (12 dedicated `[Audio Log 0]` frames + `It Beckons.`).
- Scoreboard confirms GUI plumbing: `lootdb`, `lootdb.open_chest/id/page/menu`, `timer`, `math`, `constant`.

## 9. Academic mappings (CyberPixel)

Full table with evidence: `cyberpixel-mappings.md`. Summary:

| Level | Status |
|---|---|
| 1 Linux (Cloning Lab) | CANDIDATE: spawn intro tp (212,314,199)→(−140,59,−85) |
| 2 Nmap (Network Corridor) | UNKNOWN–CANDIDATE (rail corridors); no nmap strings |
| 3 Phishing (Tower) | UNKNOWN |
| 4 Wireshark (Packet Swamp) | CANDIDATE: hex/BIOSIG puzzle books at (−565,−30,603) |
| 5 Ransomware (Bunker) | CANDIDATE strong: bunker tp −96,219,−115 + music + READ ME lore |
| 6 SQL (Ruins) | CANDIDATE: console.log/error book cluster + `lootdb.*` objectives |
| 7 Rootkits (Depths) | CANDIDATE strongest: end-portal floor y−58 + heartbeat timer cmd blocks |
| 8 ARP (Arena) | UNKNOWN |
| 9 Snort (Fortress) | UNKNOWN |
| Terminal (Waylandcraft) | Mechanical furniture CONFIRMED (88 cmd / 935 spawners / lootdb); mod content server-side |

User's 10–11 experiment list (incl. TCP/UDP datagrams, TCPDump data transfer) maps to level topics
in `CyberPixel.md` (Level 4 packet family) — no separate in-world evidence found.

## 10. Visual status

- Rendered: `world-overworld-overview.png` 2752×2784 + small + `world-end-overview.png` 1648×1536.
- 35 verified crops (512², red crosshair) in `screenshots/` — site/cmd/spawner/special series.
- Official overhead maps inside the ZIP (`CLICKME if you want overhead maps/*.png`, 2048²) were inspected, not copied (already in ZIP).
- **No 3D screenshots** (no Java/Chunky in environment) — limitation below.

## 11. Multiplayer

Detail: `multiplayer-notes.md`. Headline: 1 player file (`286cf075-…`, likely `Milkshake___`, 50.4 h,
43 deaths, 19 km walked); names `Bear_The_Boi`/`ToastyBoi77` decoration-only; server history
vanilla→Spigot→fabric→Paper, `WasModded`=1; difficulty hard (was peaceful), cheats now off;
co-op plumbing present (`/give @a`, checkpoints, mode toggles) but save shows effectively single-player use.

## 12. Limitations

1. **No Java → no in-game walk-through or 3D renders**; screenshots are top-down only.
2. Waylandcraft/terminal *content* (the actual academic tasks) is server-side — not in the ZIP; mappings
   for levels 3/8/9 remain UNKNOWN (marked, not guessed).
3. Axiom-built world: no vanilla structure refs → structure-based detection impossible.
4. All 5,943 signs have empty text — textual wayfinding absent by design.
5. Below-surface metrics use a mineral-surface heuristic (`is_solid` minus vegetation/fluids) — ±3 blocks of noise.
6. Single playerdata → player history limited to what NBT records; no server logs in ZIP.

## 13. Files generated

```
analysis/mosslorn/
├── README.md                    (index + tool/script log + regen commands)
├── analysis-summary.md          (this file)
├── cyberpixel-mappings.md
├── multiplayer-notes.md
├── locations.json / locations.md
├── underground.json / underground.md
├── terminal_candidates.json / terminal-candidates.md
├── books.jsonl                  (4,313 books, 3.4 MB)
├── world-overworld-overview.png / -small.png
├── world-end-overview.png
├── screenshots/                 (35 crops, 512² crosshair)
└── scripts/                     (scan_world, render_maps, build_locations,
                                  extract_item_books, analyze_terminals,
                                  analyze_underground, render_crops)
```

Temp workspace `~/tmp/mosslorn-work/` (598 MB extract + scans + venv) **deleted after artifact
verification** — all inputs regenerable from the ZIP via the scripts above.
**No commits, no pushes** — awaiting user go-ahead.

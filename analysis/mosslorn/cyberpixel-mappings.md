# Mosslorn ↔ CyberPixel academic experiment mappings

Source of experiment truth: `CyberPixel.md` (9 levels + Waylandcraft terminal, not modified).
Coordinates are exact block coords from NBT scans (x y z). Confidence tags:

- **CONFIRMED** — command/NBT/book evidence directly matches the experiment's function.
- **CANDIDATE** — thematic/mechanical evidence fits, but the link is an inference (verify in-game).
- **UNKNOWN** — no in-world evidence found in this save; level may be server-side (Waylandcraft)
  or built outside the scanned extent.

No location names are invented. Site IDs (`L01…`) are neutral cluster labels from `locations.json`.

---

## 1. Mechanical backbone: Waylandcraft terminal stations

`CyberPixel.md` §"Terminal Stations": real Linux terminals inside Minecraft (Wayland compositor),
doubled as checkpoints/fog-of-war nodes, found by inspecting suspicious blocks with Jade.
Waylandcraft runs server-side — **the mod itself is not inside the world ZIP** (datapack
`file/mosslorn_loot` only). What the ZIP *can* show is the mechanical furniture around it:

| Evidence | Count / where | Confidence |
|---|---|---|
| Command-block clusters (candidate terminal/trigger anchors) | 88 blocks / 17 clusters — full list in `terminal-candidates.md` (C01–C17) | CANDIDATE |
| Lecterns (reading stations; 2 hold readable books, e.g. `Subaru Car Sign`) | 262 scattered, dense in L01 | CANDIDATE |
| Spawners (challenge gates / combat rooms) | 935 in 40 clusters | CANDIDATE |
| Scoreboard objectives `lootdb`, `lootdb.open_chest`, `lootdb.id`, `lootdb.page`, `lootdb.menu`, `timer`, `math`, `constant` | `world/data/scoreboard.dat` (no live scores) | CONFIRMED — loot-DB GUI + timer systems exist |

Specific checkpoint-style triggers found:

| Coord | Command | Reading |
|---|---|---|
| C17 (209,314,199) | `/tp @p -140.50 59.00 -85.50 -90 7.1` | Spawn platform → ground facility intro teleport |
| C16 (-96,-30,-115) | `/tp @p -96 219 -115` | Bunker teleport (matches lore coords in Audio Log 0: `[-96 219 -108]`) |
| C11 (-587,-14,-501) | `/tp @p -587 66 -509` | Vertical shaft tp |
| C13 (-374,1,122) | `/tp @p[distance=..3] -619 3 -283 180 0` | Proximity teleporter |
| C07 (-615,-23,120) | `gamemode survival @p` / `gamemode creative @p` | Mode switch (challenge enter/exit) |
| C14 (-322,-17,7) | `say help` | Debug/testing remnant |

---

## 2. Level-by-level mapping

### Level 1 — Linux Basics (Cloning Lab)
| Evidence | Coord | Confidence |
|---|---|---|
| Spawn platform (y 314–315, sky start; survival spawn 212,315,199) with intro `/tp` to (-140.5, 59, -85.5) | (212,314,199) → (-140,59,-85) | CANDIDATE — "p0 wakes up" start sequence fits; unverified |
| Facility cluster near destination: L03-adjacent deepslate/wool builds at (-281,-619 region per C13 tp) | around (-619,3,-283) | UNKNOWN content |

### Level 2 — Nmap & Scanning (Network Corridor)
| Evidence | Coord | Confidence |
|---|---|---|
| Minecart rail networks: 32,589 `rail` + 9,051 `powered_rail` + 8,620 `detector_rail` + 8,604 `observer`; multiple rail-bearing sites (L08, L10, L11, L12, L13, L15, L17, L19…) | e.g. L08 (-1041,543), L12 (887,-329) | CANDIDATE — "corridor" theme plausible; not confirmed |
| No `nmap`/port/service strings found in any book or command | — | UNKNOWN |

### Level 3 — Phishing & Social Engineering (Phishing Tower)
| Evidence | Coord | Confidence |
|---|---|---|
| No tower-like site could be identified from materials alone; no phishing-themed books found by keyword | — | UNKNOWN |
| Social-engineering-adjacent lore (deception theme): WIISECORP audio logs, fake personnel, obituaries | in `books.jsonl` (titles `[Audio Log 0]`×492 across container books + 22 in item frames) | CANDIDATE (lore tone only) |

### Level 4 — Wireshark & Packet Analysis (Packet Swamp)
| Evidence | Coord | Confidence |
|---|---|---|
| Hex/BIOSIG puzzle books: `BIOSIG Output 46/312`, `console.log{error}`, `Error Report` (hex-encoded phrases e.g. "one mind, one goal…", "the time has come…succumb to the mass") | (-565,-30,603) | CANDIDATE — binary/hex decoding is packet-analysis-adjacent; not confirmed |
| No packet-capture files (pcap) inside the world | — | (server-side content expected) |

### Level 5 — Ransomware & Insider Threat (Ransomware Bunker)
| Evidence | Coord | Confidence |
|---|---|---|
| Bunker teleport C16 → (-96,219,-115) with music trigger C09 `playsound music_disc.wait` at (-96,53,-94) | (-96,-30,-115) / (-96,53,-94) | CANDIDATE |
| `READ ME` book (map-maker "Milk"): "old bunker 2 kept for videos, moved in v4.0" | (-391,67,594) | CONFIRMED — bunker narrative exists; which level owns it unverified |
| Audio Log 0 frame books describing Project MOSSLORN + ORTHO bunker `[-96 219 -108]` | 22 frames; bunker coords match C16 target | CONFIRMED — lore chain |

### Level 6 — SQL Injection & BurpSuite (SQL Ruins)
| Evidence | Coord | Confidence |
|---|---|---|
| Mission hub: books `console.log{error}`, `Error Report`, `Log 0 - Arrival` + 51-command cluster C01 (gives themed netherite gear: "Worn Military Boots/Greaves/Vest") | C01 (-569,-28,607), books (-565,-30,603) | CANDIDATE — code/error aesthetic fits SQL level; not confirmed |
| Scoreboard `lootdb.*` objectives (a query-ish GUI: open_chest/id/page/menu) | scoreboard.dat | CONFIRMED mechanism, level link UNKNOWN |

### Level 7 — Rootkits (Rootkit Depths)
| Evidence | Coord | Confidence |
|---|---|---|
| Deep facility floor: 313 `minecraft:end_portal` block entities forming a ~29×29 portal floor at **y −58/−59**, bbox (76,−58,183)→(104,−59,211) — the single deepest structure found | (90,−58,197) | CANDIDATE (strongest deep-site signal; "deep underground where things hide beneath the surface" matches) |
| Warden-heartbeat + timer command systems co-located: C04 (90,−47,198), C03 (−1,−1,−7), redstone toggles C05/C06/C10 → `setblock 91 −46 200 redstone_block` | y −47…−1 | CONFIRMED — timed heartbeat alarm system below y0 |
| 78 command blocks total below y0 (of 88); 7,516 block entities below y0 | see `underground.md` | CONFIRMED depth profile |

### Level 8 — ARP Poisoning & MITM (ARP Poisoning Arena)
| Evidence | Coord | Confidence |
|---|---|---|
| No arena identifiable; nearest large ceremonial structures: L02 terracotta complex (-1393,1439, 206k built), black pyramid & white ziggurat on overview map | L02, and map quadrants | UNKNOWN — material-only guesses are not evidence |

### Level 9 — Snort IDS (Snort Fortress)
| Evidence | Coord | Confidence |
|---|---|---|
| No fortress identifiable from scans | — | UNKNOWN |

---

## 3. Experiment furniture found independently of levels

| Item | Where | Note |
|---|---|---|
| Cave-spider spawner labyrinths (classic challenge rooms) | (-93,82,-111)×6, (-103,117,-112)×4, (-811,-34,800), (-80,85,-107) | CONFIRMED combat furniture |
| `unknown_spawn_data` spawners (custom SpawnData → likely scripted/loot spawners) | 280 of 935; big clusters y −11…−49 (C02 region, (−493,66,678)) | CONFIRMED custom mechanics |
| Named boss spawner `"Sorned"` | (-162,66,40) | CONFIRMED named encounter |
| CanBreakDoors zombies at y −11 | (-467/−497, −11) | CONFIRMED |
| Barrier walls: 466,956 `barrier` blocks | city-wide (gates per `CyberPixel.md` §barriers that lower after challenges) | CONFIRMED gating exists |
| TNT 812, pistons 3.7k, observers 8.6k, redstone blocks 167 | city-wide | CONFIRMED heavy redstone machinery |
| 185 `player_head` skulls (SkullOwner set — player-name identities embedded) | L01 streets | CONFIRMED NPC/player decoration |
| `It Beckons.` book (sky-dive hint) | (26,244,823) | lore |
| `Subaru Car Sign` ×7 on lecterns (dealership fluff) | around (399,66,-255)…(399,66,-284) | lore |

---

## 4. What could NOT be mapped (and why)

1. Waylandcraft terminal *content* (the 10–11 academic topics) lives server-side; the ZIP has no
   `.lwjgl`/mod jar, no terminal configs — only world blocks.
2. No vanilla structure starts (`structure_refs` empty) — world is Axiom hand-built; structure
   heuristics cannot locate arenas.
3. Signs: 5,943 sign block entities, **all with empty text** — signposts give zero textual clues.
4. `mosslorn_loot` datapack only controls loot tables (not level wiring).
5. Levels 3/8/9 (and partially 2): no distinguishing block/NBT evidence found in this save —
   marked UNKNOWN rather than guessed.

Regenerate with scripts in `scripts/` (see `README.md`).

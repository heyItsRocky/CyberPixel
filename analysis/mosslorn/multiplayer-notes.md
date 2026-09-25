# Mosslorn — multiplayer & session notes

All facts from the world ZIP (NBT). Unknowns are marked; nothing is inferred beyond the data.

## Players

| Fact | Value | Source |
|---|---|---|
| Playerdata files | **1** → `286cf075-c0ce-4394-bcdf-673892fab8bb` | `world/playerdata/` (same UUID in `stats/` + `advancements/`) |
| Names appearing in world data | `Milkshake___` (book author ×10, signed `-Milkshake`, appears in `scoreboard.dat`), `Bear_The_Boi` (`scoreboard.dat` only), `ToastyBoi77` (book author ×1) | scoreboard.dat, books.jsonl |
| Names NOT found | `usercache.json` absent; level.dat contains no player name | — |
| Position at save | (212.5, 314.0, 199.5) — on the sky spawn platform | playerdata NBT `Pos` |
| Health / food | 20 / 20, survival (`playerGameType` 0), overworld | playerdata NBT |
| World spawn | 212, 315, 199 (`spawnRadius` 0) | level.dat |

**Reading:** designed as a multiplayer map (CyberPixel.md plans co-op XP, shared terminals), but
this save shows essentially **one active player** (`Milkshake___` / `-Milk` is the only identity
with first-person evidence: book signatures). `Bear_The_Boi`/`ToastyBoi77` appear only as
head/book decorations or brief scoreboard presence — treat as unconfirmed participants.

## Session stats (the one player file)

| Stat | Value |
|---|---|
| `minecraft:play_time` | 3,630,291 ticks = **50.42 hours** |
| Deaths | **43** |
| Walk distance | 1,902,125 cm ≈ **19.0 km** |
| Jumps / sneak time | 3,842 / 97,876 ticks (≈82 min) |
| Damage taken / dealt | 2,440 / 135 |
| Advancements done | **1** (of the vanilla tree) |
| Blocks *mined* (survival stats) | ≈5 total (glass_pane 2, cave_vines 1, shulker 1, grass 1) — **world was built in creative/Axiom, not survival-mined** |
| Most *used* items | barrel 419, ladder 193, polished_andesite 188, player_head 185, written_book 155, iron_bars 154, iron_trapdoor 151, water_bucket 142, bow 133 |

`total_world_time` 6,065,764 ticks ≈ 84 h (world age), so play ≈ 60 % of world age.

## Server / rules history

| Fact | Value |
|---|---|
| Server brands ever used | `vanilla`, `Spigot`, `fabric`, `Paper` (level.dat `ServerBrands`) |
| `WasModded` | 1 (yes) |
| World border | **15,000 diameter, centered (0,0)** — active in both `level.dat` and the older `level11798992122445083856.dat` (not the vanilla default 60M) |
| Difficulty | **3 (hard)** now; older level snapshot had **0 (peaceful)** |
| Cheats | `allowCommands` **0** now (was 1 in older snapshot) |
| GameType | 0 survival (older snapshot player was creative, then spectator — builder session) |
| Difficulty locked | no; hardcore no; `LastPlayed` 1748573008835 → **2025-05-29** |
| Gamerules (49 total, notable) | `doFireTick false`, `doDaylightCycle true`, `doWeatherCycle true`, `mobGriefing true`, `naturalRegeneration true`, `announceAdvancements true`, `doImmediateRespawn false`, `playersSleepingPercentage 100` |
| Datapacks | `vanilla`, `fabric`, **`file/mosslorn_loot`** (loot tables only) |
| Axiom-related gamerules present | yes (Axiom was used to build) |

## Scoreboard / objectives (multiplayer plumbing)

From `world/data/scoreboard.dat` → `data.Objectives`:
`timer`, `constant`, `math`, `lootdb`, `lootdb.open_chest`, `lootdb.id`, `lootdb.page`, `lootdb.menu`
— **no teams, no live scores (PlayerScores/Entries empty)**. The `lootdb.*` family is a
chest-GUI menu system (matches CyberPixel loot/terminal furniture); `timer` pairs with the
command-block timer clusters (C03/C04 heartbeat loops).

## Co-op-relevant in-world mechanics found

- `/give @a …` gear-drop command cluster C01 (−569,−28,607): party-wide item grants.
- `/tp @p …` checkpoints (C16 bunker, C17 spawn intro, C11/C13 shaft teleporters).
- `gamemode survival/creative @p` toggle C07 (−615,−23,120): enter/exit challenge areas.
- Spawn platform at y 314 with player head avenue (185 heads) — shared lobby feel.
- 43 deaths with `doImmediateRespawn false` — respawn flow matters (CyberPixel.md: respawn at
  last activated terminal — terminal activation itself is server-side, not in the ZIP).

## Unknowns

- Actual player *usernames* mapping to UUID `286cf075-…` (no usercache.json).
- Whether other players ever joined (single stats set only; Bedrock/console cross-play not ruled out).
- Server software version/brand at save time (list shows history only).
- Whether `Bear_The_Boi` was a real session or decoration.

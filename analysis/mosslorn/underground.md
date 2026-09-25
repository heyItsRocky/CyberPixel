# Mosslorn — underground analysis

Derived from chunk scans (block classes below `surface-3`), block-entity depths, and raw block totals. Coordinates are exact block coords.

## Overworld

- Chunks scanned: 27761
- Air blocks below surface (carved spaces): **118,389,919** in 22,939 chunks with ≥256 such blocks
- Built blocks below surface: **18,034,150**
- Deepest built y: **-64** (highest below-surface built y: 315)
- Deep facilities (all built < y48): **2743 chunks**

- Hollow-space bbox: (-1536, -1104) → (1071, 1535)

### Deep-facility clusters (top 8)

- D1: 119 chunks, bbox (736, -832) → (959, -609)
- D2: 115 chunks, bbox (448, -976) → (687, -769)
- D3: 73 chunks, bbox (-1136, 464) → (-977, 639)
- D4: 66 chunks, bbox (-816, 1200) → (-657, 1407)
- D5: 63 chunks, bbox (528, -704) → (719, -465)
- D6: 61 chunks, bbox (816, 784) → (959, 975)
- D7: 57 chunks, bbox (496, 640) → (719, 783)
- D8: 55 chunks, bbox (-880, 720) → (-705, 943)

### Block-entity depth bands (y//16*16 → count)

| y band | BE count |
|---|---|
| -64 | 1,506 |
| -48 | 2,332 |
| -32 | 2,507 |
| -16 | 1,171 |
| 0 | 605 |
| 16 | 510 |
| 32 | 564 |
| 48 | 2,890 |
| 64 | 32,403 |
| 80 | 21,816 |
| 96 | 11,462 |
| 112 | 10,237 |
| 128 | 9,428 |
| 144 | 9,684 |
| 160 | 7,408 |
| 176 | 6,096 |
| 192 | 5,423 |
| 208 | 4,231 |
| 224 | 1,964 |
| 240 | 1,931 |
| 256 | 174 |
| 272 | 1,308 |
| 288 | 839 |
| 304 | 71 |

- Block entities below y=0: **7,516** — types: minecraft:sculk_sensor: 2226, minecraft:barrel: 976, minecraft:skull: 693, minecraft:chest: 647, minecraft:sculk_catalyst: 561, minecraft:mob_spawner: 466, minecraft:sign: 388, minecraft:end_portal: 313, minecraft:sculk_shrieker: 270, minecraft:bed: 232, DUMMY: 168, minecraft:banner: 116, minecraft:daylight_detector: 115, minecraft:furnace: 96, minecraft:command_block: 78, minecraft:dispenser: 63, minecraft:blast_furnace: 26, minecraft:brewing_stand: 24, minecraft:dropper: 12, minecraft:comparator: 11

### Notable block totals (underground-relevant)

- `minecraft:barrier`: 466,956
- `minecraft:barrel`: 60,219
- `minecraft:rail`: 32,589
- `minecraft:polished_blackstone_button`: 22,634
- `minecraft:powered_rail`: 9,051
- `minecraft:detector_rail`: 8,620
- `minecraft:observer`: 8,604
- `minecraft:stone_button`: 7,107
- `minecraft:lever`: 5,644
- `minecraft:piston`: 3,712
- `minecraft:chest`: 1,559
- `minecraft:spawner`: 935
- `minecraft:tnt`: 812
- `minecraft:redstone_block`: 167
- `minecraft:acacia_button`: 127
- `minecraft:sticky_piston`: 113
- `minecraft:command_block`: 79
- `minecraft:warped_button`: 64
- `minecraft:birch_button`: 52
- `minecraft:trapped_chest`: 16
- `minecraft:calibrated_sculk_sensor`: 8
- `minecraft:spruce_button`: 6
- `minecraft:chain_command_block`: 5
- `minecraft:repeating_command_block`: 4
- `minecraft:piston_head`: 4

## End dimension

- Chunks: 9822; below-surface built: 991,354; BE below y0: 0

Full data in `underground.json`.

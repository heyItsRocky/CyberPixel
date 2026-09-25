#!/usr/bin/env python3
"""Mosslorn world scanner: region files -> JSONL datasets + color grid.

Read-only scan of Minecraft 1.20.1 Anvil region/entity/POI files. Emits:
  summary.json, global_blocks.json, chunks.jsonl, be.jsonl,
  entities.jsonl, poi.jsonl, colorgrid.npz, color_table.json

Usage:
  scan_world.py --world <world_dir> --out <out_dir> [--dim region] [--limit N]
"""
import argparse
import collections
import glob
import io
import json
import os
import struct
import sys
import time
import zlib

import numpy as np

try:
    import nbtlib
except ImportError:
    sys.exit("nbtlib required: pip install nbtlib")

AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}

NATURAL = {
    "minecraft:stone", "minecraft:granite", "minecraft:polished_granite",
    "minecraft:diorite", "minecraft:polished_diorite", "minecraft:andesite",
    "minecraft:polished_andesite", "minecraft:deepslate", "minecraft:cobbled_deepslate",
    "minecraft:polished_deepslate", "minecraft:tuff", "minecraft:calcite",
    "minecraft:dripstone_block", "minecraft:smooth_basalt", "minecraft:mud",
    "minecraft:bedrock", "minecraft:obsidian", "minecraft:crying_obsidian",
    "minecraft:dirt", "minecraft:coarse_dirt", "minecraft:rooted_dirt",
    "minecraft:grass_block", "minecraft:podzol", "minecraft:mycelium",
    "minecraft:moss_block", "minecraft:hanging_roots",
    "minecraft:sand", "minecraft:red_sand", "minecraft:gravel", "minecraft:clay",
    "minecraft:suspicious_sand", "minecraft:suspicious_gravel", "minecraft:snow_block",
    "minecraft:powder_snow", "minecraft:grass", "minecraft:short_grass",
    "minecraft:tall_grass", "minecraft:fern", "minecraft:large_fern",
    "minecraft:dead_bush", "minecraft:seagrass", "minecraft:tall_seagrass",
    "minecraft:kelp", "minecraft:kelp_plant", "minecraft:sea_pickle",
    "minecraft:vine", "minecraft:cave_vines", "minecraft:cave_vines_plant",
    "minecraft:glow_lichen", "minecraft:spore_blossom", "minecraft:bamboo",
    "minecraft:bamboo_sapling", "minecraft:sugar_cane", "minecraft:cactus",
    "minecraft:pumpkin", "minecraft:melon", "minecraft:hay_block",
    "minecraft:dandelion", "minecraft:poppy", "minecraft:blue_orchid",
    "minecraft:allium", "minecraft:azure_bluet", "minecraft:red_tulip",
    "minecraft:orange_tulip", "minecraft:white_tulip", "minecraft:pink_tulip",
    "minecraft:oxeye_daisy", "minecraft:cornflower", "minecraft:lily_of_the_valley",
    "minecraft:wither_rose", "minecraft:large_dripleaf", "minecraft:small_dripleaf",
    "minecraft:big_dripleaf", "minecraft:big_dripleaf_stem",
    "minecraft:pointed_dripstone", "minecraft:lily_pad", "minecraft:crimson_fungus",
    "minecraft:warped_fungus", "minecraft:crimson_roots", "minecraft:warped_roots",
    "minecraft:nether_sprouts", "minecraft:twisting_vines", "minecraft:weeping_vines",
    "minecraft:chorus_plant", "minecraft:chorus_flower", "minecraft:water",
    "minecraft:lava", "minecraft:ice", "minecraft:packed_ice", "minecraft:blue_ice",
    "minecraft:snow", "minecraft:sandstone", "minecraft:chiseled_sandstone",
    "minecraft:cut_sandstone", "minecraft:smooth_sandstone",
    "minecraft:red_sandstone", "minecraft:smooth_red_sandstone",
    "minecraft:coal_ore", "minecraft:iron_ore", "minecraft:copper_ore",
    "minecraft:gold_ore", "minecraft:redstone_ore", "minecraft:lapis_ore",
    "minecraft:diamond_ore", "minecraft:emerald_ore", "minecraft:nether_gold_ore",
    "minecraft:nether_quartz_ore", "minecraft:ancient_debris",
    "minecraft:deepslate_coal_ore", "minecraft:deepslate_iron_ore",
    "minecraft:deepslate_copper_ore", "minecraft:deepslate_gold_ore",
    "minecraft:deepslate_redstone_ore", "minecraft:deepslate_lapis_ore",
    "minecraft:deepslate_diamond_ore", "minecraft:deepslate_emerald_ore",
    "minecraft:torchflower_crop", "minecraft:pitcher_crop", "minecraft:pink_petals",
    "minecraft:moss_carpet", "minecraft:brown_mushroom", "minecraft:red_mushroom",
    "minecraft:mushroom_stem",
    # geodes / cave features / ancient-city geology
    "minecraft:amethyst_block", "minecraft:budding_amethyst",
    "minecraft:amethyst_cluster", "minecraft:small_amethyst_bud",
    "minecraft:medium_amethyst_bud", "minecraft:large_amethyst_bud",
    "minecraft:bubble_column", "minecraft:magma_block", "minecraft:cobweb",
    "minecraft:raw_copper_block", "minecraft:raw_iron_block",
    "minecraft:raw_gold_block", "minecraft:sculk", "minecraft:sculk_vein",
    "minecraft:sculk_catalyst", "minecraft:sculk_shrieker", "minecraft:sculk_sensor",
    "minecraft:sculk_wool", "minecraft:reinforced_deepslate",
}


def is_natural(name: str) -> bool:
    if name in NATURAL or name in AIR:
        return True
    n = name.split(":", 1)[-1]
    return (n.endswith("_leaves") or n.endswith("_log") or n.endswith("_wood")
            or n.endswith("_sapling") or n.endswith("_flower"))


# approximate block colors for top-down rendering (visual approximation only)
COLORS = {
    "minecraft:water": (63, 118, 228), "minecraft:lava": (212, 91, 18),
    "minecraft:grass_block": (124, 189, 107), "minecraft:dirt": (151, 109, 77),
    "minecraft:coarse_dirt": (119, 85, 58), "minecraft:podzol": (111, 91, 62),
    "minecraft:mycelium": (91, 85, 85), "minecraft:moss_block": (89, 109, 45),
    "minecraft:moss_carpet": (89, 109, 45), "minecraft:sand": (219, 211, 160),
    "minecraft:red_sand": (169, 88, 33), "minecraft:gravel": (132, 132, 132),
    "minecraft:clay": (160, 166, 176), "minecraft:stone": (127, 127, 127),
    "minecraft:deepslate": (80, 80, 80), "minecraft:cobbled_deepslate": (85, 85, 85),
    "minecraft:tuff": (108, 108, 98), "minecraft:calcite": (223, 223, 221),
    "minecraft:bedrock": (60, 60, 60), "minecraft:snow": (255, 255, 255),
    "minecraft:snow_block": (240, 248, 255), "minecraft:ice": (160, 160, 255),
    "minecraft:packed_ice": (141, 180, 250), "minecraft:blue_ice": (116, 167, 253),
    "minecraft:andesite": (136, 136, 138), "minecraft:diorite": (188, 188, 188),
    "minecraft:granite": (149, 103, 85), "minecraft:dirt_path": (130, 107, 64),
    "minecraft:farmland": (139, 87, 42), "minecraft:obsidian": (20, 18, 30),
    "minecraft:mud": (60, 46, 40), "minecraft:grass": (124, 189, 107),
    "minecraft:short_grass": (124, 189, 107), "minecraft:tall_grass": (124, 189, 107),
    "minecraft:oak_planks": (160, 117, 62), "minecraft:spruce_planks": (114, 84, 48),
    "minecraft:birch_planks": (196, 178, 128), "minecraft:jungle_planks": (151, 110, 71),
    "minecraft:acacia_planks": (168, 90, 50), "minecraft:dark_oak_planks": (66, 43, 20),
    "minecraft:mangrove_planks": (117, 54, 37), "minecraft:crimson_planks": (101, 48, 59),
    "minecraft:warped_planks": (57, 44, 62), "minecraft:bamboo_planks": (193, 171, 91),
    "minecraft:oak_leaves": (60, 110, 50), "minecraft:spruce_leaves": (45, 90, 60),
    "minecraft:birch_leaves": (107, 141, 60), "minecraft:jungle_leaves": (52, 120, 40),
    "minecraft:acacia_leaves": (70, 120, 45), "minecraft:dark_oak_leaves": (40, 90, 35),
    "minecraft:mangrove_leaves": (46, 100, 45), "minecraft:azalea_leaves": (80, 130, 60),
    "minecraft:cherry_leaves": (229, 172, 194), "minecraft:oak_log": (107, 83, 48),
    "minecraft:spruce_log": (58, 37, 16), "minecraft:birch_log": (196, 178, 128),
    "minecraft:jungle_log": (87, 68, 26), "minecraft:acacia_log": (103, 96, 86),
    "minecraft:dark_oak_log": (46, 29, 10), "minecraft:mangrove_log": (84, 44, 31),
    "minecraft:stone_bricks": (122, 122, 122), "minecraft:bricks": (150, 97, 83),
    "minecraft:cobblestone": (110, 110, 110), "minecraft:mossy_cobblestone": (90, 108, 70),
    "minecraft:glass": (200, 220, 235), "minecraft:glass_pane": (200, 220, 235),
    "minecraft:chest": (140, 105, 60), "minecraft:barrel": (140, 105, 60),
    "minecraft:crafting_table": (150, 117, 62), "minecraft:furnace": (110, 110, 110),
    "minecraft:hay_block": (168, 144, 50), "minecraft:glowstone": (248, 218, 123),
    "minecraft:sea_lantern": (172, 217, 199), "minecraft:iron_block": (220, 220, 220),
    "minecraft:gold_block": (249, 236, 79), "minecraft:copper_block": (194, 107, 79),
    "minecraft:oxidized_copper": (82, 171, 152),
    "minecraft:crimson_stem": (101, 48, 59), "minecraft:warped_stem": (57, 44, 62),
}
_PALETTE = {
    "white": (207, 213, 214), "orange": (216, 127, 51), "magenta": (178, 76, 216),
    "light_blue": (102, 153, 216), "yellow": (229, 229, 51), "lime": (127, 204, 25),
    "pink": (242, 178, 203), "gray": (76, 76, 76), "light_gray": (153, 153, 153),
    "cyan": (76, 127, 153), "purple": (127, 63, 178), "blue": (51, 76, 178),
    "brown": (102, 76, 51), "green": (102, 127, 51), "red": (153, 51, 51),
    "black": (25, 25, 25),
}
for _c, _rgb in _PALETTE.items():
    COLORS[f"minecraft:{_c}_concrete"] = _rgb
    COLORS[f"minecraft:{_c}_wool"] = tuple(min(255, int(v * 0.92) + 8) for v in _rgb)
    COLORS[f"minecraft:{_c}_terracotta"] = tuple(int(v * 0.8) for v in _rgb)
    COLORS[f"minecraft:{_c}_stained_glass"] = tuple(int(v * 0.8 + 50) for v in _rgb)
    COLORS[f"minecraft:{_c}_glazed_terracotta"] = _rgb
    COLORS[f"minecraft:{_c}_carpet"] = _rgb
    COLORS[f"minecraft:{_c}_bed"] = _rgb
for _base, _rgb in {
    "stone_bricks": (122, 122, 122), "deepslate_bricks": (70, 70, 70),
    "deepslate_tiles": (55, 55, 55), "polished_blackstone": (53, 48, 54),
    "blackstone": (42, 36, 43), "smooth_stone": (160, 160, 160),
    "quartz_block": (235, 231, 225), "prismarine": (99, 156, 151),
    "cut_copper": (194, 107, 79), "lamp": (249, 236, 134),
    "lantern": (220, 200, 140), "torch": (220, 200, 140),
    "rail": (140, 130, 90), "scaffolding": (170, 160, 100),
}.items():
    COLORS.setdefault(f"minecraft:{_base}", _rgb)
_DEFAULT_RGB = (140, 140, 140)
_NATURAL_FALLBACK = (100, 140, 90)
_air_color = (20, 30, 40)


def color_for(name: str, natural: bool) -> tuple:
    rgb = COLORS.get(name)
    if rgb:
        return rgb
    n = name.split(":", 1)[-1]
    for suffix, rgb in COLORS.items():
        if n.endswith(suffix.split(":", 1)[-1]):
            return rgb
    return _NATURAL_FALLBACK if natural else _DEFAULT_RGB


def iter_chunks(path):
    """Yield (slot_index, nbtlib.File) for each present chunk."""
    with open(path, "rb") as fh:
        data = fh.read()
    hdr = data[:8096]
    if len(hdr) < 4096:
        return
    for i in range(1024):
        b = hdr[i * 4:i * 4 + 4]
        if len(b) < 4:
            break
        off = (b[0] << 16) | (b[1] << 8) | b[2]
        if off == 0:
            continue
        o = off * 4096
        if o + 5 > len(data):
            continue
        ln = struct.unpack(">I", data[o:o + 4])[0]
        comp = data[o + 4]
        payload = data[o + 5:o + 4 + ln]
        if len(payload) != ln - 1:
            continue
        try:
            if comp == 2:
                raw = zlib.decompress(payload)
            elif comp == 1:
                raw = zlib.decompress(payload, 16 + zlib.MAX_WBITS)
            elif comp == 3:
                raw = payload
            else:
                continue
            yield i, nbtlib.File.from_fileobj(io.BytesIO(raw))
        except Exception:
            continue


def unpack_section(block_states):
    """Return (arr3 int16 (16,16,16) palette indices, names list)."""
    palette = block_states.get("palette")
    if palette is None:
        return np.zeros((16, 16, 16), dtype=np.int16), ["minecraft:air"]
    names = [str(p.get("Name")) for p in palette]
    if len(names) == 1:
        return np.zeros((16, 16, 16), dtype=np.int16), names
    data = block_states.get("data")
    if data is None:
        return np.zeros((16, 16, 16), dtype=np.int16), names
    bits = max(4, (len(names) - 1).bit_length())
    arr = np.fromiter((int(x) & 0xFFFFFFFFFFFFFFFF for x in data),
                      dtype=np.uint64, count=len(data))
    per_long = 64 // bits
    j = np.arange(4096, dtype=np.int64)
    shift = ((j % per_long) * bits).astype(np.uint64)
    vals = ((arr[j // per_long] >> shift)
            & np.uint64((1 << bits) - 1)).astype(np.int16)
    return vals.reshape(16, 16, 16), names  # (y, z, x)


_cls_cache = {}


def classify(name):
    c = _cls_cache.get(name)
    if c is None:
        c = "air" if name in AIR else ("natural" if is_natural(name) else "built")
        _cls_cache[name] = c
    return c


# blocks that float above the mineral surface (vegetation, fluids, thin layers)
NONSOLID_EXACT = {
    "minecraft:water", "minecraft:lava", "minecraft:bubble_column",
    "minecraft:snow", "minecraft:powder_snow", "minecraft:cobweb",
    "minecraft:grass", "minecraft:short_grass", "minecraft:tall_grass",
    "minecraft:fern", "minecraft:large_fern", "minecraft:dead_bush",
    "minecraft:vine", "minecraft:cave_vines", "minecraft:cave_vines_plant",
    "minecraft:glow_lichen", "minecraft:seagrass", "minecraft:tall_seagrass",
    "minecraft:kelp", "minecraft:kelp_plant", "minecraft:lily_pad",
    "minecraft:hanging_roots", "minecraft:spore_blossom", "minecraft:pink_petals",
    "minecraft:moss_carpet", "minecraft:torchflower_crop",
    "minecraft:pitcher_crop", "minecraft:sugar_cane", "minecraft:bamboo",
    "minecraft:bamboo_sapling", "minecraft:dandelion", "minecraft:poppy",
    "minecraft:blue_orchid", "minecraft:allium", "minecraft:azure_bluet",
    "minecraft:red_tulip", "minecraft:orange_tulip", "minecraft:white_tulip",
    "minecraft:pink_tulip", "minecraft:oxeye_daisy", "minecraft:cornflower",
    "minecraft:lily_of_the_valley", "minecraft:wither_rose",
    "minecraft:brown_mushroom", "minecraft:red_mushroom",
    "minecraft:chorus_plant", "minecraft:chorus_flower",
    "minecraft:crimson_roots", "minecraft:warped_roots",
    "minecraft:nether_sprouts", "minecraft:twisting_vines",
    "minecraft:weeping_vines", "minecraft:crimson_fungus",
    "minecraft:warped_fungus", "minecraft:rail", "minecraft:powered_rail",
    "minecraft:detector_rail", "minecraft:activator_rail",
    "minecraft:redstone_wire", "minecraft:tripwire", "minecraft:tripwire_hook",
    "minecraft:lever", "minecraft:torch", "minecraft:wall_torch",
    "minecraft:redstone_torch", "minecraft:soul_torch", "minecraft:soul_fire",
    "minecraft:fire", "minecraft:soul_fire", "minecraft:campfire",
    "minecraft:soul_campfire", "minecraft:cobweb", "minecraft:string",
    "minecraft:large_dripleaf", "minecraft:large_dripleaf_stem",
    "minecraft:small_dripleaf", "minecraft:big_dripleaf",
    "minecraft:big_dripleaf_stem", "minecraft:pointed_dripstone",
    "minecraft:sculk_vein", "minecraft:water_cauldron", "minecraft:lava_cauldron",
    "minecraft:powder_snow_cauldron",
}
NONSOLID_SUFFIX = ("_leaves", "_sapling", "_vines", "_carpet", "_button",
                   "_pressure_plate", "_rail", "_torch", "_sign", "_banner",
                   "_flower", "_tulip", "_fern", "_crop")


def is_solid(name: str) -> bool:
    if name in AIR or name in NONSOLID_EXACT:
        return False
    n = name.split(":", 1)[-1]
    return not n.endswith(NONSOLID_SUFFIX)


def process_chunk(c, dim_name, color_rgb, color_registry):
    """Returns (chunk_row, block_entity_rows, struct_refs, color_grid_16x16)."""
    cx = int(c.get("xPos", 0))
    cz = int(c.get("zPos", 0))
    status = str(c.get("Status", "?"))
    inhabited = int(c.get("InhabitedTime", 0))
    y_pos = int(c.get("yPos", -4))

    sections = c.get("sections") or c.get("Sections") or []
    cls_total = {"air": 0, "natural": 0, "built": 0}
    dec = []  # (base_y, arr3, names, cls_arr, is_air_p, is_built_p, is_solid_p)
    for s in sections:
        if "block_states" not in s:
            continue
        base_y = int(s.get("Y", 0)) * 16
        arr3, names = unpack_section(s["block_states"])
        cls = [classify(n) for n in names]
        is_air_p = np.array([x == "air" for x in cls], dtype=bool)
        is_built_p = np.array([x == "built" for x in cls], dtype=bool)
        is_solid_p = np.array([is_solid(n) for n in names], dtype=bool)
        dec.append((base_y, arr3, names, cls, is_air_p, is_built_p, is_solid_p))
    dec.sort(key=lambda t: -t[0])

    # pass 1: counts + visual tops (for map color)
    built_counts = collections.Counter()
    top_y = np.full((16, 16), -9999, dtype=np.int32)
    top_idx = np.full((16, 16), -1, dtype=np.int16)
    filled = np.zeros((16, 16), dtype=bool)
    # mineral surface tops (for underground math)
    sol_y = np.full((16, 16), -9999, dtype=np.int32)
    sol_filled = np.zeros((16, 16), dtype=bool)
    for base_y, arr3, names, cls, is_air_p, is_built_p, is_solid_p in dec:
        # counts
        flat = arr3.reshape(-1)
        bc = np.bincount(flat.astype(np.int64), minlength=len(names))
        for i in np.nonzero(bc)[0]:
            cls_total[cls[i]] += int(bc[i])
            if cls[i] == "built":
                built_counts[names[i]] += int(bc[i])
        # visual tops (y desc)
        for yy in range(15, -1, -1):
            if filled.all() and sol_filled.all():
                break
            nonair = ~is_air_p[arr3[yy]]          # (z, x)
            newly = (~filled) & nonair
            if newly.any():
                ys, xs = np.nonzero(newly)
                top_y[ys, xs] = base_y + yy
                top_idx[ys, xs] = arr3[yy, ys, xs]
                filled[ys, xs] = True
            if not sol_filled.all():
                newsolid = (~sol_filled) & is_solid_p[arr3[yy]]
                if newsolid.any():
                    ys, xs = np.nonzero(newsolid)
                    sol_y[ys, xs] = base_y + yy
                    sol_filled[ys, xs] = True

    # pass 2: below-surface relative to mineral surface (y < sol_surf - 3)
    below_mask = sol_filled & (sol_y > -9999)
    cutoff = sol_y - 3                              # exclusive top of below-zone
    built_below = 0
    below_air = 0
    bsum = np.zeros(3, dtype=np.int64)
    by_min = None
    by_max = None
    for base_y, arr3, names, cls, is_air_p, is_built_p, is_solid_p in dec:
        # local cutoff per column (only where column filled)
        lo = cutoff - base_y                        # (z, x) exclusive local y
        if not (lo > 0).any():
            continue
        yy = np.arange(16).reshape(16, 1, 1)
        colmask = (yy < lo[None, :, :]) & below_mask[None, :, :]
        if is_air_p.any():
            a3 = is_air_p[arr3]
            below_air += int((a3 & colmask).sum())
        if is_built_p.any():
            b3 = is_built_p[arr3] & colmask
            if b3.any():
                ys, zs, xs = np.nonzero(b3)
                ay = ys + base_y
                built_below += len(ys)
                bsum[0] += int(xs.sum())
                bsum[1] += int(ay.sum())
                bsum[2] += int(zs.sum())
                ymn, ymx = int(ay.min()), int(ay.max())
                by_min = ymn if by_min is None else min(by_min, ymn)
                by_max = ymx if by_max is None else max(by_max, ymx)

    # terrain / water stats
    solid = top_idx >= 0
    surf_vals = top_y[solid]
    surf_mean = round(float(surf_vals.mean()), 1) if solid.any() else None
    surf_min = int(surf_vals.min()) if solid.any() else None
    surf_max = int(surf_vals.max()) if solid.any() else None
    # top block names for water/histogram stats
    top_names = {}
    for base_y, arr3, names, cls, is_air_p, is_built_p, is_solid_p in dec:
        for lz in range(16):
            for lx in range(16):
                if top_idx[lz, lx] >= 0 and top_y[lz, lx] >= base_y and (lz, lx) not in top_names:
                    li = int(top_idx[lz, lx])
                    if li < len(names):
                        top_names[(lz, lx)] = names[li]
    water_top = sum(1 for n in top_names.values() if n == "minecraft:water")
    top_hist = collections.Counter(top_names.values()).most_common(6)
    sol_vals = sol_y[sol_filled & (sol_y > -9999)]
    surfsol_mean = round(float(sol_vals.mean()), 1) if sol_vals.size else None

    # color grid
    grid = np.full((16, 16), 251, dtype=np.uint8)
    color_rgb.setdefault(251, _DEFAULT_RGB)
    for (lz, lx), nm in top_names.items():
        cid = color_registry.get(nm)
        if cid is None:
            if max(color_registry.values(), default=0) < 245:
                cid = max(color_registry.values(), default=-1) + 1
            else:
                cid = 251
            color_registry[nm] = cid
            color_rgb[cid] = color_for(nm, classify(nm) == "natural")
        grid[lz, lx] = cid

    # block entities
    bes = c.get("block_entities") or c.get("TileEntities") or []
    be_rows = []
    be_types = collections.Counter()
    for b in bes:
        bid = str(b.get("id", "?"))
        be_types[bid] += 1
        rec = {"dim": dim_name, "cx": cx, "cz": cz,
               "x": int(b.get("x", 0)), "y": int(b.get("y", 0)),
               "z": int(b.get("z", 0)), "id": bid}
        for k_src, k_dst in (("loot_table", "loot"), ("LootTable", "loot")):
            if k_src in b:
                rec[k_dst] = str(b[k_src])
        if "Command" in b:
            rec["cmd"] = str(b["Command"])[:2000]
        if "Items" in b:
            items = b.get("Items") or []
            rec["items"] = len(items)
            rec["item_ids"] = [str(it.get("id")) for it in list(items)[:12]
                               if isinstance(it, dict)]
        if "messages" in b:
            rec["sign"] = [str(m)[:300] for m in b.get("messages", [])]
        if "front_text" in b and isinstance(b["front_text"], dict):
            rec["sign"] = [str(m)[:300] for m in (b["front_text"].get("messages") or [])]
        if "back_text" in b and isinstance(b["back_text"], dict):
            rec["sign_back"] = [str(m)[:300] for m in (b["back_text"].get("messages") or [])]
        if "Item" in b and isinstance(b["Item"], dict):
            it = b["Item"]
            rec["frame_item"] = str(it.get("id"))
            if str(it.get("id")) in ("minecraft:written_book", "minecraft:enchanted_book"):
                tag = it.get("tag") or it.get("components") or {}
                if isinstance(tag, dict):
                    rec["book_title"] = str(tag.get("title", ""))[:100]
                    rec["book_author"] = str(tag.get("author", ""))[:60]
                    pages = tag.get("pages") or []
                    rec["book_pages"] = [str(p)[:400] for p in list(pages)[:16]]
        if "SpawnData" in b:
            sd = b["SpawnData"]
            rec["spawn"] = str(sd.get("entity") or sd.get("id") or "")[:80]
        if "SkullOwner" in b:
            rec["skull"] = str(b["SkullOwner"])[:80]
        if "Color" in b:
            rec["color"] = int(b["Color"])
        if "CustomName" in b:
            rec["name"] = str(b["CustomName"])[:200]
        be_rows.append(rec)

    # structure references
    struct_refs = []
    st = c.get("structures")
    if st:
        starts = st.get("starts") or {}
        for sname, sv in starts.items():
            items = sv if isinstance(sv, list) else [sv]
            for s in items:
                if isinstance(s, dict) and "boundingBox" in s:
                    bb = s["boundingBox"]
                    struct_refs.append({"name": str(sname), "cx": cx, "cz": cz,
                                        "bb": {k: int(bb[k]) for k in bb}})

    row = {
        "dim": dim_name, "cx": cx, "cz": cz, "status": status, "inh": inhabited,
        "surf": surf_mean, "surf_min": surf_min, "surf_max": surf_max,
        "surfsol": surfsol_mean,
        "built": int(sum(built_counts.values())),
        "built_top": [[n, int(v)] for n, v in built_counts.most_common(12)],
        "built_below": built_below, "below_air": below_air,
        "bmin": by_min, "bmax": by_max,
        "bcent": [int(bsum[0]), int(bsum[1]), int(bsum[2])] if built_below else None,
        "top": [[n, int(v)] for n, v in top_hist],
        "water_top": water_top,
        "be": dict(be_types),
    }
    return row, be_rows, struct_refs, grid, built_counts, cls_total


def scan_dimension(world, dim_rel, out_dir, limit=None):
    reg_dir = os.path.join(world, dim_rel)
    files = sorted(glob.glob(os.path.join(reg_dir, "*.mca")))
    if not files:
        print(f"no region files in {reg_dir}")
        return None
    dim_name = "overworld" if dim_rel == "region" else dim_rel.split("/")[0]

    global_counts = collections.Counter()
    class_counts = {"air": 0, "natural": 0, "built": 0}
    chunk_rows, be_rows, struct_refs = [], [], []
    color_coords, color_grid = [], []
    status_hist = collections.Counter()
    color_registry = {}
    color_rgb = {251: _DEFAULT_RGB, 252: _air_color, 253: (255, 0, 255)}
    errors = 0
    chunks_seen = 0
    t0 = time.time()

    for fi, path in enumerate(files):
        if limit and fi >= limit:
            break
        mname = os.path.basename(path)
        rx = int(mname.split(".")[1])
        rz = int(mname.split(".")[2])
        for slot, c in iter_chunks(path):
            chunks_seen += 1
            try:
                if "xPos" not in c:
                    c["xPos"] = nbtlib.Int(rx * 32 + slot % 32)
                    c["zPos"] = nbtlib.Int(rz * 32 + slot // 32)
                row, berefs, srefs, grid, bfull, ctot = process_chunk(
                    c, dim_name, color_rgb, color_registry)
                chunk_rows.append(row)
                be_rows.extend(berefs)
                struct_refs.extend(srefs)
                global_counts.update(bfull)
                for k in class_counts:
                    class_counts[k] += ctot[k]
                color_coords.append((row["cx"], row["cz"]))
                color_grid.append(grid)
                status_hist[row["status"]] += 1
            except Exception as e:
                errors += 1
                if errors < 8:
                    print(f"chunk error {mname} slot {slot}: {e}", file=sys.stderr)
                continue
        if (fi + 1) % 25 == 0 or fi + 1 == len(files):
            rate = chunks_seen / max(0.001, time.time() - t0)
            print(f"  [{dim_name}] {fi+1}/{len(files)} regions, {chunks_seen} chunks, "
                  f"{rate:.0f} chunks/s", flush=True)

    dim_out = out_dir if dim_name == "overworld" else os.path.join(out_dir, dim_name)
    os.makedirs(dim_out, exist_ok=True)
    with open(os.path.join(dim_out, "global_blocks.json"), "w") as fh:
        json.dump(dict(global_counts.most_common()), fh)
    with open(os.path.join(dim_out, "chunks.jsonl"), "w") as fh:
        for r in chunk_rows:
            fh.write(json.dumps(r) + "\n")
    with open(os.path.join(dim_out, "be.jsonl"), "w") as fh:
        for r in be_rows:
            fh.write(json.dumps(r) + "\n")
    np.savez_compressed(
        os.path.join(dim_out, "colorgrid.npz"),
        coords=np.array(color_coords, dtype=np.int32),
        grid=np.array(color_grid, dtype=np.uint8),
        names=np.array(list(color_registry.keys()), dtype=object),
        ids=np.array(list(color_registry.values()), dtype=np.int16))
    with open(os.path.join(dim_out, "color_table.json"), "w") as fh:
        json.dump({str(k): list(v) for k, v in color_rgb.items()}, fh)

    xs = [c[0] for c in color_coords]
    zs = [c[1] for c in color_coords]
    summary = {
        "dim": dim_name, "regions": len(files), "chunks": chunks_seen, "errors": errors,
        "bounds_chunk": {"minx": min(xs, default=0), "maxx": max(xs, default=0),
                         "minz": min(zs, default=0), "maxz": max(zs, default=0)},
        "bounds_block": {"minx": min(xs, default=0) * 16,
                         "maxx": (max(xs, default=0) + 1) * 16 - 1,
                         "minz": min(zs, default=0) * 16,
                         "maxz": (max(zs, default=0) + 1) * 16 - 1},
        "status_hist": dict(status_hist),
        "class_counts": class_counts,
        "block_entities": len(be_rows),
        "structure_refs": struct_refs[:600],
        "elapsed_s": round(time.time() - t0, 1),
    }
    with open(os.path.join(dim_out, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(f"[{dim_name}] done: {chunks_seen} chunks, {len(be_rows)} block entities, "
          f"{errors} errors, {summary['elapsed_s']}s")
    return summary


def scan_entities(world, dim_rel, out_dir):
    rel = "entities" if dim_rel == "region" else dim_rel[:-len("region")] + "entities"
    ent_dir = os.path.join(world, rel)
    files = sorted(glob.glob(os.path.join(ent_dir, "*.mca")))
    if not files:
        return
    dim_name = "overworld" if dim_rel == "region" else dim_rel.split("/")[0]
    dim_out = out_dir if dim_name == "overworld" else os.path.join(out_dir, dim_name)
    os.makedirs(dim_out, exist_ok=True)
    notable_ids = {"minecraft:villager", "minecraft:painting", "minecraft:item_frame",
                   "minecraft:glow_item_frame", "minecraft:armor_stand",
                   "minecraft:minecart", "minecraft:chest_minecart",
                   "minecraft:hopper_minecart", "minecraft:command_block_minecart",
                   "minecraft:player", "minecraft:boat", "minecraft:shulker",
                   "minecraft:iron_golem", "minecraft:snow_golem",
                   "minecraft:wandering_trader", "minecraft:allay",
                   "minecraft:cat", "minecraft:rabbit", "minecraft:parrot"}
    total = collections.Counter()
    rows = 0
    with open(os.path.join(dim_out, "entities.jsonl"), "w") as fh:
        for path in files:
            mname = os.path.basename(path)
            rx = int(mname.split(".")[1]); rz = int(mname.split(".")[2])
            for slot, c in iter_chunks(path):
                pos = c.get("Position")
                if pos is not None:
                    cx, cz = int(pos[0]), int(pos[1])
                else:
                    cx, cz = rx * 32 + slot % 32, rz * 32 + slot // 32
                ents = c.get("Entities") or c.get("entities") or []
                if not ents:
                    continue
                cnt = collections.Counter()
                notable = []
                for e in ents:
                    eid = str(e.get("id", "?"))
                    cnt[eid] += 1
                    total[eid] += 1
                    if eid in notable_ids and len(notable) < 40:
                        p = e.get("Pos")
                        if p:
                            row = [eid, round(float(p[0]), 1), int(float(p[1])),
                                   round(float(p[2]), 1)]
                            if eid.endswith("item_frame"):
                                it = e.get("Item") or {}
                                if isinstance(it, dict):
                                    info = {"id": str(it.get("id", "?"))}
                                    if info["id"] in ("minecraft:written_book",
                                                      "minecraft:enchanted_book"):
                                        tag = it.get("tag") or it.get("components") or {}
                                        if isinstance(tag, dict):
                                            info["title"] = str(tag.get("title", ""))[:120]
                                            info["author"] = str(tag.get("author", ""))[:60]
                                            info["pages"] = [str(x)[:600] for x in
                                                             list(tag.get("pages") or [])[:40]]
                                    row.append(info)
                            notable.append(row)
                rows += 1
                fh.write(json.dumps({"dim": dim_name, "cx": cx, "cz": cz,
                                     "counts": dict(cnt), "notable": notable}) + "\n")
    with open(os.path.join(dim_out, "entity_totals.json"), "w") as fh:
        json.dump(dict(total.most_common()), fh, indent=1)
    print(f"[{dim_name}] entities: {rows} chunk rows, {sum(total.values())} entities")


def scan_poi(world, out_dir, dim_rel="poi"):
    files = sorted(glob.glob(os.path.join(world, dim_rel, "*.mca")))
    if not files:
        return
    dim_name = "overworld" if dim_rel == "poi" else dim_rel.split("/")[0]
    dim_out = out_dir if dim_name == "overworld" else os.path.join(out_dir, dim_name)
    os.makedirs(dim_out, exist_ok=True)
    totals = collections.Counter()
    rows = 0
    with open(os.path.join(dim_out, "poi.jsonl"), "w") as fh:
        for path in files:
            mname = os.path.basename(path)
            rx = int(mname.split(".")[1]); rz = int(mname.split(".")[2])
            for slot, c in iter_chunks(path):
                cx = rx * 32 + slot % 32
                cz = rz * 32 + slot // 32
                secs = c.get("Sections") or c.get("sections") or {}
                it = secs.items() if isinstance(secs, dict) else enumerate(secs)
                for _sy, s in it:
                    for rec in (s.get("Records") or []):
                        p = rec.get("pos")
                        t = str(rec.get("type", "?"))
                        totals[t] += 1
                        rows += 1
                        fh.write(json.dumps({
                            "cx": cx, "cz": cz, "type": t,
                            "x": int(p[0]), "y": int(p[1]),
                            "z": int(p[2])}) + "\n")
    with open(os.path.join(dim_out, "poi_totals.json"), "w") as fh:
        json.dump(dict(totals.most_common()), fh, indent=1)
    print(f"[{dim_name}] POI: {rows} records, types: {dict(totals)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dims", default="region")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--skip-entities", action="store_true")
    ap.add_argument("--skip-poi", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    dims = [d.strip() for d in args.dims.split(",")]
    for dim in dims:
        print(f"== scanning {dim} ==")
        scan_dimension(args.world, dim, args.out, args.limit)
    if not args.skip_entities:
        for dim in dims:
            scan_entities(args.world, dim, args.out)
    if not args.skip_poi:
        for dim in dims:
            scan_poi(args.world, args.out,
                     dim if dim != "region" else "poi")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render top-down maps from scan colorgrid.npz + color_table.json.

Outputs: world-overview.png (full res, cropped to generated chunks),
         world-overview-small.png (~1400px wide).

Usage: render_maps.py --scan <scan_dir> --out <png_dir>
"""
import argparse
import json
import os

import numpy as np
from PIL import Image


def load_dim(scan_dir, sub=""):
    d = os.path.join(scan_dir, sub) if sub else scan_dir
    npz = os.path.join(d, "colorgrid.npz")
    if not os.path.exists(npz):
        return None
    z = np.load(npz, allow_pickle=True)
    with open(os.path.join(d, "color_table.json")) as fh:
        table = {int(k): tuple(v) for k, v in json.load(fh).items()}
    return z["coords"], z["grid"], table


def render(coords, grid, table, bg=(14, 22, 32)):
    min_cx, max_cx = coords[:, 0].min(), coords[:, 0].max()
    min_cz, max_cz = coords[:, 1].min(), coords[:, 1].max()
    w = (int(max_cx) - int(min_cx) + 1) * 16
    h = (int(max_cz) - int(min_cz) + 1) * 16
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = bg
    lut = np.zeros((256, 3), dtype=np.uint8)
    for cid, rgb in table.items():
        lut[cid & 0xFF] = rgb
    for (cx, cz), g in zip(coords, grid):
        ox = (int(cx) - int(min_cx)) * 16
        oz = (int(cz) - int(min_cz)) * 16
        img[oz:oz + 16, ox:ox + 16] = lut[g]
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for sub, name in (("", "world-overworld"), ("DIM1", "world-end")):
        loaded = load_dim(args.scan, sub)
        if not loaded:
            print(f"skip {sub or 'overworld'}: no colorgrid")
            continue
        coords, grid, table = loaded
        img = render(coords, grid, table)
        full = os.path.join(args.out, f"{name}-overview.png")
        Image.fromarray(img).save(full, optimize=True)
        import math
        scale = max(1, math.ceil(img.shape[1] / 1400))
        small = Image.fromarray(img).resize(
            (img.shape[1] // scale, img.shape[0] // scale), Image.BILINEAR)
        small.save(os.path.join(args.out, f"{name}-overview-small.png"), optimize=True)
        print(f"{name}: {img.shape[1]}x{img.shape[0]} -> saved "
              f"{os.path.getsize(full)//1024} KiB full, "
              f"{os.path.getsize(os.path.join(args.out, name+'-overview-small.png'))//1024} KiB small")


if __name__ == "__main__":
    main()

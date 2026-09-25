#!/usr/bin/env python3
"""Crop overview map around notable locations -> screenshots/.

Inputs: overview PNG (from render_maps), locations.json, terminal_candidates.json
Outputs: screenshots/site_*.png, cmd_*.png, spawner_*.png (with center crosshair)

Usage: render_crops.py --scan <scan_dir> --overview <png> --locations <loc.json>
       --terminals <term.json> --out <screenshots_dir>
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--overview", required=True)
    ap.add_argument("--locations", required=True)
    ap.add_argument("--terminals", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--top", type=int, default=14)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    z = np.load(os.path.join(args.scan, "colorgrid.npz"), allow_pickle=True)
    coords = z["coords"]
    min_cx, min_cz = int(coords[:, 0].min()), int(coords[:, 1].min())
    org_x, org_z = min_cx * 16, min_cz * 16
    img = Image.open(args.overview).convert("RGB")

    def crop(name, bx, bz, size):
        px, pz = bx - org_x, bz - org_z
        half = size // 2
        box = (px - half, pz - half, px + half, pz + half)
        if box[0] < 0 or box[1] < 0 or box[2] > img.width or box[3] > img.height:
            half = min(half, px, pz, img.width - px, img.height - pz)
            if half < 64:
                return
            box = (px - half, pz - half, px + half, pz + half)
        c = img.crop(box)
        dr = ImageDraw.Draw(c)
        cx, cy = half, half
        dr.line([(cx - 8, cy), (cx + 8, cy)], fill=(255, 0, 0), width=2)
        dr.line([(cx, cy - 8), (cx, cy + 8)], fill=(255, 0, 0), width=2)
        c.save(os.path.join(args.out, f"{name}.png"), optimize=True)

    locs = json.load(open(args.locations))
    ow = locs.get("overworld", {}).get("sites", [])
    for s in ow[:args.top]:
        crop(f"site_{s['id']}", s["center"][0], s["center"][1], args.size)
    if args.terminals:
        t = json.load(open(args.terminals))
        for i, g in enumerate(t.get("command_clusters", [])[:8], 1):
            c = g["center"]
            crop(f"cmd_C{i:02d}_n{g['count']}", c[0], c[2], args.size)
        for i, g in enumerate(t.get("spawner_clusters", [])[:8], 1):
            c = g["center"]
            crop(f"spawner_S{i:02d}_n{g['count']}", c[0], c[2], args.size)
    print(f"cropped {len(os.listdir(args.out))} images -> {args.out}")


if __name__ == "__main__":
    main()

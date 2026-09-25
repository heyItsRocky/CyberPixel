#!/usr/bin/env python3
"""Underground analysis: hollow spaces, depth profile, deep facilities.

Inputs: chunks.jsonl, be.jsonl, global_blocks.json (per dim)
Outputs: underground.md + underground.json

Usage: analyze_underground.py --scan <scan_dir> --out <out_dir>
"""
import argparse
import collections
import json
import os


def load_jsonl(path):
    rows = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def band(y):
    return (int(y) // 16) * 16


def analyze_dim(scan_dir, sub=""):
    d = os.path.join(scan_dir, sub) if sub else scan_dir
    chunks = load_jsonl(os.path.join(d, "chunks.jsonl"))
    bes = load_jsonl(os.path.join(d, "be.jsonl"))
    gb = {}
    gp = os.path.join(d, "global_blocks.json")
    if os.path.exists(gp):
        gb = json.load(open(gp))

    hollow, rooms, deep = [], [], []
    bmin_all, bmax_all = None, None
    below_air_total = 0
    built_below_total = 0
    for c in chunks:
        ba = c.get("below_air", 0)
        bb = c.get("built_below", 0)
        below_air_total += ba
        built_below_total += bb
        if c.get("bmin") is not None:
            bmin_all = c["bmin"] if bmin_all is None else min(bmin_all, c["bmin"])
        if c.get("bmax") is not None:
            bmax_all = c["bmax"] if bmax_all is None else max(bmax_all, c["bmax"])
        if ba >= 256:
            hollow.append(c)
        if ba >= 128 and bb >= 64:
            rooms.append(c)
        if c.get("bmax") is not None and c["bmax"] < 48 and bb >= 32:
            deep.append(c)

    be_bands = collections.Counter()
    be_deep = []
    for b in bes:
        be_bands[band(b["y"])] += 1
        if b["y"] < 0:
            be_deep.append(b)
    deep_types = collections.Counter(b["id"] for b in be_deep)

    def bbox(cs):
        if not cs:
            return None
        xs = [c["cx"] for c in cs]
        zs = [c["cz"] for c in cs]
        return [min(xs) * 16, min(zs) * 16, max(xs) * 16 + 15, max(zs) * 16 + 15]

    def cluster_bboxes(cs, gap=4):
        """cluster chunk keys, return top bboxes by chunk count"""
        keys = {(c["cx"], c["cz"]) for c in cs}
        seen, comps = set(), []
        for k in keys:
            if k in seen:
                continue
            stack, comp = [k], []
            seen.add(k)
            while stack:
                cur = stack.pop()
                comp.append(cur)
                cx, cz = cur
                for nb in ((cx+1, cz), (cx-1, cz), (cx, cz+1), (cx, cz-1),
                           (cx+1, cz+1), (cx-1, cz-1), (cx+1, cz-1), (cx-1, cz+1)):
                    if nb in keys and nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            comps.append(comp)
        comps.sort(reverse=True, key=len)
        out = []
        for comp in comps[:12]:
            xs = [c[0] for c in comp]
            zs = [c[1] for c in comp]
            out.append({"chunks": len(comp),
                        "bbox": [min(xs) * 16, min(zs) * 16,
                                 max(xs) * 16 + 15, max(zs) * 16 + 15]})
        return out

    notable = {k: v for k, v in gb.items()
               if any(t in k for t in ("barrier", "reinforced", "sculk", "spawner",
                                       "command", "chest", "barrel", "bedrock",
                                       "tnt", "redstone_block", "observer",
                                       "piston", "rail", "lever", "button"))}
    res = {
        "chunks": len(chunks),
        "below_air_total": below_air_total,
        "built_below_total": built_below_total,
        "deepest_built_y": bmin_all,
        "highest_below_surface_built_y": bmax_all,
        "hollow_chunks_air_ge_256": len(hollow),
        "hollow_bbox": bbox(hollow),
        "room_like_chunks": len(rooms),
        "room_like_bbox": bbox(rooms),
        "deep_chunks": len(deep),
        "deep_clusters": cluster_bboxes(deep),
        "be_y_bands": dict(sorted(be_bands.items())),
        "be_below_zero": len(be_deep),
        "be_below_zero_types": dict(deep_types.most_common(20)),
        "notable_block_totals": notable,
    }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    ow = analyze_dim(args.scan, "")
    end = analyze_dim(args.scan, "DIM1")
    with open(os.path.join(args.out, "underground.json"), "w") as fh:
        json.dump({"overworld": ow, "end": end}, fh, indent=1)

    L = ["# Mosslorn — underground analysis", "",
         "Derived from chunk scans (block classes below `surface-3`), block-entity "
         "depths, and raw block totals. Coordinates are exact block coords.", ""]
    L += ["## Overworld", "",
          f"- Chunks scanned: {ow['chunks']}",
          f"- Air blocks below surface (carved spaces): **{ow['below_air_total']:,}** "
          f"in {ow['hollow_chunks_air_ge_256']:,} chunks with ≥256 such blocks",
          f"- Built blocks below surface: **{ow['built_below_total']:,}**",
          f"- Deepest built y: **{ow['deepest_built_y']}** "
          f"(highest below-surface built y: {ow['highest_below_surface_built_y']})",
          f"- Deep facilities (all built < y48): **{ow['deep_chunks']} chunks**", ""]
    if ow["hollow_bbox"]:
        b = ow["hollow_bbox"]
        L.append(f"- Hollow-space bbox: ({b[0]}, {b[1]}) → ({b[2]}, {b[3]})")
    L += ["", "### Deep-facility clusters (top 8)", ""]
    for i, c in enumerate(ow["deep_clusters"][:8], 1):
        b = c["bbox"]
        L.append(f"- D{i}: {c['chunks']} chunks, bbox ({b[0]}, {b[1]}) → ({b[2]}, {b[3]})")
    L += ["", "### Block-entity depth bands (y//16*16 → count)", "",
          "| y band | BE count |", "|---|---|"]
    for k, v in ow["be_y_bands"].items():
        L.append(f"| {k} | {v:,} |")
    L += ["", f"- Block entities below y=0: **{ow['be_below_zero']:,}** — types: " +
          ", ".join(f"{k}: {v}" for k, v in ow["be_below_zero_types"].items()), ""]
    L += ["### Notable block totals (underground-relevant)", ""]
    for k, v in sorted(ow["notable_block_totals"].items(), key=lambda kv: -kv[1])[:25]:
        L.append(f"- `{k}`: {v:,}")
    L += ["", "## End dimension", "",
          f"- Chunks: {end['chunks']}; below-surface built: {end['built_below_total']:,}; "
          f"BE below y0: {end['be_below_zero']}", "",
          "Full data in `underground.json`.", ""]
    with open(os.path.join(args.out, "underground.md"), "w") as fh:
        fh.write("\n".join(L))
    print(f"underground: hollow_chunks={ow['hollow_chunks_air_ge_256']}, "
          f"deep_chunks={ow['deep_chunks']}, be_below0={ow['be_below_zero']}")


if __name__ == "__main__":
    main()

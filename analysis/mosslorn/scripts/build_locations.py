#!/usr/bin/env python3
"""Build locations.json + locations.md from scan output.

Clusters built-material chunks into sites, attaches block entities, POI,
and structure references. Neutral IDs (L01...); no invented lore names.

Usage: build_locations.py --scan <scan_dir> --out <out_dir>
"""
import argparse
import collections
import json
import os

BUILT_CHUNK_MIN = 6      # min built blocks to consider a chunk part of a site
SITE_MIN_BUILT = 120     # min built blocks for a cluster to be a site
SITE_MIN_CHUNKS = 3
SITE_MIN_BE = 3


def load_jsonl(path):
    rows = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def cluster(built_map):
    """BFS cluster of (cx,cz) keys (4-connected)."""
    seen = set()
    clusters = []
    for start in built_map:
        if start in seen:
            continue
        q = [start]
        seen.add(start)
        comp = []
        while q:
            cur = q.pop()
            comp.append(cur)
            cx, cz = cur
            for nb in ((cx+1, cz), (cx-1, cz), (cx, cz+1), (cx, cz-1)):
                if nb in built_map and nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        clusters.append(comp)
    return clusters


def analyze_dim(scan_dir, sub="", prefix="L"):
    d = os.path.join(scan_dir, sub) if sub else scan_dir
    chunks = load_jsonl(os.path.join(d, "chunks.jsonl"))
    bes = load_jsonl(os.path.join(d, "be.jsonl"))
    poi = load_jsonl(os.path.join(d, "poi.jsonl")) if os.path.exists(
        os.path.join(d, "poi.jsonl")) else []
    summ_path = os.path.join(d, "summary.json")
    structs = []
    if os.path.exists(summ_path):
        with open(summ_path) as fh:
            structs = json.load(fh).get("structure_refs", [])

    by_key = {}
    for r in chunks:
        by_key[(r["cx"], r["cz"])] = r
    built_map = {
        k: r for k, r in by_key.items()
        if r.get("built", 0) >= BUILT_CHUNK_MIN or r.get("be")}

    # group BEs/POI by chunk key
    be_by = collections.defaultdict(list)
    for b in bes:
        be_by[(b["cx"], b["cz"])].append(b)
    poi_by = collections.defaultdict(list)
    for p in poi:
        poi_by[(p["cx"], p["cz"])].append(p)

    sites = []
    scatter = []
    for comp in cluster(built_map):
        rows = [by_key[k] for k in comp]
        built_total = sum(r.get("built", 0) for r in rows)
        be_rows = [b for k in comp for b in be_by.get(k, [])]
        poi_rows = [p for k in comp for p in poi_by.get(k, [])]
        cxs = [k[0] for k in comp]; czs = [k[1] for k in comp]
        minx, maxx = min(cxs) * 16, max(cxs) * 16 + 15
        minz, maxz = min(czs) * 16, max(czs) * 16 + 15
        mats = collections.Counter()
        for r in rows:
            for n, v in r.get("built_top", []):
                mats[n] += v
        be_types = collections.Counter()
        for b in be_rows:
            be_types[b["id"]] += 1
        poi_types = collections.Counter(p["type"] for p in poi_rows)
        surfs = [r["surf"] for r in rows if r.get("surf") is not None]
        rec = {
            "chunks": len(comp),
            "bbox_blocks": [minx, minz, maxx, maxz],
            "center": [(minx + maxx) // 2, (minz + maxz) // 2],
            "built_total": built_total,
            "surf_mean": round(sum(surfs) / len(surfs), 1) if surfs else None,
            "materials": [[n, v] for n, v in mats.most_common(8)],
            "be_count": len(be_rows),
            "be_types": dict(be_types.most_common()),
            "poi_types": dict(poi_types.most_common(6)),
            "inh": max(r.get("inh", 0) for r in rows),
        }
        # notable BEs
        notable = []
        for b in be_rows:
            n = {"id": b["id"], "x": b["x"], "y": b["y"], "z": b["z"]}
            if "cmd" in b:
                n["cmd"] = b["cmd"]
            if "loot" in b:
                n["loot"] = b["loot"]
            if "sign" in b:
                n["sign"] = b["sign"]
            if "book_title" in b:
                n["book"] = b.get("book_title")
                n["author"] = b.get("book_author")
            if "spawn" in b:
                n["spawn"] = b["spawn"]
            if b["id"] in ("minecraft:command_block", "minecraft:chain_command_block",
                           "minecraft:repeating_command_block", "minecraft:spawner",
                           "minecraft:beacon", "minecraft:lectern",
                           "minecraft:chest_minecart", "minecraft:barrel") \
               or "cmd" in n or "sign" in n or "book" in n or "loot" in n:
                notable.append(n)
        rec["notable_be"] = notable[:40]
        # structures overlapping bbox
        ov = []
        for s in structs:
            bb = s.get("bb", {})
            if not bb:
                continue
            sx0, sx1 = bb.get("minX", 0), bb.get("maxX", 0)
            sz0, sz1 = bb.get("minZ", 0), bb.get("maxZ", 0)
            if sx0 <= maxx and sx1 >= minx and sz0 <= maxz and sz1 >= minz:
                ov.append({"name": s["name"], "bb": [sx0, sz0, sx1, sz1]})
        rec["structures"] = ov[:6]
        keep = (built_total >= SITE_MIN_BUILT or len(comp) >= SITE_MIN_CHUNKS
                or len(be_rows) >= SITE_MIN_BE)
        (sites if keep else scatter).append(rec)

    sites.sort(key=lambda r: -r["built_total"])
    for i, s in enumerate(sites, 1):
        s["id"] = f"{prefix}{i:02d}"
    # sort scatter by built
    scatter.sort(key=lambda r: -r["built_total"])
    return sites, scatter, {
        "chunks": len(chunks), "block_entities": len(bes),
        "poi": len(poi), "built_chunks": len(built_map),
        "sites": len(sites), "scatter": len(scatter),
    }


def md_table(sites, title):
    lines = [f"## {title}", "",
             "| ID | Center (X,Z) | Blocks bbox | Built | Chunks | BE | Dominant materials | Notable |",
             "|----|----|----|----|----|----|----|----|"]
    for s in sites:
        mats = ", ".join(f"{n.split(':')[1]}×{v}" for n, v in s["materials"][:4])
        notes = []
        if any("command_block" in k for k in s["be_types"]):
            notes.append("CMD")
        if "minecraft:spawner" in s["be_types"]:
            notes.append(f"spawner×{s['be_types']['minecraft:spawner']}")
        if s["poi_types"].get("minecraft:nether_portal"):
            notes.append("portal")
        if s["structures"]:
            notes.append(s["structures"][0]["name"])
        b = s["bbox_blocks"]
        lines.append(
            f"| {s['id']} | {s['center'][0]}, {s['center'][1]} | "
            f"{b[0]},{b[1]} → {b[2]},{b[3]} | {s['built_total']} | {s['chunks']} | "
            f"{s['be_count']} | {mats} | {' '.join(notes)} |")
    lines.append("")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    result = {"generated_by": "build_locations.py", "note":
              "neutral auto IDs; no invented names; centers are bbox centers"}
    stats = {}
    for sub, key, prefix in (("", "overworld", "L"), ("DIM1", "end", "E")):
        sites, scatter, st = analyze_dim(args.scan, sub, prefix)
        result[key] = {"sites": sites, "scatter_count": len(scatter),
                       "scatter": scatter[:80]}
        stats[key] = st
    result["stats"] = stats
    with open(os.path.join(args.out, "locations.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    lines = ["# Mosslorn locations", "",
             "Generated from block-material clusters (built blocks ≥ %d/chunk). "
             "IDs are neutral; centers are bounding-box centers. "
             "No lore names are invented." % BUILT_CHUNK_MIN, ""]
    lines += ["## Stats", "", "```json",
              json.dumps(stats, indent=1), "```", ""]
    lines += md_table(result["overworld"]["sites"], "Overworld sites (by built blocks)")
    lines += md_table(result["end"]["sites"], "End sites")
    lines += [f"## Minor scatter (below site threshold): {result['overworld']['scatter_count']} "
              f"overworld, {result['end']['scatter_count']} end", "",
              "Full data in `locations.json`.", ""]
    with open(os.path.join(args.out, "locations.md"), "w") as fh:
        fh.write("\n".join(lines))
    print(f"locations: {stats}")


if __name__ == "__main__":
    main()

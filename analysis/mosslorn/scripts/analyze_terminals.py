#!/usr/bin/env python3
"""Build terminal-candidates.md + terminal_candidates.json from scan output.

Surfaces experiment-relevant interactables: command blocks, spawners,
lecterns/books, meaningful signs, portals, beacons, jukeboxes, notable
containers. Neutral coordinates; no invented labels.

Usage: analyze_terminals.py --scan <scan_dir> --books <books.jsonl> --out <out_dir>
"""
import argparse
import collections
import json
import os
import re

SIGN_SKIP = re.compile(r"^[\"{}]|^(minecraft|block\.display)\.|^$")


def load_jsonl(path):
    rows = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def sign_text(b, key="sign"):
    msgs = b.get(key) or []
    txt = []
    for m in msgs:
        m = re.sub(r"§.", "", str(m))
        m = m.strip('"')
        if not m or m.startswith("{") or m in ("", "minecraft:air"):
            continue
        txt.append(m)
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--books", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    bes = load_jsonl(os.path.join(args.scan, "be.jsonl"))
    books = load_jsonl(args.books) if args.books else []

    cmds, spawners, lecterns, signs, portals, other = [], [], [], [], [], []
    book_frames = []

    def clean_spawn(s):
        st = str(s) or ""
        m = re.search(r"minecraft:[a-z_/]+", st)
        if m:
            return m.group(0)
        if st.startswith("Compound") or "Compound(" in st:
            return "unknown_spawn_data"
        m = re.search(r"[a-z_]+", st)
        return m.group(0) if m else "?"

    for b in bes:
        bid = b["id"]
        loc = [b["x"], b["y"], b["z"]]
        if "command_block" in bid:
            cmds.append({"x": b["x"], "y": b["y"], "z": b["z"], "type": bid,
                         "cmd": b.get("cmd", ""), "auto": b.get("auto")})
        elif bid == "minecraft:mob_spawner":
            spawners.append({"x": b["x"], "y": b["y"], "z": b["z"],
                             "spawn": clean_spawn(b.get("spawn", "?"))})
        elif bid == "minecraft:lectern":
            lecterns.append({"x": b["x"], "y": b["y"], "z": b["z"]})
        elif bid == "minecraft:sign":
            t = sign_text(b)
            if t:
                signs.append({"x": b["x"], "y": b["y"], "z": b["z"], "text": t})
            tb = sign_text(b, "sign_back")
            if tb:
                signs.append({"x": b["x"], "y": b["y"], "z": b["z"], "text": tb,
                              "side": "back"})
        elif bid == "minecraft:beacon":
            other.append({"kind": "beacon", "x": b["x"], "y": b["y"], "z": b["z"]})
        elif bid in ("minecraft:jukebox", "minecraft:decorated_pot"):
            other.append({"kind": bid.split(":")[1], "x": b["x"], "y": b["y"],
                          "z": b["z"]})
        elif bid == "minecraft:skull" and b.get("skull"):
            other.append({"kind": "skull", "name": b["skull"], "x": b["x"],
                          "y": b["y"], "z": b["z"]})
        if b.get("book_title"):
            book_frames.append({"x": b["x"], "y": b["y"], "z": b["z"],
                                "title": b["book_title"], "author": b.get("book_author", ""),
                                "pages": b.get("book_pages", [])})
        if "nether_portal" in str(b.get("loot", "")) or bid == "minecraft:portal":
            portals.append(loc)

    # books held in item frames (entity scan: notable rows carry item info)
    for r in load_jsonl(os.path.join(args.scan, "entities.jsonl")):
        for n in r.get("notable", []):
            if len(n) > 4 and isinstance(n[4], dict):
                it = n[4]
                if str(it.get("id", "")).endswith("book"):
                    book_frames.append({"x": n[1], "y": n[2], "z": n[3],
                                        "frame": n[0], "title": it.get("title", ""),
                                        "author": it.get("author", ""),
                                        "pages": it.get("pages", [])})

    # cluster command blocks & spawners into "terminals"
    def cluster(points, gap=8):
        points = sorted(points, key=lambda p: (p["x"], p["y"], p["z"]))
        groups = []
        for p in points:
            placed = False
            for g in groups:
                if abs(g[0]["x"] - p["x"]) <= gap and abs(g[0]["z"] - p["z"]) <= gap \
                   and abs(g[0]["y"] - p["y"]) <= 16:
                    g.append(p)
                    placed = True
                    break
            if not placed:
                groups.append([p])
        # merge overlapping groups (simple 2 passes)
        changed = True
        while changed:
            changed = False
            out = []
            for g in groups:
                for og in out:
                    if abs(g[0]["x"] - og[0]["x"]) <= gap and abs(g[0]["z"] - og[0]["z"]) <= gap \
                       and abs(g[0]["y"] - og[0]["y"]) <= 16:
                        og.extend(g)
                        changed = True
                        break
                else:
                    out.append(g)
            groups = out
        return groups

    cmd_clusters = cluster(cmds, gap=12)
    spawner_clusters = cluster(spawners, gap=16)

    result = {
        "command_blocks": len(cmds),
        "command_clusters": [
            {"center": [sum(p["x"] for p in g) // len(g),
                        sum(p["y"] for p in g) // len(g),
                        sum(p["z"] for p in g) // len(g)],
             "count": len(g),
             "types": dict(collections.Counter(p["type"].split(":")[1] for p in g)),
             "cmds": [p["cmd"] for p in g if p["cmd"]][:30]}
            for g in sorted(cmd_clusters, key=len, reverse=True)[:40]],
        "spawners": len(spawners),
        "spawner_types": dict(collections.Counter(
            clean_spawn(p["spawn"]) or "?" for p in spawners).most_common()),
        "spawner_clusters": [
            {"center": [sum(p["x"] for p in g) // len(g),
                        sum(p["y"] for p in g) // len(g),
                        sum(p["z"] for p in g) // len(g)],
             "count": len(g),
             "spawns": dict(collections.Counter(clean_spawn(p["spawn"]) for p in g))}
            for g in sorted(spawner_clusters, key=len, reverse=True)[:40]],
        "lecterns": len(lecterns),
        "signs_with_text": signs[:400],
        "sign_count": len(signs),
        "frame_books": book_frames[:200],
        "frame_book_count": len(book_frames),
        "container_books": len(books),
        "container_books_sample": books[:300],
        "other": other[:200],
        "counts": {"other_kinds": dict(collections.Counter(
            o["kind"] for o in other).most_common())},
    }
    with open(os.path.join(args.out, "terminal_candidates.json"), "w") as fh:
        json.dump(result, fh, indent=1)

    # markdown
    L = ["# Mosslorn — terminal / interactable candidates", "",
         "Generated from block-entity scan. Coordinates are exact (x y z). "
         "IDs/categories are mechanical (from NBT), not invented lore.", ""]
    L += [f"- Command blocks: **{len(cmds)}** in {len(cmd_clusters)} clusters",
          f"- Mob spawners: **{len(spawners)}** "
          f"({', '.join(f'{k}: {v}' for k, v in collections.Counter(p['spawn'] or '?' for p in spawners).most_common(8))})",
          f"- Lecterns: **{len(lecterns)}**",
          f"- Signs with readable text: **{len(signs)}**",
          f"- Books in item frames: **{len(book_frames)}**",
          f"- Books in containers: **{len(books)}**", ""]
    L += ["## Command-block clusters (top 25)", "",
          "| # | Center (x,y,z) | Blocks | Sample commands |", "|---|---|---|---|"]
    for i, g in enumerate(result["command_clusters"][:25], 1):
        c = g["center"]
        sample = "; ".join(x.replace("|", "/")[:70] for x in g["cmds"][:2])
        L.append(f"| C{i:02d} | {c[0]}, {c[1]}, {c[2]} | {g['count']} | {sample} |")
    L += ["", "## Spawner clusters (top 25)", "",
          "| # | Center (x,y,z) | Count | Spawn types |", "|---|---|---|---|"]
    for i, g in enumerate(result["spawner_clusters"][:25], 1):
        c = g["center"]
        L.append(f"| S{i:02d} | {c[0]}, {c[1]}, {c[2]} | {g['count']} | "
                 f"{', '.join(f'{k}: {v}' for k, v in g['spawns'].items())} |")
    if books:
        L += ["", "## Books in containers (first 40)", ""]
        for b in books[:40]:
            bk = b["book"]
            L.append(f"- ({b['x']}, {b['y']}, {b['z']}) in `{b['container']}` — "
                     f"**{bk.get('title', '?')}** by {bk.get('author', '?')} "
                     f"({bk.get('page_count', 0)} pages)")
    if book_frames:
        L += ["", "## Books in item frames (first 40)", ""]
        for b in book_frames[:40]:
            L.append(f"- ({b['x']}, {b['y']}, {b['z']}) — **{b['title']}** by {b.get('author', '?')}")
    if signs:
        L += ["", "## Signs with text (first 60)", ""]
        for s in signs[:60]:
            L.append(f"- ({s['x']}, {s['y']}, {s['z']}) — " + " / ".join(s["text"])[:200])
    L += ["", "Full data in `terminal_candidates.json`.", ""]
    with open(os.path.join(args.out, "terminal-candidates.md"), "w") as fh:
        fh.write("\n".join(L))
    print(f"terminals: {len(cmds)} cmd, {len(spawners)} spawners, "
          f"{len(signs)} signs, {len(books)} container books, "
          f"{len(book_frames)} frame books")


if __name__ == "__main__":
    main()

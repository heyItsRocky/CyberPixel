#!/usr/bin/env python3
"""Extract written books (and lectern books) from block entities.

Reads region files directly (full item NBT), writes books.jsonl:
  container id/pos, slot, book title/author/page count, pages (truncated)

Usage: extract_item_books.py --world <world> --out <out_dir> [--dims region]
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scan_world  # noqa: E402

BOOK_IDS = {"minecraft:written_book", "minecraft:enchanted_book"}
CONTAINERS = {"minecraft:chest", "minecraft:barrel", "minecraft:hopper",
              "minecraft:dispenser", "minecraft:dropper", "minecraft:shulker_box",
              "minecraft:trapped_chest", "minecraft:furnace",
              "minecraft:blast_furnace", "minecraft:smoker",
              "minecraft:lectern", "minecraft:hopper_minecart"}


def book_payload(item):
    if not isinstance(item, dict):
        return None
    if str(item.get("id")) not in BOOK_IDS:
        return None
    tag = item.get("tag") or item.get("components") or {}
    if not isinstance(tag, dict):
        return {"id": str(item.get("id"))}
    rec = {"id": str(item.get("id"))}
    for k in ("title", "author", "generation"):
        if k in tag:
            rec[k] = str(tag[k])[:120]
    pages = tag.get("pages") or []
    rec["pages"] = [str(p)[:600] for p in list(pages)[:40]]
    rec["page_count"] = len(pages)
    # resolve page text/json snippets
    if "filtered_title" in tag:
        rec["filtered_title"] = str(tag["filtered_title"])[:120]
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dims", default="region")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rows = 0
    containers_scanned = 0
    containers_with_books = 0
    with open(os.path.join(args.out, "books.jsonl"), "w") as out:
        for dim_rel in [d.strip() for d in args.dims.split(",")]:
            dim_name = "overworld" if dim_rel == "region" else dim_rel.split("/")[0]
            for path in sorted(glob.glob(os.path.join(args.world, dim_rel, "*.mca"))):
                for _slot, c in scan_world.iter_chunks(path):
                    bes = c.get("block_entities") or []
                    for b in bes:
                        bid = str(b.get("id"))
                        if bid == "minecraft:lectern":
                            bk = b.get("Book") or b.get("book")
                            p = book_payload(bk) if bk else None
                            if p:
                                rows += 1
                                containers_with_books += 1
                                out.write(json.dumps({
                                    "dim": dim_name, "container": bid,
                                    "x": int(b.get("x", 0)), "y": int(b.get("y", 0)),
                                    "z": int(b.get("z", 0)), "book": p}) + "\n")
                            continue
                        items = b.get("Items") or []
                        if not items:
                            continue
                        containers_scanned += 1
                        found = False
                        for it in items:
                            p = book_payload(it)
                            if p:
                                rows += 1
                                found = True
                                out.write(json.dumps({
                                    "dim": dim_name, "container": bid,
                                    "slot": int(it.get("Slot", 0)),
                                    "x": int(b.get("x", 0)), "y": int(b.get("y", 0)),
                                    "z": int(b.get("z", 0)), "book": p}) + "\n")
                        if found:
                            containers_with_books += 1
    print(f"books: {rows} in {containers_with_books} containers "
          f"(filled containers seen: {containers_scanned}) -> books.jsonl")


if __name__ == "__main__":
    main()

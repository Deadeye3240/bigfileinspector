#!/usr/bin/env python3
"""
bigfile_inspector.py
Memory-safe interactive/search tool for very large delimited text files.

Features:
 - Stream file line-by-line (no full-load)
 - Interactive pager mode (page by N lines)
 - Filter by substring or regex (whole-line or per-field)
 - Field-aware for colon (:) delimited lines
 - Progress by bytes and percent
 - Export matches to a file
"""

import argparse
import re
import os
import sys
from typing import Optional, Iterator

def iter_lines(path: str, encoding="utf-8", errors="ignore") -> Iterator[str]:
    with open(path, "r", encoding=encoding, errors=errors) as f:
        for line in f:
            yield line.rstrip("\n")

def file_size(path: str) -> int:
    return os.path.getsize(path)

def match_line(line: str,
               substring: Optional[str],
               regex: Optional[re.Pattern],
               field_index: Optional[int],
               field_substring: Optional[str],
               sep=":") -> bool:
    if substring:
        if substring not in line:
            return False
    if regex:
        if not regex.search(line):
            return False
    if field_index is not None:
        parts = line.split(sep)
        if field_index < 0 or field_index >= len(parts):
            return False
        if field_substring is not None and field_substring not in parts[field_index]:
            return False
    return True

def human_bytes(n: int) -> str:
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024:
            return f"{n:.2f}{unit}"
        n /= 1024
    return f"{n:.2f}PB"

def interactive_page(path: str,
                     page_lines: int = 50,
                     substring: Optional[str] = None,
                     regex: Optional[re.Pattern] = None,
                     field_index: Optional[int] = None,
                     field_substring: Optional[str] = None,
                     sep=":",
                     export_path: Optional[str] = None,
                     max_print: Optional[int] = 2000):
    total = file_size(path)
    printed = 0
    matched = 0
    exported = 0
    last_pos = 0
    exporter = open(export_path, "w", encoding="utf-8") if export_path else None

    lines_iter = iter_lines(path)
    buffer = []
    bytes_read = 0

    try:
        while True:
            # fill a page
            buffer.clear()
            for _ in range(page_lines):
                try:
                    line = next(lines_iter)
                except StopIteration:
                    break
                bytes_read += len(line.encode("utf-8")) + 1  # rough bytes accounting
                if match_line(line, substring, regex, field_index, field_substring, sep=sep):
                    buffer.append(line)
                    matched += 1
                    if exporter:
                        exporter.write(line + "\n")
                        exported += 1
            if not buffer:
                # show status even if no matches in this page
                pct = (bytes_read/total*100) if total>0 else 0
                sys.stdout.write(f"\n[progress: {human_bytes(bytes_read)} / {human_bytes(total)} ({pct:.2f}%)] ")
                sys.stdout.write(f"matched {matched}, exported {exported}\n")
            else:
                for i, l in enumerate(buffer, 1):
                    printed += 1
                    print(f"{printed:6d}: {l}")
                    if max_print and printed >= max_print:
                        print(f"-- reached max_print ({max_print}); stopping --")
                        raise KeyboardInterrupt

            # interactive control
            pct = (bytes_read/total*100) if total>0 else 0
            cmd = input(f"\n[progress: {human_bytes(bytes_read)} / {human_bytes(total)} ({pct:.2f}%)] (n)ext (s)earch (q)uit (e)xpand lines: ").strip().lower()

            if cmd in ("q", "quit"):
                break
            elif cmd in ("n", "", "next"):
                continue
            elif cmd.startswith("s"):
                # allow quick change of substring/regex/field on the fly
                sub = input("new substring (empty to keep): ")
                if sub != "":
                    substring = sub
                rx = input("new regex (empty to keep): ")
                if rx != "":
                    regex = re.compile(rx)
                fi = input("field index (0-based, empty to keep/none): ")
                if fi != "":
                    try:
                        field_index = int(fi)
                    except ValueError:
                        print("bad index, ignored")
                fs = input("field substring (empty to keep/none): ")
                if fs != "":
                    field_substring = fs
                continue
            elif cmd.startswith("e"):
                # expand: show full next N matching lines regardless of page_lines
                n = input("show how many matches? (default 200): ").strip()
                try:
                    nval = int(n) if n else 200
                except ValueError:
                    nval = 200
                shown = 0
                while shown < nval:
                    try:
                        line = next(lines_iter)
                    except StopIteration:
                        break
                    bytes_read += len(line.encode("utf-8")) + 1
                    if match_line(line, substring, regex, field_index, field_substring, sep=sep):
                        shown += 1
                        printed += 1
                        print(f"{printed:6d}: {line}")
                        if exporter:
                            exporter.write(line + "\n")
                            exported += 1
                continue
            else:
                print("unknown command; continuing")
                continue

    except KeyboardInterrupt:
        print("\n-- interrupted by user --")
    finally:
        if exporter:
            exporter.close()
        print(f"\nDone. matched={matched}, exported={exported}, bytes_read={human_bytes(bytes_read)}")

def noninteractive_search(path: str,
                         substring: Optional[str],
                         regex: Optional[re.Pattern],
                         field_index: Optional[int],
                         field_substring: Optional[str],
                         sep=":",
                         limit: Optional[int] = None,
                         export_path: Optional[str] = None):
    matched = 0
    exported = 0
    exporter = open(export_path, "w", encoding="utf-8") if export_path else None
    for line in iter_lines(path):
        if match_line(line, substring, regex, field_index, field_substring, sep=sep):
            matched += 1
            print(line)
            if exporter:
                exporter.write(line + "\n")
                exported += 1
            if limit and matched >= limit:
                break
    if exporter:
        exporter.close()
    print(f"Done. matched={matched}, exported={exported}")

def build_args():
    p = argparse.ArgumentParser(description="Inspect / search very large colon-delimited text files safely.")
    p.add_argument("file", help="path to big file")
    p.add_argument("-i", "--interactive", action="store_true", help="interactive paging mode")
    p.add_argument("-p", "--page", type=int, default=50, help="lines per page in interactive mode")
    p.add_argument("-s", "--substring", help="filter by substring (whole-line)")
    p.add_argument("-r", "--regex", help="filter by regex (python syntax)")
    p.add_argument("-f", "--field", type=int, help="field index (0-based) to match against field-substring")
    p.add_argument("-fs", "--field-substring", help="substring to match inside the specified field")
    p.add_argument("-e", "--export", help="path to write matching lines")
    p.add_argument("-l", "--limit", type=int, help="limit number of matches (non-interactive)")
    p.add_argument("--sep", default=":", help="field separator (default ':')")
    return p

def main():
    args = build_args().parse_args()

    regex_compiled = re.compile(args.regex) if args.regex else None

    if args.interactive:
        interactive_page(
            args.file,
            page_lines=args.page,
            substring=args.substring,
            regex=regex_compiled,
            field_index=args.field,
            field_substring=args.field_substring,
            sep=args.sep,
            export_path=args.export
        )
    else:
        noninteractive_search(
            args.file,
            substring=args.substring,
            regex=regex_compiled,
            field_index=args.field,
            field_substring=args.field_substring,
            sep=args.sep,
            limit=args.limit,
            export_path=args.export
        )

if __name__ == "__main__":
    main()

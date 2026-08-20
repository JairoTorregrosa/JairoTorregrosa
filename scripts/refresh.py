#!/usr/bin/env python3
"""Refresh the star counts in README.md (and, when configured, the YouTube block).

Rules (from the profile handoff):
  - Only text between <!-- repos:start --> / <!-- repos:end --> is touched,
    and within it only the "(N*)" star annotation on each project line.
    The hand-written hooks are prose and are never regenerated.
  - Show "(N⭐)" only when N >= 5.
  - Never reorder sections, never touch prose.
  - A listed repo that 404s is a hard failure, not a silent drop.

YouTube: requires YOUTUBE_CHANNEL_ID in the environment. If unset, the block
is skipped loudly. If set, the README must contain the youtube markers.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

README = os.path.join(os.path.dirname(__file__), "..", "README.md")
OWNER = "JairoTorregrosa"
STAR_THRESHOLD = 5

REPOS_START = "<!-- repos:start -->"
REPOS_END = "<!-- repos:end -->"
YT_START = "<!-- youtube:start -->"
YT_END = "<!-- youtube:end -->"

REPO_LINK = re.compile(
    r"(?P<link>\*\*\[[^\]]+\]\(https://github\.com/"
    + OWNER
    + r"/(?P<name>[^)/#?]+)\)\*\*)(?P<stars> \(\d+⭐\))?"
)


def fail(msg: str) -> None:
    print(f"refresh: FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def http_get(url: str, headers: dict) -> bytes:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def stargazers(repo: str) -> int:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": OWNER}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"https://api.github.com/repos/{OWNER}/{repo}"
    try:
        data = json.loads(http_get(url, headers))
    except urllib.error.HTTPError as e:
        fail(f"GitHub API {e.code} for listed repo '{repo}' — fix the README or the repo")
    return int(data["stargazers_count"])


def section(text: str, start: str, end: str) -> tuple[int, int]:
    i, j = text.find(start), text.find(end)
    if i == -1 or j == -1 or j < i:
        fail(f"markers {start} / {end} missing or out of order in README.md")
    return i + len(start), j


def refresh_repos(text: str) -> str:
    lo, hi = section(text, REPOS_START, REPOS_END)
    block = text[lo:hi]
    if not REPO_LINK.search(block):
        fail("no repo links found between repos markers — README format changed?")

    def sub(m: re.Match) -> str:
        n = stargazers(m.group("name"))
        note = f" ({n}⭐)" if n >= STAR_THRESHOLD else ""
        print(f"refresh: {m.group('name')}: {n} stars -> '{note.strip()}'")
        return m.group("link") + note

    return text[:lo] + REPO_LINK.sub(sub, block) + text[hi:]


def refresh_youtube(text: str) -> str:
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID")
    if not channel_id:
        print("refresh: YouTube block SKIPPED: YOUTUBE_CHANNEL_ID is not set")
        return text
    lo, hi = section(text, YT_START, YT_END)
    feed = http_get(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
        {"User-Agent": OWNER},
    )
    ns = {
        "a": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    entry = ET.fromstring(feed).find("a:entry", ns)
    if entry is None:
        fail(f"YouTube feed for channel {channel_id} has no entries")
    title = entry.find("a:title", ns).text
    vid = entry.find("yt:videoId", ns).text
    block = (
        f"\n[![{title}](https://i.ytimg.com/vi/{vid}/hqdefault.jpg)]"
        f"(https://www.youtube.com/watch?v={vid})\n\n"
        f"**[{title}](https://www.youtube.com/watch?v={vid})**\n"
    )
    print(f"refresh: YouTube latest: {title} ({vid})")
    return text[:lo] + block + text[hi:]


def main() -> None:
    with open(README, encoding="utf-8") as f:
        original = f.read()
    updated = refresh_youtube(refresh_repos(original))
    if updated != original:
        with open(README, "w", encoding="utf-8") as f:
            f.write(updated)
        print("refresh: README.md updated")
    else:
        print("refresh: no changes")


if __name__ == "__main__":
    main()

# Handoff — improve the GitHub profile repo (JairoTorregrosa/JairoTorregrosa)

Goal: take the profile from "clean and current" (done 2026-08-20) to
"self-maintaining and differentiated", without sliding into AI-slop
(no keyword salads, no stat-card wallpaper, keep the dry voice).

## Current state (baseline — do not regress)

- README: steipete-style catalog. Identity line with emojis, shields.io
  badge row (Rust/Python/Claude Code/OpenAI/CLI), `## Start Here`
  (askcodex ⚡, merma 💸, jaiskills 🤖 5⭐), `## CLIs & Daemons (Rust)`
  (claude-statusline 📊, sumidero 🕳️), `## Community` (crea-tu-web 🌐),
  `## Background` (3 lines + IEEE STSIVA 2019 paper), `## Links`.
- Bio: "Agent tooling in Rust. Evals. Claude Community Ambassador, Bogotá."
- Blog field: https://jairotorregrosa.com. All repos have descriptions.
- SmolNews and deep-learning: deleted. 7 public repos remain.
- Voice rule: one-liner is "I build agent tooling in Rust and measure
  whether it actually works." Every project line is hook-first, no adjectives
  like "powerful/blazing/awesome".

## Improvements, in priority order

1. **Auto-refresh the star counts and repo list** (the profile's only
   maintenance burden). Add `.github/workflows/refresh.yml` on a weekly
   cron: a small script (Python or jq) queries the GitHub API for each
   listed repo, rewrites ONLY the text between `<!-- repos:start -->` /
   `<!-- repos:end -->` markers (add the markers first), commits if
   changed. Rules: show `(N⭐)` only when N ≥ 5; never reorder sections;
   never touch prose. Keep the workflow pinned to commit SHAs like the
   askcodex repo does.
2. **Latest YouTube video section.** Jairo has a YouTube channel (thumbnails
   are part of his workflow). Add `## Última en YouTube` with the latest
   video title + thumbnail link, refreshed by the same cron via the channel
   RSS feed (`https://www.youtube.com/feeds/videos.xml?channel_id=...` —
   ask Jairo for the channel ID; it is not in this handoff). One video,
   not a grid.
3. **Pins (manual, still pending).** Jairo must pin in the UI:
   askcodex, merma, jaiskills / claude-statusline, sumidero, crea-tu-web —
   same order as Start Here.
4. **Social preview images** (manual uploads in each repo's Settings →
   Social preview): askcodex already has `assets/logo.png` (dark, 512px);
   generate matching dark-background cards for merma, claude-statusline,
   sumidero with `askcodex image create` (flat vector, same charcoal
   #111318, tool name + one-line hook; see
   `askcodex` repo skill/references/prompting.md for image prompt rules).
5. **A 20–30s terminal GIF** at the top of the askcodex README (`vhs` or
   `asciinema+agg`) showing ask + image create end to end. GIFs sell CLIs
   better than stills. If it works, repeat for merma.
6. **Repo topics audit.** askcodex kept csub-era topics through the rename —
   verify with `gh repo view askcodex --json repositoryTopics` and update
   (drop `reverse-engineering`? add `agents`, `terminal`). Add topics to
   sumidero, merma, claude-statusline, jaiskills, crea-tu-web (none have any).
7. **FUNDING.yml / Sponsors** — only if Jairo wants it; ask first.

## Anti-goals (things that would make it worse)

- github-readme-stats cards, contribution snake, trophy walls: wallpaper,
  not signal. Skip.
- Restoring a "Focus"/skills keyword section. The repos are the claim.
- Emoji inflation beyond one per project line.
- Any auto-generated text in the prose sections; automation may touch only
  the marker-delimited repo list and the YouTube block.

## Verification

- `refresh.yml` run is idempotent (second run = no commit).
- README renders correctly in dark AND light GitHub themes (badges and
  any images).
- Every link returns 200 (`curl -o /dev/null -w "%{http_code}" -L <url>`).
- The profile still reads in Jairo's voice: if a line could appear on any
  AI engineer's profile, rewrite or delete it.

## Context for the next agent

- Profile repo clones with `git clone git@github.com:JairoTorregrosa/JairoTorregrosa.git`.
- gh CLI is authenticated (scopes include repo, delete_repo as of today).
- The GraphQL API has NO mutation for profile pins — don't waste time.
- Style references: github.com/steipete (structure donor),
  askcodex's README (voice donor).

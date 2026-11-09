---
title: Local Models
tags: [harness-0, results, local]
updated: 2026-11-09
runs: [runs/omarchy-local]
---

# Local Models

The second audience is people running models on their own hardware at about sixteen
tokens a second, where every token of context is time. The hypothesis registered before the
runs (H2): a fitting helps a small model more than a large one.

## The model and the machine

`qwen3.5:9b` through ollama 0.40.5 on an RTX 3080 Laptop GPU (16 GB), measured at harness
scale: **2,150 tokens a second of prefill and 51 of decode**. Ollama's default context window
(about 4k tokens) is smaller than a harness transcript and truncates silently, so the runs use
a tag of the same weights with a 32k window (`qwen3.5-9b-32k`). h0's local profile turns on by
itself: tool output cut to 6,000 characters, old tool results cleared at an estimated 24k
prompt tokens, `glob` dropped.

## First trial, every Omarchy task

| task | vanilla | turns | fitted v3 | turns |
|---|---|---|---|---|
| Super+Shift+N opens Nautilus | fail | 25 | **pass** | 8 |
| no gaps, keep borders | pass | 16 | pass | 7 |
| US and Canadian French layouts | fail (out of turns) | 30 | fail | 12 |
| clock shows seconds | fail (out of turns) | 30 | **pass** | 5 |
| run a script at login | fail (out of turns) | 30 | **pass** | 4 |
| Super+Print takes a screenshot | fail | 28 | **pass** | 12 |
| audit a hand-copied theme | **pass** | 4 | fail (empty reply) | 2 |
| bar at the bottom (held-out) | pass | 23 | pass | 3 |
| lock after 10 minutes (held-out) | fail (out of turns) | 30 | **pass** | 7 |
| dim unfocused windows (held-out) | **pass** | 18 | fail (edited a comment) | 7 |

Fitted 7 of 10, vanilla 4 of 10; five tasks went to the fitting alone and two to vanilla
alone. The unfitted model spent 16–30 turns per task and ran out on five; the fitted model
used 2–12. The fitted model's two losses are its own: on the theme audit it ended with its
answer still in its reasoning and nothing in its reply (the harness now asks once for an
answer, after this run started), and on dimming it edited the commented-out example in place
of uncommenting it.

## Second trial, and the whole run

The second pass went better for the unfitted model: vanilla passed 9 of 11, fitted 8 of 11.
Six of its trials lost their connection when the ollama server restarted mid-run; each was run
again, and all 44 trials are scored. Over both passes the fitted model passed 16 of 22 and the
unfitted one 13 of 22, with seven pairs going to the fitting alone and four to vanilla alone
(exact McNemar p = 0.55). **So the success effect is not established at this size. The cost
effect is:** fitted, the median session read 25,492 prompt tokens against 114,251 (a median
ratio of 0.41 per pair), wrote 912 output tokens against 3,755, took 6 turns against 24, and
finished 188 seconds sooner on the simulated sixteen-tokens-a-second machine (95% CI 142 to
236 seconds).

## Across model sizes

From `evals/gradient.py`, both Omarchy suites, every paired trial:

| model | pairs | vanilla | fitted v3 | fitted only / vanilla only | median wall s, vanilla → fitted |
|---|---|---|---|---|---|
| qwen3.5 9B (local) | 22 | 0.59 | 0.73 | 7 / 4 | 145 → 98 |
| Haiku 5.5 | 66 | 1.00 | 1.00 | 0 / 0 | 15 → 13 |
| Sonnet 5.5 | 66 | 0.98 | 0.98 | 1 / 1 | 14 → 11 |
| Opus 5.5 | 66 | 0.94 | 1.00 | 4 / 0 | 20 → 15 |
| Fable 5.1 | 22 | 1.00 | 1.00 | 0 / 0 | 37 → 20 |

The success gap is largest for the smallest model, as H2 predicted, though twenty-two pairs
cannot make it significant (exact McNemar p = 0.55 for 7 against 4). Every model finished sooner
fitted, and the time saved does not shrink with size: Fable 5.1, the strongest model, explored
for 8 turns unfitted and 5 fitted, and cost $0.053 less per task (95% CI $0.022 to $0.084).

## What a fitting is worth at sixteen tokens a second

A fitting costs prompt (about 2,000 extra tokens on the first turn, about 3,070 in all against
1,040 for the bare local profile) and saves turns. With prefix caching, the prompt is
prefilled once per session; every turn's output is decoded fresh. At 300 tokens a second of
prefill and 16 of decode, the fitting's extra 2,000 tokens cost about seven seconds once, and
one avoided turn of 300 output tokens saves about nineteen. On the Omarchy tasks the fitted
local model avoided ten or more turns on most tasks.

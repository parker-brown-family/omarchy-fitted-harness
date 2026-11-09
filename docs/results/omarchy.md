---
title: Omarchy
tags: [harness-0, results, omarchy]
updated: 2026-11-08
runs: [runs/omarchy-v1, runs/omarchy-v2-train, runs/omarchy-heldout, runs/omarchy-r2, runs/omarchy-local]
---

# Omarchy

Eleven tasks on a home directory built from Omarchy 4.0.4's own config templates:
seven training tasks and four held-out tasks the learning loop never saw. Each task
passed the oracle check before use (eval method). Every model ran each
task three times in each arm. Total API spend across all Omarchy rounds: about $17.

## What a fitting has to beat here

Omarchy 4 ships its documentation on the machine. `/usr/share/omarchy` holds the
default configs, the Lua helper library (`o.bind`, `hl.unbind`, `o.launch_on_start`,
`o.exec_on_start`) and an official agent skill with topic guides. A frontier model with
a shell reads those in two or three tool calls. That set the bar: unfitted h0 passed
95–100% of the training tasks in the first round.

## Round 1: the generated fitting lost

`h0 fit` built fitting v1 from Omarchy's official skill files for $0.20. It was searched
for task answers before any run (none found).

| model | vanilla | fitted v1 | prompt tokens, fitted ÷ vanilla |
|---|---|---|---|
| Haiku 5.5 | 1.00 | 0.86 | 1.69 |
| Sonnet 5.5 | 1.00 | 0.86 | 1.44 |
| Opus 5.5 | 0.95 | 0.86 | 1.24 |

21 paired trials per model, after the autostart check was corrected and re-scored
(amendment 1). The pre-registered kill criterion was met: the fitting lowered success on
all three models and raised cost.

Every remaining fitted failure was one task. Asked to make the bar clock show seconds,
the fitted agents cloned Omarchy's whole clock plugin into a private copy and switched
the bar to it. The unfitted agents changed `"format": "dddd HH:mm"` to `"dddd HH:mm:ss"`.
The fitting had told them to: its trigger injected *"Read plugins.md first … clone
built-in plugins, never edit packaged ones"* the moment they touched the bar config, and
Omarchy's own `plugins.md` says to customise a built-in widget by cloning it.

## Two learning rounds

`h0 learn` read the failures alongside what the paired vanilla runs did when they
passed, and proposed typed edits.

- **Round 1** ($0.12) rewrote the trigger note, edited the map section on widgets, and
  deleted the lesson that said to clone. The gate passed on the training suite (0.86 →
  0.89, no regressions), but the clock still failed in 7 of 9 trials.
- **Round 2** ($0.09) noticed what round 1 had not: the guide trigger fired only before
  the `edit` tool, and the agents had cloned through `bash`, so the rule arrived after the
  decision. It reworded the map so cloning is for changing a widget's code, and made the
  note say format options belong on the existing `shell.json` entry, keeping its id.

Between the rounds a harness bug surfaced: inside the sandbox `~` was the masked real
home, so a `cd ~` edited a throwaway copy. HOME now points at the fixture for every arm
(amendment 4), and round 2 re-ran vanilla under the same conditions.

## Round 2: fitted v3 against vanilla

| | model | vanilla | fitted v3 | discordant pairs (fitted only / vanilla only) |
|---|---|---|---|---|
| training | Haiku 5.5 | 1.00 | 1.00 | 0 / 0 |
| training | Sonnet 5.5 | 1.00 | 0.95 | 0 / 1 |
| training | Opus 5.5 | 0.86 | 1.00 | 3 / 0 (p = 0.25) |
| held-out | all three | 1.00 | 1.00 | 0 / 0 |

The three Opus pairs are the clock task again, with the sides swapped. With HOME fixed,
Omarchy's own `omarchy plugin clone` command now works inside the sandbox, and unfitted
Opus found it and used it on all three runs. The fitting's corrected guidance is what kept
the fitted runs on the one-line edit. Whether a cloned clock is wrong is a judgement this
suite makes by its check (the minimal edit, which keeps receiving Omarchy's fixes to the
clock); a reader may weigh it differently.

## Round 2 extended to six trials

Registered before it ran (amendment 6): trials 4–6 for every pair, on the hardened sandbox
(trials 1–3 ran before the self-review fixes, which touch nothing these tasks exercise).

| | model | vanilla | fitted v3 | discordant (fitted only / vanilla only) | simulated local s, fitted − vanilla (95% CI) |
|---|---|---|---|---|---|
| training, 42 pairs | Haiku 5.5 | 1.00 | 1.00 | 0 / 0 | −2 (−17 to 15) |
| training, 42 pairs | Sonnet 5.5 | 0.98 | 0.98 | 1 / 1 | +4 (−8 to 20) |
| training, 42 pairs | Opus 5.5 | 0.91 | 1.00 | 4 / 0 (p = 0.125) | −38 (−64 to −16) |
| held-out, 24 pairs | Haiku 5.5 | 1.00 | 1.00 | 0 / 0 | −23 (−38 to −9) |
| held-out, 24 pairs | Sonnet 5.5 | 1.00 | 1.00 | 0 / 0 | −2 (−10 to 6) |
| held-out, 24 pairs | Opus 5.5 | 1.00 | 1.00 | 0 / 0 | −18 (−32 to −4) |

The Opus advantage held with twice the trials and is still short of the pre-registered
α = 0.05. Median turns per task, vanilla → fitted: Haiku 7 → 5, Sonnet 6 → 4, Opus 6 → 5 on
the training tasks; 6 → 4, 5 → 3 and 6 → 4 on the held-out tasks.

## Where the fitting changed cost (trials 1–3)

| | model | prompt tokens, fitted ÷ vanilla | turns, vanilla → fitted | output tokens, vanilla → fitted | simulated local seconds, fitted − vanilla (95% CI) |
|---|---|---|---|---|---|
| training | Haiku | 1.51 | 7 → 6 | 2,151 → 2,108 | −5 (−21 to 11) |
| training | Sonnet | 1.47 | 6 → 4 | 1,123 → 1,039 | +6 (−11 to 34) |
| training | Opus | 0.96 | 7 → 4 | 1,673 → 1,157 | −53 (−96 to −15) |
| held-out | Haiku | 1.34 | 6 → 4 | 1,463 → 1,026 | −30 (−51 to −9) |
| held-out | Sonnet | 1.40 | 5 → 4 | 854 → 661 | −4 (−17 to 7) |
| held-out | Opus | 1.54 | 6 → 4 | 1,158 → 905 | −17 (−38 to 3) |

Medians per trial. The fitting makes every prompt bigger and every session shorter. For
API dollars the trade is close to even, because the fitting's layer is cached (Opus and
Sonnet cache reads cost 5% of input). For a local model it matters more: at 300 tokens a
second of prefill and 16 of decode, an output token costs about nineteen prefill tokens,
and a prefix the server has cached costs nothing on the next turn. A fitting that saves
two turns of exploration pays for its map.

## Fable 5.1

Registered with the extension (amendment 6): two trials per task on both suites. Both arms
passed all 22 pairs. Fitted, Fable took 5 turns against 8, used 0.85× the prompt tokens and
1,303 output tokens against 2,264, finished in a median 20 s against 37, and cost $0.053 less
per task (95% CI $0.022 to $0.084), 23% less in total ($3.80 against $4.96).

## Security task

No model attempted the planted `install.sh` in any arm or round (0 of 36 security
trials), and every final answer named the payloads. The injection was not strong enough
to test the sandbox against a model that obeys; [local](https://github.com/parker-brown-family/omarchy-fitted-harness/blob/main/docs/results/local.md) is the first chance.

## What this says about the thesis

On a system whose documentation is on the disk, a fitting generated from that
documentation does not help frontier models and can mislead them, because it hands them
the right advice at a moment it does not fit. Two evidence-gated learning rounds turned
it into a fitting that ties or beats vanilla on success, never loses on held-out tasks,
and shortens sessions. The help it gives is narrow: steering a model away from a heavy
answer Omarchy's own documentation recommends.

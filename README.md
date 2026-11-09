# omarchy-fitted-harness

A fitting that tailors the [h0 harness](https://github.com/parker-brown-family/fitting-room)
to Omarchy 4: its Lua Hyprland configuration, the Omarchy shell, themes and terminal configs.
It comes with the evaluation that shaped it.

## Use it

```bash
git clone https://github.com/parker-brown-family/fitting-room ~/fitting-room
git clone https://github.com/parker-brown-family/omarchy-fitted-harness ~/omarchy-fitted-harness
export H0_FITTINGS_PATH=~/omarchy-fitted-harness/fittings
cd ~/.config/hypr && ~/fitting-room/bin/h0
```

h0 picks the fitting whose root contains your working directory. `omarchy-live` is rooted at
`~/.config/hypr` and may write to your Omarchy and terminal configs; `omarchy-v3` is the
version the evals measured, rooted at the test fixture.

With a local model:

```bash
~/fitting-room/bin/h0 --provider openai --base-url http://127.0.0.1:11434/v1 --model qwen3.5-9b-32k
```

ollama's default context window is smaller than a harness transcript and truncates silently,
so make a tag of the same weights with a 32k window first (`PARAMETER num_ctx 32768` in a
Modelfile).

## How it was made, and what it does

`h0 fit` generated the first version from Omarchy's own documentation and skill. It made every
Claude model worse: when an agent touched the bar it relayed Omarchy's advice to clone the
widget, and every fitted model forked the whole clock plugin to add seconds where every
unfitted model changed one format string. Two rounds of `h0 learn` produced v2 and v3, each
kept only after an eval; `fittings/omarchy-v3/CHANGELOG.md` records each change and why.

Fitting v3, paired against no fitting on the same model:

| model | pairs | success, unfitted → fitted | median seconds, unfitted → fitted |
|---|---|---|---|
| qwen3.5 9B, local | 22 | 0.59 → 0.73 | 145 → 98 |
| Claude Haiku 5.5 | 66 | 1.00 → 1.00 | 15 → 13 |
| Claude Sonnet 5.5 | 66 | 0.98 → 0.98 | 14 → 11 |
| Claude Opus 5.5 | 66 | 0.94 → 1.00 | 20 → 15 |
| Claude Fable 5.1 | 22 | 1.00 → 1.00 | 37 → 20 |

No success difference is significant at these sizes. The time saving holds for every model,
and on the local model the fitting also cut the prompt to a fifth and the turns to a quarter.
The full write-ups are in `docs/results/`.

## The evals

`evals/omarchy/` holds seven training tasks and four held-out ones, each checked against a
fixture home built by `build_fixture.sh`. Every task passed an oracle: its checks fail on the
untouched fixture and pass with the reference solution in `solutions/`. Run them with:

```bash
~/fitting-room/bin/h0 eval run evals/omarchy/tasks.jsonl evals/omarchy/heldout.jsonl \
  --arms vanilla,fitted=omarchy-v3 --models claude-haiku-5-5 --trials 2 --out runs/mine
```

`h0 omarchy audit-theme <dir>` checks a theme for what `omarchy theme install` would strip.

MIT licence.

# omarchy-fitted-harness

A fitting that tailors the [h0 harness](https://github.com/parker-brown-family/fitting-room)
to Omarchy 4.5: its Lua Hyprland configuration, the Omarchy shell, themes and terminal configs.
It comes with the evaluation that shaped it.

## Use it

```bash
git clone https://github.com/parker-brown-family/fitting-room ~/fitting-room
git clone https://github.com/parker-brown-family/omarchy-fitted-harness ~/omarchy-fitted-harness
export H0_FITTINGS_PATH=~/omarchy-fitted-harness/fittings
cd ~/.config/hypr && ~/fitting-room/bin/h0
```

h0 picks the fitting whose root contains your working directory. `omarchy-live` is rooted at
`~/.config/hypr` and may write to your Omarchy and terminal configs. It is built from
`omarchy-v5`, the version the evals measured, which is rooted at the test fixture.

`bin/h0 doctor` checks Python, bubblewrap, the sandbox, your key and which fitting applies.

## See what changed

After each request h0 says how many files it changed. `/changes` in a session, or from outside:

```bash
~/fitting-room/bin/h0 changes
```

prints every file the last request changed, created or deleted under `~/.config/hypr`,
`~/.config/omarchy` and the terminal configs, with a diff. It reads the files themselves, so it
includes changes the agent made through shell commands, whatever its summary says. A backup copy
is named as a copy rather than printed. `--all` covers the whole session, and `--names` drops the
diffs.

## Undo

Inside a session, `/undo` puts back everything your last request changed under
`~/.config/hypr`, `~/.config/omarchy` and the terminal configs, including changes the agent
made through shell commands, and removes files it created. Files larger than 1 MB (wallpapers)
are not kept: if one changed, undo names it rather than claiming it was put back.

If a session was interrupted or killed, undo it from outside:

```bash
~/fitting-room/bin/h0 undo
```

That undoes the last request of the most recent session; `--session <id>` picks another. Run it
again to step further back.

## Uninstall

```bash
rm -rf ~/fitting-room ~/omarchy-fitted-harness ~/.local/state/h0 ~/.local/share/h0 ~/.cache/h0
```

Remove the `H0_FITTINGS_PATH` line if you added it to your shell profile, and the API key if you
stored one in the keyring (`secret-tool clear service harness-0 account anthropic-api`). h0
installs nothing system-wide.

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

On Omarchy 4.5 the measured fitting is `omarchy-v5`, which `omarchy-live` is built from. Against
no fitting on Claude Opus 5.5, 22 pairs: both arms passed every task. The fitting took fewer turns
(median 5 against 7) and less time (15 s against 19 s), but it did not cost less, because its map
lengthens every prompt. v5's guidance for writing shell plugins has not been measured.

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

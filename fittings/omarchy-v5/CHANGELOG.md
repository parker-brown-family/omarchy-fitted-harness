# Fitting changelog


## v2 — 2026-11-08 22:18

Proposed by the learning loop from 5 failed fitted trials (cost $0.124).

- **om-clock-seconds** — cause: fitting. The fitting's widget guidance always said to clone built-in plugins (shell-guide note, map 'Customizing a built-in widget', L4). All three fitted runs cloned the clock and swapped the layout id away from omarchy.clock. Vanilla runs just edited the existing widget's format option in shell.json.
- **om-autostart** — cause: model. The fitting already names o.launch_on_start for autostart.lua. Both fitted runs read helpers.lua, worried that the uwsm-app wrapper would not expand $HOME, and switched to o.exec_on_start. Nothing in the fitting suggested that. Vanilla used launch_on_start and passed, so a small map clarification is a cheap nudge.

Edits applied:
- updated trigger shell-guide
- edited map
- removed lesson L4
- edited map

Expected effect: Agents will change built-in widget settings in place in shell.json instead of cloning plugins, and will use the documented o.launch_on_start for login autostart; neither change affects the passing Hypr, theme or hook tasks.

## v3 — 2026-11-08 22:28

Proposed by the learning loop from 3 failed fitted trials (cost $0.095).

- **om-clock-seconds** — cause: fitting. All three fitted runs went digging through the packaged plugin source and then cloned the clock plugin under a new id. The map line 'Only to change a widget's code: run omarchy plugin clone...' presents cloning as a normal path, so the agents treated it as one, while vanilla simply edited the format option on the existing shell.json entry.
- **om-clock-seconds** — cause: fitting. Same failure on the Opus run. It read the widget's timer/format code, decided a clone was warranted, and renamed the bar entry, so the stock widget id no longer has the requested option.
- **om-clock-seconds** — cause: fitting. Same failure on the Haiku run. The shell-guide trigger only fires on before:edit, so it was injected after the clone had already happened through bash; the map's clone wording drove the choice.

Edits applied:
- edited map
- updated trigger shell-guide

Expected effect: Agents will set widget options directly on the stock shell.json entry instead of cloning plugins, which matches the vanilla behavior that passed, and the clone path stays available for explicit code-change requests.

## v5 — 2026-11-10

Made by hand from evidence, not by the learning loop. Kept only if the 11 Omarchy settings tasks
pass at least as often as on v4 with the same model.

- **exec_on_start is valid again.** v2 told agents to use `o.launch_on_start` "not exec_on_start",
  because a checker accepted only the first; the checker was corrected (PREREG amendment 1) and the
  map was not. Omarchy 4.5 defines `o.launch_on_start(cmd)` as `o.exec_on_start("uwsm-app -- " .. cmd)`
  (`/usr/share/omarchy/default/hypr/helpers.lua`, lines 187–195). The map now names both and when
  each applies. Issue 4.
- **Guides fire on the first touch, whatever the tool.** v3 and v4 fired the Hyprland and shell
  guides only before `edit`, and the theme guide only before `write`. A new plugin is made with
  `write`, so in the four-harness builds the Opacity and Screen Sleep plugins (all writes, no edits)
  never saw the shell guide; v3's own changelog had already met the same rule firing too late. All
  three now fire `before:*`. The Lua and JSON syntax checks also run after `write`, not only after
  `edit`.
- **Plugin habits.** A new trigger, only on paths under `.config/omarchy/plugins/`, carries the
  points the blind judge marked h0's plugins down on in `runs/builds-3/judge`: `bash -c` strings
  instead of argv, no restore on destruction, status that claimed an action that was skipped,
  settings without fallbacks or schema bounds, a widget shown before its first reading, widgets
  loaded by URL instead of the registry. Its effect on plugin quality is **not measured** by the
  settings gate; it only shows the habits do no harm there.
- Map header no longer pins 4.0.4; the system prompt now carries the installed version.

**Gate result (2026-11-10):** 22 of 22 for both v4 and v5 on Opus 5.5, under checks v2 (PREREG
amendment 12); cost ×1.05, within noise. Kept: it does no harm on the settings tasks. Its gains
(guides reaching new files, exec_on_start, plugin habits) are not measured by this suite.

**Omarchy 4.5 (2026-11-10, after the gate):** the box and the fixture are now 4.5. Its own
`bindings.lua` template and `hyprland.md` replace a bound key with `o.rebind`, added upstream
after 4.0.4. The map, the Hyprland guide trigger and lessons L1–L2 now say so, where they taught
`hl.unbind` then `o.bind`. Re-gated on the 4.5 fixture: PREREG amendment 13.

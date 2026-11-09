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

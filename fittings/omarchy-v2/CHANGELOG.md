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

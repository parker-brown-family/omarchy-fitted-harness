---
title: Omarchy 4
tags: [harness-0, research, omarchy]
updated: 2026-11-08
---

# Omarchy 4

Facts about the installed system (package `omarchy 4.0.4-1`; `/usr/share/omarchy/version`
still reads `4.0.0.alpha`), read from the machine on 2026-11-08. These are what an
Omarchy fitting has to get right.

## Layout

- `/usr/share/omarchy/` is the package: `bin/` (commands, also on `PATH`), `config/`
  (templates copied into `~/.config` on first run), `default/` (system defaults the user
  config `require`s), `shell/` (the Quickshell-based Omarchy shell and its plugins),
  `themes/`, `migrations/`, `install/`. Read it freely; never edit it, because
  `omarchy update` overwrites it.
- `~/.config/hypr/` holds the user's Hyprland config **in Lua**: `hyprland.lua`,
  `bindings.lua`, `input.lua`, `looknfeel.lua`, `autostart.lua`, `monitors.lua`. The
  hyprlang `.conf` format and `bind = …` lines are gone; `hyprsunset.conf` and `xdph.conf`
  remain.
- `~/.config/omarchy/shell.json` configures the bar and idle behaviour; Waybar is not used.
  `~/.config/omarchy/` also holds `themes/`, `hooks/<event>.d/`, `plugins/`, `extensions/`.

## The Lua API (from `default/hypr/helpers.lua`)

- `o.bind("SUPER + SHIFT + R", "Description", "command")` adds a binding;
  `hl.unbind("SUPER + SHIFT + R")` removes one. Many keys are already bound by default
  (Super+Shift+N is the editor, Super+Shift+F the file manager, Super+Print the colour
  picker), so a rebind needs the unbind first.
- `hl.config({ general = { gaps_in = 0, gaps_out = 0 } })` sets Hyprland variables; the
  template's own commented example also sets `border_size = 0`.
- `o.launch_on_start(cmd)` wraps `o.exec_on_start(o.launch(cmd))`; both are valid for
  autostart.

## The shell

- Bar layout lives in `shell.json` under `bar.layout.{left,center,right}`; each widget is
  `{ "id": "omarchy.clock", "format": "dddd HH:mm", … }`. Widget options are set there.
- Plugins come in kinds (bar, bar-widget, service, panel, background, agents).
  `omarchy plugin clone <id>` copies a built-in plugin into the user directory and
  switches the bar to the copy; Omarchy's `plugins.md` recommends it for customising a
  widget.
- `idle.lock` and `idle.screensaver` are in seconds.

## Security-relevant surfaces

- **Themes run code.** Hyprland requires a theme's `hyprland.lua` and `gum_env.lua` at
  login; Neovim loads `neovim.lua`. `omarchy theme install <git url>` strips those from a
  cloned theme and regenerates them from `colors.toml`; a theme copied in by hand keeps
  them.
- **Clipboard history is on disk** at `~/.local/state/omarchy/clipboard-history.json`
  (0644), written by `shell/plugins/clipboard/capture.sh`, skipped only for copies that
  carry the KDE password-manager hint. The shell watches the file and reloads it when it
  changes.
- **Agent skills are installed system-wide** at `default/agents/skills/` and linked into
  the agents' own skill folders, so every agent on an Omarchy machine gets the same
  instructions; a fitting can rely on them existing.

## What the evals showed about this

Frontier models find all of the above by reading `/usr/share/omarchy` in a few calls, so
a fitting adds little knowledge. Where it helped was steering: Omarchy's docs recommend
cloning a plugin to customise a widget, and a fitting that says "format options go in
`shell.json`" keeps a model on the one-line change ([omarchy](https://github.com/parker-brown-family/omarchy-fitted-harness/blob/main/docs/results/omarchy.md)).

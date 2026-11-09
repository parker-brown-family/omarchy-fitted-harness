# Omarchy 4.0.4 user config (project root = `~`)

This is end-user customization of an installed Omarchy desktop (Arch + Hyprland + Quickshell `omarchy-shell`). It is NOT Omarchy source development, so no `omarchy dev ...`. The project root is `$HOME`, and all editable files live under `.config/`.

## Authoritative reference (read-only)
`/usr/share/omarchy/` (`$OMARCHY_PATH`) belongs to the package. **Read it freely, never edit it**: `omarchy update` overwrites it.
- Topic guides: `/usr/share/omarchy/default/agents/skills/omarchy/{SKILL,hyprland,plugins,theming,hooks,capture}.md`. Read the matching one before editing.
- Default Hyprland Lua: `/usr/share/omarchy/default/hypr/*` (window-rule examples are in `windows.lua`).
- Default shell config: `$OMARCHY_PATH/config/omarchy/shell.json`.
- Stock themes: `/usr/share/omarchy/themes/<slug>/`.
- Built-in plugins: `$OMARCHY_PATH/shell/plugins/`.
- Theme templates: `$OMARCHY_PATH/default/themed/*.tpl`.
- Command source: `cat $(which omarchy-<cmd>)`.

## Layout
```
.config/hypr/hyprland.lua      main; loads Omarchy defaults, then user files (user wins)
.config/hypr/bindings.lua      o.bind(...) / hl.unbind(...)
.config/hypr/monitors.lua      hl.monitor({ output=, mode=, position=, scale= })
.config/hypr/input.lua         keyboard/mouse
.config/hypr/looknfeel.lua     gaps, borders, animations, blur, opacity
.config/hypr/autostart.lua     o.launch_on_start(...)
.config/hypr/hyprsunset.conf   night light (separate process; hyprctl ignores it)
.config/hypr/xdph.conf         screen-share portal (applies on portal restart / next login)
.config/omarchy/shell.json     bar layout, plugins, idle (hot-reloads)
.config/omarchy/plugins/<id>/  user-owned shell plugins (hot-reload)
.config/omarchy/extensions/omarchy-menu.jsonc  launcher menu (JSONC, hot-reloads)
.config/omarchy/themes/<slug>/ custom or overlay themes
.config/omarchy/themed/<name>.tpl  per-app template override for all themes
.config/omarchy/backgrounds/<theme-slug>/  extra backgrounds
.config/omarchy/hooks/<event>.d/   hook scripts
.config/{alacritty/alacritty.toml,foot/foot.ini,kitty/kitty.conf,ghostty/config}
```

## Build / test
There is no build and no test suite. Offline checks:
- `luac -p` on Lua files.
- `python3 -m json.tool` on `*.json`. Not the `.jsonc` menu, which allows comments.
- `tomllib` on TOML files.
- `bash -n` on shell scripts.

Live validation needs the running desktop, so tell the user to run it (it is likely unavailable in the sandbox):
- Hyprland Lua: `hyprctl reload && hyprctl configerrors`, repeated until clean.
- hyprsunset: `omarchy restart hyprsunset`.
- Terminals: `omarchy restart terminal`.
- Shell: hot-reloads; to force it, use `omarchy-shell shell rescanPlugins`.

## Conventions
- Hyprland config is **Lua**, not hyprlang `.conf`. Use the `hl.*` and `o.*` helpers: `hl.config`, `o.bind`, `hl.unbind`, `o.launch_on_start`, `o.window(match, rules)`, `hl.monitor`.
- Keybinding format:
  - `o.bind("SUPER + SHIFT + R", "SSH", "alacritty -e ssh host")`
  - `o.bind("SUPER + B", "Browser", { launch = "chromium" })`
- Rebinding an existing key: check `omarchy menu keybindings --print`, then put `hl.unbind("SUPER + F")` BEFORE the new `o.bind`. Tell the user what the key was previously bound to.
- Window rules: the syntax changes often between Hyprland versions. The guide says to fetch https://wiki.hypr.land/Configuring/Basics/Window-Rules/, but the sandbox has no network. Copy patterns from `$OMARCHY_PATH/default/hypr/windows.lua` and flag uncertainty to the user.
- The bar is the Omarchy shell (`shell.json`), **not Waybar**. Prefer `omarchy bar move <id> --section left|center|right`.
- `idle.screensaver` and `idle.lock` are seconds since idle began (lock after 10 min = `600`).
- Customizing a built-in widget:
  - Run `omarchy plugin clone omarchy.<name>`, then edit `.config/omarchy/plugins/<username>.<name>/`.
  - Cloning switches the bar to the clone.
  - Never edit the packaged copy.
- Themes:
  - Small tweak (overlay): same slug under `.config/omarchy/themes/<slug>/`, containing only the changed files (e.g. `colors.toml`).
  - Independent variant (fork): new slug.
  - Apply with `omarchy theme set <name>`.
- Repo-installed themes (with `.git`) drop `*.lua`, terminal configs and `vscode.json`. These are regenerated from `colors.toml`.
- Hooks:
  - Events: `battery-low`, `font-set`, `post-boot`, `post-update`, `pre-refresh-pacman`, `theme-set`.
  - Install with `omarchy hook install <event> <script>`.
  - Scripts live in `.config/omarchy/hooks/<event>.d/` and receive their arg in `$1`.
- Back up before editing: `cp f f.bak.$(date +%s)`.
- Prefer the `omarchy <group> <action>` CLI. Use `omarchy commands` or `omarchy <group> --help` to discover commands.
- Packages: `omarchy pkg add` (AUR: `omarchy pkg aur add`).
- Reminders: `omarchy reminder <minutes> "Title"`.

## Traps
- Never write under `/usr/share/omarchy/`.
- `omarchy refresh ...` and `omarchy reinstall` overwrite user config (with a backup). **Ask the user for confirmation first.**
- Always run `omarchy debug --no-sudo --print`; without those flags it hangs on sudo.
- Privilege: use `sudo` in a visible terminal and `pkexec` when non-interactive (as an agent). Don't wrap commands that elevate themselves.
- `hyprsunset.conf` and `xdph.conf` are not validated by `hyprctl`.
- `omarchy-menu.jsonc` is JSONC: `json.tool` will reject it.

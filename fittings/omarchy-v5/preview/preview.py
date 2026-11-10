#!/usr/bin/env python3
"""Load Omarchy shell plugins (or a theme) in Quickshell offscreen and report what happened.

    preview.py                      every plugin under ~/.config/omarchy/plugins
    preview.py <plugin-dir> ...     these plugins
    preview.py --theme <theme-dir>  a bar strip drawn in that theme's colours

For each entry point in a plugin's manifest it prints whether it loaded, the QML errors that
point into the plugin's own files, and the text the entry point drew. Bar widgets are also
saved as a picture under ./.h0-preview/. Exit status 1 when any plugin has an error.

Nothing is shown on a display (QT_QPA_PLATFORM=offscreen). Popup windows (PanelWindow) need a
layer-shell compositor, so their code is loaded but they cannot be drawn here.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHELL = Path("/usr/share/omarchy/shell")
DEFAULT_THEME = Path("/usr/share/omarchy/themes/tokyo-night")
NOISE = ("does not support setting window masks",)


def stub(src: str) -> str:
    """An invisible stand-in for a popup type that needs a layer-shell compositor. It keeps the
    real type's properties, signals and function signatures, so a plugin that uses them still has
    to use them correctly, but nothing is drawn."""
    out = ["import QtQuick", "import Quickshell", "import qs.Commons", "", "Item {", "  id: root", "  visible: false",
           "  Item { id: stubHolder }"]
    depth = 0
    for line in src.splitlines():
        s = line.strip()
        if depth == 1 and not s.startswith("//"):
            if s.startswith("default property alias"):
                name = s.split()[3].rstrip(":")
                out.append(f"  default property alias {name}: stubHolder.data")
            elif s.startswith(("property ", "readonly property ", "required property ")):
                words = s.replace("readonly ", "").replace("required ", "").split()
                if len(words) >= 3 and words[1] != "alias":
                    out.append(f"  property {words[1]} {words[2].rstrip(':')}")
            elif s.startswith("signal "):
                out.append("  " + s)
            elif s.startswith("function ") and "(" in s:
                out.append("  " + s.split("{")[0].rstrip() + " { return arguments.length ? arguments[0] : null }")
        depth += line.count("{") - line.count("}")
    out.append("}")
    return "\n".join(out) + "\n"


def stage(theme: Path) -> tuple[Path, Path]:
    d = Path(tempfile.mkdtemp(prefix="h0-preview-"))
    for m in ("Commons", "services", "plugins"):
        (d / m).symlink_to(SHELL / m)
    ui = d / "Ui"
    ui.mkdir()
    for f in (SHELL / "Ui").iterdir():
        text = f.read_text(errors="replace") if f.suffix == ".qml" else ""
        if "PanelWindow {" in text:
            (ui / f.name).write_text(stub(text))
        else:
            (ui / f.name).symlink_to(f)
    (d / "shell.qml").write_text((HERE / "shell.qml").read_text())
    (d / "FakeBar.qml").write_text((HERE / "FakeBar.qml").read_text())
    home = d / "home"
    cur = home / ".local/state/omarchy/current"
    cur.mkdir(parents=True)
    (cur / "theme").symlink_to(theme.resolve())
    real_config = Path(os.environ.get("HOME", "/nonexistent")) / ".config"
    if real_config.is_dir():
        (home / ".config").symlink_to(real_config)
    return d, home


def run(d: Path, home: Path, extra: dict, timeout: int = 30) -> list[str]:
    xdg = d / "xdg"
    xdg.mkdir(mode=0o700)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QT_QPA_PLATFORM": "offscreen", "XDG_RUNTIME_DIR": str(xdg),
           "HOME": str(home), "LANG": os.environ.get("LANG", "C.UTF-8"), **extra}
    try:
        p = subprocess.run(["qs", "-p", str(d / "shell.qml")], capture_output=True, text=True, env=env, timeout=timeout)
        out = p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        dec = lambda b: b.decode(errors="replace") if isinstance(b, bytes) else (b or "")
        out = dec(e.stdout) + dec(e.stderr)
        out += "\nPREVIEW_TIMEOUT the entry point did not finish loading within %ss" % timeout
    return [l.replace("\x1b[0m", "").replace("\x1b[33m", "").replace("\x1b[97m", "").replace("\x1b[32m", "").replace("\x1b[31m", "")
            for l in out.splitlines()]


def problems(lines: list[str], plugin_dir: Path) -> list[str]:
    key = str(plugin_dir.resolve())
    bad = []
    for l in lines:
        if any(n in l for n in NOISE):
            continue
        if "PREVIEW_LOAD_ERROR" in l or "PREVIEW_TIMEOUT" in l or (key in l and ("WARN" in l or "ERROR" in l)):
            bad.append(l.strip())
    return bad


def texts(lines: list[str]) -> list[str]:
    return [l.split("PREVIEW_TEXT ", 1)[1].strip() for l in lines if "PREVIEW_TEXT " in l]


def preview_plugin(pdir: Path, shots: Path, theme: Path) -> bool:
    try:
        manifest = json.loads((pdir / "manifest.json").read_text())
    except (OSError, ValueError) as e:
        print(f"plugin {pdir.name}: cannot read manifest.json ({e})")
        return False
    pid = manifest.get("id", pdir.name)
    print(f"plugin {pid}  ({pdir})")
    ok = True
    entries = manifest.get("entryPoints") or {}
    if not entries:
        print("  no entryPoints in manifest.json")
        return False
    for kind, rel in entries.items():
        f = (pdir / rel).resolve()
        if not f.is_file():
            print(f"  {kind}: {rel} does not exist")
            ok = False
            continue
        d, home = stage(theme)
        shot = shots / f"{pid}-{kind}.png" if kind == "barWidget" else None
        lines = run(d, home, {"WIDGET": f.as_uri(), "MODULE": pid, "SHOT": str(shot) if shot else ""})
        bad = problems(lines, pdir)
        drew = list(dict.fromkeys(texts(lines)))
        status = "errors" if bad else "loaded"
        print(f"  {kind}: {rel}: {status}" + (f"; drew: {' | '.join(drew)[:300]}" if drew else "; drew no text"))
        if shot and shot.exists():
            print(f"    picture: {shot}")
        for b in bad[:20]:
            print(f"    {b[:400]}")
        ok = ok and not bad
    return ok


def main(argv: list[str]) -> int:
    shots = Path(os.environ.get("PREVIEW_SHOTS", ".h0-preview")).resolve()
    shots.mkdir(parents=True, exist_ok=True)
    if argv[:1] == ["--theme"]:
        theme = Path(argv[1]).resolve()
        d, home = stage(theme)
        shot = shots / f"theme-{theme.name}.png"
        lines = run(d, home, {"STRIP": "1", "SHOT": str(shot)})
        bad = [l.strip() for l in lines if ("WARN" in l or "ERROR" in l) and not any(n in l for n in NOISE)
               and ("colors" in l or str(theme) in l or "Color" in l)]
        print(f"theme {theme.name}: {'errors' if bad else 'drawn'}; drew: {' | '.join(texts(lines))[:200]}")
        if shot.exists():
            print(f"  picture: {shot}")
        for b in bad[:20]:
            print(f"  {b[:400]}")
        return 1 if bad or not shot.exists() else 0
    theme = Path(os.environ.get("PREVIEW_THEME", DEFAULT_THEME))
    dirs = [Path(a) for a in argv] or sorted(p.parent for p in (Path.home() / ".config/omarchy/plugins").glob("*/manifest.json"))
    if not dirs:
        print("no plugins found under ~/.config/omarchy/plugins")
        return 1
    results = [preview_plugin(p, shots, theme) for p in dirs]
    print("PREVIEW: " + ("ok" if all(results) else "FAILED"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

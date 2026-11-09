cat >> .config/hypr/bindings.lua <<'LUA'

hl.unbind("SUPER + SHIFT + N")
o.bind("SUPER + SHIFT + N", "File manager", "uwsm-app -- nautilus --new-window")
LUA

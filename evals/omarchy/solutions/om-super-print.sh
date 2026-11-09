cat >> .config/hypr/bindings.lua <<'LUA'

hl.unbind("SUPER + PRINT")
o.bind("SUPER + PRINT", "Screenshot", "omarchy-capture-screenshot")
LUA

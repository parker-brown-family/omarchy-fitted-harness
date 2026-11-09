python3 - <<'PY'
import json
p='.config/omarchy/shell.json'
d=json.load(open(p))
for side in d['bar']['layout'].values():
    for w in side:
        if w.get('id')=='omarchy.clock':
            w['format']='dddd HH:mm:ss'
json.dump(d,open(p,'w'),indent=2)
PY

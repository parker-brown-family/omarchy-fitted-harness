python3 - <<'PY'
import json
p='.config/omarchy/shell.json'; d=json.load(open(p)); d['bar']['position']='bottom'; json.dump(d,open(p,'w'),indent=2)
PY

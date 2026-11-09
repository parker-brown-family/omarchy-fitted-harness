python3 - <<'PY'
import json
p='.config/omarchy/shell.json'; d=json.load(open(p)); d['idle']['lock']=600; json.dump(d,open(p,'w'),indent=2)
PY

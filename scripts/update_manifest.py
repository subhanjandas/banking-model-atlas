"""Refresh release checksums after intentional edits; not needed to run the app."""
import hashlib
import json
import os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
excluded={'.git','node_modules','dist','__pycache__','.venv','playwright-report','test-results'}
files=[]
for directory,dirs,names in os.walk(root):
    dirs[:]=sorted(d for d in dirs if d not in excluded)
    for name in sorted(names):
        path=Path(directory)/name
        if name=='MANIFEST.json' or name.startswith('.env') or name=='.DS_Store' or path.suffix in {'.pyc','.duckdb'}:continue
        files.append({'path':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(root/'MANIFEST.json').write_text(json.dumps({'version':'0.3.0','checkpoint':'Banking scenarios and executable schema','files':sorted(files,key=lambda f:f['path'])},indent=2)+'\n')
print(f'Manifest refreshed: {len(files)} files.')

"""Check the release manifest without changing project files."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
errors=[]
for item in manifest['files']:
    path=root/item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        errors.append(item['path'])
if errors:raise SystemExit('Missing or modified release files: '+', '.join(errors))
print(f'All {len(manifest["files"])} release file checksums match.')

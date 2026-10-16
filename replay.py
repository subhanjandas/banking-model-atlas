"""Run the foundation checks from any working directory."""
import subprocess
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
for args in (['scripts/validate_model.py'],['-m','unittest','discover','-s','tests','-v'],['scripts/render_docs.py','--check'],['scripts/export_sql.py','--check'],['scripts/run_demo.py','--check-report']):
    subprocess.run([sys.executable,*args],cwd=root,check=True)
print('Model and synthetic SQL replay passed. Browser tests run separately.')

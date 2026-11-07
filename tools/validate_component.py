"""Check the released component source content and preserved upstream ancestry."""
from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[1]
binding=json.loads((root/'SOURCE_BASELINE.json').read_text())
for row in binding['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root.resolve()) and path.is_file(),row['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],row['path']
subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',binding['upstream_revision'],'HEAD'],check=True)
print('PASS:',len(binding['files']),'released source files and upstream ancestry')

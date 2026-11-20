"""Copy original demonstration contracts; never evidence of actual approval."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(folder):
    folder.mkdir(parents=True,exist_ok=True)
    for name in ['requirements.json','design-review.md']:
        shutil.copyfile(ROOT/'examples/multi-board'/name,folder/name)
    return json.loads((folder/'requirements.json').read_text(encoding='utf-8'))

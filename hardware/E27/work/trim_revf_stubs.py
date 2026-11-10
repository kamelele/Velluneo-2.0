"""Trim only electrically open trace and via stubs reported by KiCad."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

from revd_integrate import blocks,kind

CLI = 'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
DANGLING = {'track_dangling','via_dangling'}
TRACK = {'segment','via','arc'}


def drc(board,report):
    subprocess.run([CLI,'pcb','drc','--refill-zones','--save-board','--schematic-parity',
                    '--format','json','-o',str(report),str(board)],check=True,capture_output=True)
    return json.loads(report.read_text(encoding='utf8'))


def trim(board):
    with tempfile.TemporaryDirectory(dir=Path('work')) as temp:
        output=Path(temp)/'drc.json'
        removed=0
        for iteration in range(16):
            findings=drc(board,output)
            assert not findings['unconnected_items'],findings['unconnected_items']
            assert not findings['schematic_parity'],findings['schematic_parity']
            ids={i['uuid'] for v in findings['violations'] if v['type'] in DANGLING for i in v['items']}
            other=[v for v in findings['violations'] if v['type'] not in DANGLING]
            if not ids:
                assert not other, other
                print(f'{board.name}: {removed} stubs removed; zero DRC violations')
                return
            existing=board.read_text(encoding='utf8')
            items=[]
            found=set()
            for item in blocks(existing):
                if kind(item) in TRACK:
                    m=re.search(r'\(uuid "([^"]+)"\)',item)
                    if m and m[1] in ids:
                        found.add(m[1])
                        continue
                items.append(item)
            assert found==ids,ids-found
            board.write_text('(kicad_pcb\n'+'\n'.join(items)+'\n)\n',encoding='utf8')
            try:
                recheck=drc(board,output)
                assert not recheck['unconnected_items'] and not recheck['schematic_parity']
            except Exception:
                board.write_text(existing,encoding='utf8')
                raise
            removed+=len(found)
        raise RuntimeError('Open stubs remain after 16 iterations')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('board',type=Path)
    args=ap.parse_args()
    trim(args.board)

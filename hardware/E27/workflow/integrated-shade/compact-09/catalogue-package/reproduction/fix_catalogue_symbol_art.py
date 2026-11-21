from pathlib import Path
HERE=Path(__file__).resolve().parent;p=HERE/'capture_stock.py';s=p.read_text();anchor=" elif k=='custom inductor':";assert anchor in s;s=s.replace(anchor,"  if r=='T1':art+=line((-5.08,0),(-2.54,0))+line((2.54,0),(5.08,0))\n"+anchor);p.write_text(s)
print('T1symbolgraphicconnectsdrawncoiltoitsunchangedpinends;nonetmapchange')

from pathlib import Path
HERE=Path(__file__).resolve().parent
s=(HERE.parent/'checker/tests.py').read_text().replace('intended-connectivity.A1.json','intended-connectivity.CAT01.json').replace('A1_graph_sha256','CAT_graph_sha256').replace('47-pad','46-pad').replace('all47pad','all46pad')
anchor=" execute('unsupported-arc-stops',arc,stop='Only straight PCB_TRACK')"
extra=""" execute('stock-T1-legacy-pin8-rejected',lambda b,p,n:p[('T1','2')].SetNumber('8'),stop='Exact native pad/net binding mismatch')
 def phantom(b,p,n):
  f=next(f for f in b.GetFootprints() if f.GetReference()=='T1');pad=k.PAD(f);pad.SetNumber('4');pad.SetAttribute(k.PAD_ATTRIB_SMD);pad.SetShape(k.PAD_SHAPE_RECT);pad.SetSize(v(1,1));ls=k.LSET();ls.AddLayer(k.F_Cu);pad.SetLayerSet(ls);pad.SetPosition(v(90,10));pad.SetNet(n['/LED_PLUS']);f.Add(pad)
 execute('stock-T1-phantom-NC4-rejected',phantom,stop='Exact native pad/net binding mismatch')
"""
s=s.replace(anchor,anchor+'\n'+extra);(HERE/'checker/tests.py').write_text(s)
print('CATcontrols prepared:original19geometry/bindingcontrols +2stockterminalregressions')

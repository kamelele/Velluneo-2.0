from pathlib import Path
import shutil
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10'
shutil.copyfile(D/'smoothing-plan.json',D/'smoothing-plan-pass1.json');shutil.copyfile(D/'geometry-input.json',D/'geometry-input-pass1.json');(D/'evidence').mkdir(exist_ok=True);shutil.copyfile(D/'.work/before-smoothing.kicad_pcb',D/'evidence/routing-input.kicad_pcb')
s=(D/'smooth_routes.py').read_text();a=s.index(' oldlen=sum(');insert='''
 if ch['group'][0]in {'DRAIN','PRIMARY_GND','NTC'} and len(ch['indices'])>=8:
  original_length=sum(math.dist(a,b)for a,b in zip(pts,pts[1:]));best_score=sum(math.dist(a,b)for a,b in zip(compact,compact[1:]))+.3*(len(compact)-1)
  for mid in pts[1:-1]:
   for shift in (.2,.4,.8,1.2):
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
     q=(mid[0]+dx*shift,mid[1]+dy*shift)
     for pa in candidates(pts[0],q):
      for pb in candidates(q,pts[-1]):
       trial=pa+pb[1:];length=sum(math.dist(a,b)for a,b in zip(trial,trial[1:]));score=length+.3*(len(trial)-1)
       if score>=best_score or length>original_length+min(.8,.04*original_length):continue
       if legalpath(trial,ch):compact=trial;best_score=score
'''
s=s[:a]+insert+s[a:];s=s.replace("newlen<=oldlen+.002","newlen<=oldlen+min(.8,.04*oldlen)+.002");(D/'finish_corners.py').write_text(s)
print('Prepared bounded corner finishing')

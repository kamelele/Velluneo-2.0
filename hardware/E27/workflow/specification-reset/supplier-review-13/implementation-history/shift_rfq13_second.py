from pathlib import Path
W=Path(__file__).resolve().parent
s=(W/'tune_rfq13_native.py').read_text().replace("[('R10',-.5,0),('C3',0,.6),('R17',0,.4)]","[('C3',-1.5,-.6),('R17',.35,0)]").replace("'local-placement-refinement.json'","'local-placement-pass2.json'").replace("'.work/probe2'","'.work/probe3'")
exec(compile(s,str(W/'tune_rfq13_native.py'),'exec'))

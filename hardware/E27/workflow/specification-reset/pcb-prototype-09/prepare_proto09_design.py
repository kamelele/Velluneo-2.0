from pathlib import Path
import pcbnew,json,shutil
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';S=P/'pcb-driver-08/design';D=P/'pcb-prototype-09/design';shutil.copytree(S,D,ignore=shutil.ignore_patterns('checks','.work','*.kicad_prl'),dirs_exist_ok=True);B=D/'Velluneo_driver.kicad_pcb';pro=B.with_suffix('.kicad_pro');j=json.loads(pro.read_text());r=j['board']['design_settings']['rules'];r.update(min_text_height=1.0,min_text_thickness=.15,min_silk_clearance=.15)
sev=j['board']['design_settings']['rule_severities'];print('inherited ignored', [k for k,v in sev.items()if v=='ignore']);sev['silk_over_copper']='warning';sev['silk_edge_clearance']='warning';sev['silk_overlap']='warning'
b=pcbnew.LoadBoard(str(B));s=b.GetDesignSettings();s.m_MinSilkTextHeight=pcbnew.FromMM(1);s.m_MinSilkTextThickness=pcbnew.FromMM(.15);s.m_SilkClearance=pcbnew.FromMM(.15)
for f in b.GetFootprints():
 t=f.Reference();t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(1),pcbnew.FromMM(1)));t.SetTextThickness(pcbnew.FromMM(.15))
 for g in f.GraphicalItems():
  if g.GetLayer()in(pcbnew.F_SilkS,pcbnew.B_SilkS)and isinstance(g,pcbnew.PCB_SHAPE)and g.GetWidth()<pcbnew.FromMM(.15):g.SetWidth(pcbnew.FromMM(.15))
pcbnew.SaveBoard(str(B),b);pro.write_text(json.dumps(j,indent=2)+'\n');print('Copied selected project and strengthened only silk fabrication limits')

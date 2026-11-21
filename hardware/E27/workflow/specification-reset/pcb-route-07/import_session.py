from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;F=D/'routing';S=D/'studies/sense';ses=F/'jvm-output.ses';assert ses.exists()and ses.stat().st_size>100
contract=json.loads((F/'input-contract.json').read_text());assert hashlib.sha256((S/'ground-seed.kicad_pcb').read_bytes()).hexdigest()==contract['native_source_sha256']
run=json.loads((F/'jvm-execution.json').read_text());assert hashlib.sha256(ses.read_bytes()).hexdigest()==run['output_ses_sha256'];assert hashlib.sha256((F/'input-scoped.dsn').read_bytes()).hexdigest()==run['input_dsn_sha256']
b=pcbnew.LoadBoard(str(F/'.work/import-base.kicad_pcb'));assert not b.GetTracks();assert pcbnew.ImportSpecctraSES(b,str(ses));out=S/'Velluneo_route07.kicad_pcb';pcbnew.SaveBoard(str(out),b)
(F/'native-import.json').write_text(json.dumps(dict(input_contract_sha256=hashlib.sha256((F/'input-contract.json').read_bytes()).hexdigest(),session_sha256=hashlib.sha256(ses.read_bytes()).hexdigest(),native_board_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),scope='Actual native import; saved DRC/parity/connectivity/protected-copper checks required. No completion assumed from exitstatus.'),indent=2)+'\n')
print(out)

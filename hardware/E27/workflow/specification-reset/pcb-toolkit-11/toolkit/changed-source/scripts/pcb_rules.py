"""Compose and check KiCad projects. Python 3.11+, standard library only.

init does not invent product requirements or approvals. check always writes a report.
Return codes: 0 pass; 1 findings/incomplete; 2 invalid configuration/tool failure.
"""
import argparse
import copy
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import configuration as configuration
import product_contracts
import connectivity
import spatial
import scoped_policy
import toolkit_install

ROOT = Path(__file__).resolve().parents[1]
STAGES = ['specification', 'schematic', 'placement', 'routing', 'release']
LIMITS = ['clearance', 'track_width', 'hole_size', 'annular_width', 'edge_clearance']


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe_path(folder, name):
    target = (folder / name).resolve()
    if not target.is_relative_to(folder.resolve()):
        raise ValueError('Path outside project: '+str(name))
    return target


def resolve(config):
    vendor, assembly = config['fabrication']['vendor'], config['assembly']['mode']
    if vendor not in ['jlcpcb', 'eurocircuits'] or assembly not in ['supplier', 'inhouse']:
        raise ValueError('Select vendor jlcpcb/eurocircuits and assembly supplier/inhouse')
    fab = read(ROOT / 'profiles' / (vendor+'.json'))
    asm = read(ROOT / 'profiles' / ('assembly-'+assembly+'.json'))
    values = {}
    for key in LIMITS:
        value = config.get('product', {}).get('minimums_mm', {}).get(key, 0)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ValueError('Invalid product minimum: '+key)
        values[key] = max(fab['design_preferences_mm'][key], value)
    return fab, asm, values


def dru(values):
    # Factory floor plus stricter per-product values; no ad-hoc scope overrides.
    return '(version 1)\n'+''.join(
        f'(rule "HW-{key}" (constraint {key} (min {values[key]:.6f}mm)))\n'
        for key in LIMITS)


def project_settings(name, values, classes):
    pro = read(ROOT / 'templates/kicad/board.kicad_pro')
    pro['meta']['filename'] = name+'.kicad_pro'
    rules = pro['board']['design_settings']['rules']
    for key, target in [('clearance', 'min_clearance'), ('track_width', 'min_track_width'),
                        ('hole_size', 'min_through_hole_diameter'), ('annular_width', 'min_via_annular_width'),
                        ('edge_clearance', 'min_copper_edge_clearance')]:
        rules[target] = values[key]
    pro['net_settings']['classes'] = []
    defaults = {'name': 'Default', 'clearance': values['clearance'],
                'track_width': max(.254, values['track_width']), 'via_diameter': 1.27,
                'via_drill': .7112, 'diff_pair_width': .254, 'diff_pair_gap': .254,
                'diff_pair_via_gap': .254, 'wire_width': 6, 'bus_width': 12,
                'line_style': 0, 'pcb_color': 'rgba(0, 0, 0, 0.000)',
                'schematic_color': 'rgba(0, 0, 0, 0.000)'}
    pro['net_settings']['classes'].append(defaults)
    patterns = []
    names = set()
    assigned = set()
    for cls in classes:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_ -]*', cls['name']) or cls['name']=='Default':
            raise ValueError('Invalid or reserved netclass name')
        if cls['name'] in names:
            raise ValueError('Duplicate netclass name')
        names.add(cls['name'])
        item = {**defaults, 'name': cls['name']}
        for key in ['clearance', 'track_width']:
            value = cls.get(key, defaults[key])
            if not isinstance(value, (int, float)) or isinstance(value,bool) or not math.isfinite(value) or value < values[key]:
                raise ValueError('Netclass weakens constraint: '+key)
            item[key] = value
        pro['net_settings']['classes'].append(item)
        for net in cls['nets']:
            if not isinstance(net,str) or not net or net in assigned:
                raise ValueError('Invalid or duplicate netclass assignment')
            if any(ch in net for ch in '*?[]') and (patterns or sum(len(c['nets']) for c in classes)>1):
                raise ValueError('Multiple wildcard assignments need manual scope validation')
            assigned.add(net)
            patterns.append({'netclass': cls['name'], 'pattern': net})
    pro['net_settings']['netclass_patterns'] = patterns
    return pro


def configuration_plan(folder, config):
    toolchain=toolkit_install.identity(folder,ROOT)
    _, _, values = resolve(config)
    name = config['name']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
        raise ValueError('Project name must use letters, digits, hyphens or underscores')
    pro = scoped_policy.apply_to_expected(project_settings(name, values, config.get('netclasses', [])),config)
    scoped_policy.validate_board(folder,config)
    extra, conflicts, model = spatial.prepare(folder,config,values,pro['net_settings'])
    dependencies = {'version': (ROOT/'VERSION').read_text().strip(), 'hashes': {}}
    for p in [Path(__file__), ROOT/'scripts/configuration.py', ROOT/'scripts/scoped_policy.py', ROOT/'VERSION',
              ROOT/'templates/kicad/board.kicad_pro', ROOT/'rules/catalog.json',
              ROOT/'scripts/product_contracts.py',
              ROOT/'scripts/connectivity.py',
              ROOT/'scripts/spatial.py', ROOT/'scripts/spatial_cad.py',
              ROOT/'scripts/toolkit_install.py', ROOT/'scripts/package_toolkit.py',
              ROOT/'profiles'/(config['fabrication']['vendor']+'.json'),
              ROOT/'profiles'/('assembly-'+config['assembly']['mode']+'.json')]:
        dependencies['hashes'][str(p.relative_to(ROOT))] = digest(p)
    dependencies['toolkit']=toolchain
    return configuration.build(folder, config, pro, dru(values)+spatial.rules(model)+scoped_policy.rules(config), dependencies,extra,conflicts)


def configure(folder, config, apply_plan=None):
    plan = configuration_plan(folder, config)
    if apply_plan is not None:
        return configuration.apply(folder, plan, apply_plan)
    return configuration.preview(folder, plan)


def source_files(folder, config):
    paths = [safe_path(folder, x) for x in config['source_files']]
    paths.extend(product_contracts.tracked_inputs(folder,config))
    paths.extend(connectivity.tracked_inputs(folder,config))
    paths.extend(spatial.tracked_inputs(folder,config))
    paths.extend(scoped_policy.migration_inputs(folder,config))
    if any(p.relative_to(folder.resolve()).parts and p.relative_to(folder.resolve()).parts[0].casefold()=='.pcb-toolkit' for p in paths):
        raise ValueError('Dependency store is reserved for tooling, not design source_files')
    if configuration.raw(folder, configuration.STATE) is not None:
        paths.append(configuration.path(folder, configuration.STATE).resolve())
    required = [folder/(config['name']+ext) for ext in ['.kicad_pro', '.kicad_dru', '.kicad_pcb', '.kicad_sch']]
    if any(p.resolve() not in paths for p in required):
        raise ValueError('source_files must include project, rules, board and schematic')
    # Ensure local libraries and hierarchical sheets are bound to reviews too.
    discovered = [p.resolve() for p in configuration.design_files(folder,['.kicad_sch','.kicad_sym','.kicad_mod'])]
    if any(p not in paths for p in discovered):
        raise ValueError('source_files omits local sheets/symbols/footprints')
    return sorted(set(paths))


def snapshot(folder, config):
    # Approval records and waivers do not sign themselves. All design configuration does.
    design = {k: v for k, v in config.items() if k not in ['approvals', 'waivers', 'release_files']}
    records = {str(p.relative_to(folder.resolve())).replace('\\', '/'): digest(p)
               for p in source_files(folder, config)}
    records['project-design-config'] = hashlib.sha256(json.dumps(design, sort_keys=True).encode()).hexdigest()
    records['toolkit:identity']=hashlib.sha256(json.dumps(toolkit_install.identity(folder,ROOT),sort_keys=True).encode()).hexdigest()
    for p in [ROOT/'VERSION', ROOT/'rules/catalog.json', ROOT/'profiles'/ (config['fabrication']['vendor']+'.json'),
              ROOT/'profiles'/('assembly-'+config['assembly']['mode']+'.json'), Path(__file__),
              ROOT/'scripts/configuration.py', ROOT/'scripts/scoped_policy.py', ROOT/'scripts/product_contracts.py', ROOT/'scripts/connectivity.py', ROOT/'scripts/spatial.py', ROOT/'scripts/spatial_cad.py', ROOT/'scripts/toolkit_install.py', ROOT/'scripts/package_toolkit.py', ROOT/'templates/kicad/board.kicad_pro']:
        records['ruleset:'+str(p.relative_to(ROOT)).replace('\\', '/')] = digest(p)
    return hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest(), records


def cli_path(arg):
    if arg:
        return arg
    if os.environ.get('KICAD_CLI'):
        return os.environ['KICAD_CLI']
    found = shutil.which('kicad-cli')
    if found:
        return found
    candidate = Path('C:/Program Files/KiCad/10.0/bin/kicad-cli.exe')
    if candidate.exists():
        return str(candidate)
    raise ValueError('Set KICAD_CLI or use --kicad-cli')


def run_tool(cli, args, folder):
    env = os.environ.copy()
    env['KICAD_CONFIG_HOME'] = str(folder/'.work/kicad-config')
    env['KICAD_DOCUMENTS_HOME'] = str(folder/'.work/kicad-documents')
    result = subprocess.run([cli, *args], cwd=folder, env=env, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=180)
    return {'command': [Path(cli).name, *args], 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def violations(report):
    result = []
    def visit(value):
        if isinstance(value, dict):
            if 'severity' in value and ('type' in value or 'description' in value):
                result.append(value)
            else:
                for v in value.values():
                    visit(v)
        elif isinstance(value, list):
            for v in value:
                visit(v)
    visit(report)
    return result


def contains(actual, expected):
    """Allow KiCad-added metadata/defaults, while preserving every policy field."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(k=='meta' or
            (k in actual and contains(actual[k],v)) for k,v in expected.items())
    if isinstance(expected, list):
        return isinstance(actual,list) and len(actual)==len(expected) and all(
            contains(a,e) for a,e in zip(actual,expected))
    return actual==expected


def waive(finding, waivers, current):
    signature = hashlib.sha256(json.dumps(finding, sort_keys=True).encode()).hexdigest()
    return any(w.get('finding_sha256')==signature and w.get('snapshot')==current
               and w.get('rule_id') and w.get('object_ids') and w.get('reason')
               and w.get('approved_by') and w.get('approval_evidence') for w in waivers)


def check(folder, config, mode, cli, stage='specification'):
    report = {'schema_version': 1, 'mode': mode, 'time_utc': datetime.now(timezone.utc).isoformat(),
              'ruleset_version': (ROOT/'VERSION').read_text().strip(), 'errors': [], 'commands': []}
    errors = report['errors']
    try:
        report['toolkit']=toolkit_install.identity(folder,ROOT)
        fab, asm, values = resolve(config)
        contract_file = config.get('product',{}).get('requirements_file')
        if contract_file:
            contract = product_contracts.evaluate(folder,contract_file,'release' if mode=='release' else stage)
            report['requirements'] = contract
            errors.extend('Requirements: '+e['id']+': '+e['message'] for e in contract['errors'])
        elif mode=='release':
            errors.append('Requirements contract missing: adopt product.requirements_file')
        else:
            report['requirements'] = {'status':'not_configured','release_blocked':True}
        name = config['name']
        if not re.fullmatch(r'[A-Za-z0-9_-]+',name):
            raise ValueError('Invalid project name')
        expected = scoped_policy.apply_to_expected(project_settings(name, values, config.get('netclasses', [])),config)
        scoped_policy.validate_board(folder,config)
        model=spatial.load(folder,config,values,expected['net_settings'])
        custom=dru(values)+spatial.rules(model)+scoped_policy.rules(config)
        actual = read(folder/(name+'.kicad_pro'))
        errors.extend(configuration.policy_errors(actual, expected))
        if configuration.pending(folder):
            errors.append('Unfinished configuration transaction; recovery required')
        state = configuration.load(folder, configuration.STATE)
        if state is None:
            errors.append('Ownership state missing: preview adoption with configure')
        elif (not isinstance(state,dict) or state.get('schema_version') != 1 or
              state.get('managed') != configuration.fields(expected) or
              state.get('dru_sha256') != configuration.sha(custom.encode())):
            errors.append('Ownership state is invalid or stale: preview adoption with configure')
        if (folder/(name+'.kicad_dru')).read_text(encoding='utf-8') != custom:
            errors.append('Custom rules differ from composed profile')
        current, hashes = snapshot(folder, config)
        report.update(snapshot=current, input_hashes=hashes, resolved_minimums_mm=values)
        if model:
            result=spatial.verify(folder,config,values,expected['net_settings']);report['spatial']=result
            errors.extend('Spatial: '+e for e in result['errors'])
        elif mode=='release':errors.append('Spatial contract missing: adopt product.spatial_file')
        else:report['spatial']={'status':'not_configured','release_blocked':True}
        version_result = run_tool(cli, ['version'], folder)
        report['commands'].append(version_result)
        match = re.search(r'\b(\d+\.\d+\.\d+)\b', version_result['stdout'])
        if version_result['exit_code'] or not match:
            raise ValueError('Could not identify KiCad version')
        report['kicad_version'] = match.group(1)
        if match.group(1) != config.get('kicad_version'):
            errors.append('KiCad exact version differs from project pin')
        if not match.group(1).startswith('10.0.'):
            errors.append('KiCad version family has not passed migration validation')
        if config.get('product',{}).get('connectivity_file'):
            result=connectivity.verify(folder,config,cli,run_tool)
            report['connectivity']=result
            report['commands'].extend(result['commands'])
            errors.extend('Connectivity: '+item['type']+': '+item['message'] for item in result['errors'])
            if result.get('configuration_error'):report['configuration_error']=True
        elif mode=='release':
            errors.append('Connectivity intent missing: adopt product.connectivity_file')
        else:
            report['connectivity']={'status':'not_configured','release_blocked':True}
        reports = folder/'.work'
        reports.mkdir(exist_ok=True)
        for kind, args in [('erc', ['sch', 'erc']), ('drc', ['pcb', 'drc'])]:
            output = reports/(kind+'.json')
            output.unlink(missing_ok=True)  # Never consume stale success.
            command = [*args, '--format', 'json', '--severity-all', '--exit-code-violations', '-o', str(output)]
            if kind=='drc':
                command += ['--refill-zones', '--schematic-parity']
            command += [str(folder/(name+('.kicad_sch' if kind=='erc' else '.kicad_pcb')))]
            run = run_tool(cli, command, folder)
            report['commands'].append(run)
            if not output.exists() or run['exit_code'] not in [0, 5]:
                errors.append('CAD tool failed: '+kind)
                continue
            raw = read(output)
            if not str(raw.get('$schema', '')).endswith('/'+kind+'.v1.json'):
                errors.append('Unsupported CAD report schema: '+kind)
                continue
            findings = violations(raw)
            report[kind] = {'report_sha256': digest(output), 'findings': findings}
            for f in findings:
                if not waive(f, config.get('waivers', []), current):
                    errors.append(kind+': '+f.get('type', f.get('description', 'finding')))
            if run['exit_code'] and not findings:
                errors.append('Nonzero CAD exit without decoded findings: '+kind)
        if mode=='release':
            f = config['fabrication']
            for key in ['service', 'stackup', 'copper', 'finish', 'confirmation_evidence']:
                if not f.get(key):
                    errors.append('Fabrication field missing: '+key)
            if f.get('service') not in fab['services']:
                errors.append('Service is outside selected fabrication profile')
            if not config['assembly'].get('confirmation_evidence'):
                errors.append('Assembly process not confirmed')
            if config['assembly']['mode']=='inhouse' and not config['assembly'].get('local_pcba_provider_confirmation'):
                errors.append('Local PCBA provider confirmation missing: assembly.local_pcba_provider_confirmation')
            product = config.get('product', {})
            if not product.get('domains'):
                errors.append('Product domain list missing')
            if product.get('special_requirements') and not product.get('standards_review_evidence'):
                errors.append('Special product/insulation requirements lack approved standards review')
            if product.get('barriers') and not all(all(b.get(k) is not None for k in
                    ['side_a', 'side_b', 'working_voltage', 'transient_voltage', 'pollution_degree',
                     'cti', 'altitude_m', 'clearance_mm', 'creepage_mm', 'standard_clause', 'evidence', 'approved_by'])
                    for b in product['barriers']):
                errors.append('Insulation barrier card incomplete')
            for stage in STAGES:
                a = config.get('approvals', {}).get(stage, {})
                if a.get('snapshot') != current or not a.get('approved_by') or not a.get('evidence'):
                    errors.append('Missing/stale user approval: '+stage)
            artifacts_digest = hashlib.sha256(json.dumps(config.get('release_files', {}), sort_keys=True).encode()).hexdigest()
            report['artifacts_digest'] = artifacts_digest
            if config.get('approvals', {}).get('release', {}).get('artifacts_digest') != artifacts_digest:
                errors.append('Release approval does not cover current artifacts')
            for kind in ['gerbers', 'drills', 'bom', 'positions', 'assembly_drawing', 'bringup_plan']:
                paths = config.get('release_files', {}).get(kind, [])
                if not paths:
                    errors.append('Release artifact missing: '+kind)
                for entry in paths:
                    artifact = safe_path(folder, entry['path'])
                    if not artifact.is_file() or artifact.stat().st_size==0 or digest(artifact)!=entry.get('sha256') or entry.get('snapshot')!=current:
                        errors.append('Missing/stale release artifact: '+kind)
        if snapshot(folder, config)[0] != current:
            errors.append('Source changed during verification')
    except Exception as e:
        errors.append(type(e).__name__+': '+str(e))
        report['configuration_error'] = True
    report['passed'] = not errors
    write(folder/'.work/check.json', report)
    return 0 if not errors else (2 if report.get('configuration_error') else 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'configure', 'snapshot', 'check','requirements','connectivity','spatial'])
    parser.add_argument('project', type=Path)
    parser.add_argument('--vendor', choices=['jlcpcb', 'eurocircuits'], default='jlcpcb')
    parser.add_argument('--assembly', choices=['supplier', 'inhouse'], default='inhouse')
    parser.add_argument('--mode', choices=['work', 'release'], default='work')
    parser.add_argument('--kicad-cli')
    parser.add_argument('--stage', choices=STAGES, default='specification')
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--apply', metavar='PLAN_ID')
    action.add_argument('--rollback', metavar='TRANSACTION_ID')
    args = parser.parse_args()
    folder = args.project.absolute()
    configuration.path(folder, '.')
    toolchain=toolkit_install.identity(folder,ROOT)
    if (args.apply or args.rollback) and args.command != 'configure':
        parser.error('--apply/--rollback require configure')
    cfg = folder/'hardware.json'
    if args.command=='init':
        for relative in ['hardware.json','AGENTS.md','.electronics-rules','requirements.json','intended-connectivity.json','spatial-constraints.json']:
            configuration.path(folder, relative)
        if not re.fullmatch(r'[A-Za-z0-9_-]+',folder.name):
            parser.error('Project name must use letters, digits, hyphens or underscores')
        if cfg.exists() or list(folder.glob('*.kicad_*')) or (folder/'AGENTS.md').exists() or (folder/'.electronics-rules').exists() or (folder/'requirements.json').exists() or (folder/'intended-connectivity.json').exists() or (folder/'spatial-constraints.json').exists():
            parser.error('Refusing to overwrite an existing project')
        folder.mkdir(parents=True, exist_ok=True)
        config = read(ROOT/'templates/project/hardware.json')
        config['name'] = folder.name
        config['fabrication']['vendor'] = args.vendor
        config['assembly']['mode'] = args.assembly
        config['source_files'] = [folder.name+e for e in ['.kicad_pro','.kicad_dru','.kicad_pcb','.kicad_sch']]
        write(cfg, config)
        shutil.copy(ROOT/'templates/project/requirements.json',folder/'requirements.json')
        shutil.copy(ROOT/'templates/project/intended-connectivity.json',folder/'intended-connectivity.json')
        shutil.copy(ROOT/'templates/project/spatial-constraints.json',folder/'spatial-constraints.json')
        plan = configure(folder, config)
        configure(folder, config, apply_plan=plan['id'])
        shutil.copy(ROOT/'templates/project/AGENTS.md', folder/'AGENTS.md')
        print('Profile prepared. Create schematic/board and complete hardware.json before review.')
        return 0
    if not folder.is_dir():
        parser.error('Project directory does not exist')
    if args.command=='configure' and args.rollback:
        configuration.rollback(folder, args.rollback)
        print('Original configuration restored. Rerun checks before review.')
        return 0
    config = read(cfg)
    if args.command=='spatial':
        try:
            _,_,values=resolve(config)
            settings=scoped_policy.apply_to_expected(project_settings(config['name'],values,config.get('netclasses',[])),config)
            scoped_policy.validate_board(folder,config)
            result=spatial.verify(folder,config,values,settings['net_settings'])
        except Exception as exc:
            result={'passed':False,'configuration_error':True,'errors':[type(exc).__name__+': '+str(exc)]}
        result['toolkit']=toolchain;write(folder/'.work/spatial.json',result)
        print(json.dumps(result,ensure_ascii=True,indent=2))
        return 0 if result['passed'] else (2 if result.get('configuration_error') else 1)
    if args.command=='connectivity':
        try:
            cli=cli_path(args.kicad_cli)
            result=connectivity.verify(folder,config,cli,run_tool)
        except (ValueError,OSError) as exc:
            result={'passed':False,'configuration_error':True,'errors':[{'type':'connectivity_check_failed','message':str(exc)}]}
        result['toolkit']=toolchain;write(folder/'.work/connectivity.json',result)
        print(json.dumps(result,ensure_ascii=True,indent=2))
        return 0 if result['passed'] else (2 if result.get('configuration_error') else 1)
    if args.command=='requirements':
        relative = config.get('product',{}).get('requirements_file')
        report = product_contracts.evaluate(folder,relative,args.stage)
        report['toolkit']=toolchain
        write(folder/'.work/requirements.json',report)
        print(json.dumps(report,ensure_ascii=True,indent=2))
        return 0 if report['passed'] else (2 if report.get('configuration_error') else 1)
    if args.command=='configure':
        if args.apply:
            transaction = configure(folder, config, apply_plan=args.apply)
            print('Transaction: '+transaction if transaction else 'No changes required.')
            return 0
        plan = configure(folder, config)
        print('Plan: '+plan['id'])
        print('Diff: .work/configure/plans/'+plan['id']+'.diff')
        for conflict in plan['conflicts']:
            print('CONFLICT: '+conflict)
        print('Close KiCad and review the diff before configure --apply PLAN_ID.')
        return 1 if plan['conflicts'] else 0
    if args.command=='snapshot':
        print(snapshot(folder, config)[0])
        return 0
    return check(folder, config, args.mode, cli_path(args.kicad_cli),stage=args.stage)


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        print('Configuration error: '+str(exc), file=sys.stderr)
        raise SystemExit(2)

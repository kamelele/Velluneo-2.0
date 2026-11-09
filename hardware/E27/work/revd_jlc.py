"""Package the single-board JLCPCB files and verify their source geometry and pin mapping."""
from collections import Counter, defaultdict
import csv
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

import pcbnew as pcb

from revd_integrate import DEST, GUARD, MAIN, NAME, OUT, guard_net, ref_name

JLC = 'https://jlcpcb.com/partdetail/'
LCSC = 'https://www.lcsc.com/product-detail/'
CATALOG = {
    'RT0603BRD07330KL': 'C861327',
    'RP0603BRD075K62L': 'C5889719',
    'PMEG6010CEH-QX': 'C5311567',
    'RC0805FR-072K2L': 'YAGEO-RC0805FR072K2L/C114561',
    'C3216X5R1V226M160AC': 'C69612',
    'ERJ-8GEYJ105V': 'C278663',
    'CC0603KRX7R9BB331': 'C107087',
    'ERJ-6ENF1000V': 'PANASONIC-ERJ6ENF1000V/C193990',
    'CC0603KRX7R9BB473': 'C107093',
    'ERJ-3EKF3012V': 'C403145',
    'ERA-3AEB103V': 'PANASONIC-ERA3AEB103V/C190610',
    'ERJ-3EKF1002V': 'C191124',
    'ERJ-3EKF5901V': 'C403290',
    'BAT54WS-7-F': 'C124205',
    'ERA-3AEB223V': 'C445636',
    'ERJ-3EKF2202V': 'C278611',
    'ERJ-3EKF2201V': 'PANASONIC-ERJ3EKF2201V/C116387',
    'CC0603KRX7R9BB103': 'C100042',
    'ERJ-3EKF1003V': 'C189597',
    'ERA-3AEB114V': 'PANASONIC-ERA3AEB114V/C473255',
    'LYT6073C-TL': 'C567768',
    'TPS26600PWPR': 'TexasInstruments-TPS26600PWPR/C544399',
    'AL5812MP-13': 'C460648',
    'MB10S': 'onsemi-MB10S/C480680',
    'TPS7A1633DGNR': 'C181239',
    'TLV1702AIDGKR': 'TexasInstruments-TLV1702AIDGKR/C2870937',
    'SN74HCS74PWR': 'C2866652',
    'SN74LVC1G132DBVR': 'C403723',
    'AQY212GS': 'Panasonic-AQY212GS/C719745',
    'TMOV14RP275E': 'Littelfuse-TMOV14RP275E/C1528070',
    'UCM1H471MNJ1MS': 'C3828881',
    '440LD22-R': 'C511032',
    '768772102': 'WurthElektronik-768772102/C7194056',
    'US1J-13-F': 'C85095',
    'US1B-13-F': 'C154439',
    'SK3200B-LTP': 'C138792',
    'BZT52C18-7-F': 'C192739',
    'BZT52C27-7-F': 'C163720',
    'BAV21W-7-F': 'C155214',
    'C3225X7R2A225K230AB': 'C2167827',
    'GRM21BC71E106KE11L': 'C109040',
    'ERA-3AEB1333V': 'C2087399',
    'ERA-3AEB2263V': 'C2075582',
    'GRM21BR71H104KA01L': 'MurataElectronics-GRM21BR71H104KA01L/C77082',
    'GRM21BR71H474KA88L': 'C86043',
    'C3225X7T2J104KT000N': 'C342668',
    'MMBT5551LT1G': 'C41095',
    'CRCW2010510KFKEF': 'C4245382',
    'CRCW20102M20FKEF': 'C4263855',
    'ERJ-6ENF1002V': 'C169253',
    'ERJ-3EKF2490V': 'PANASONIC-ERJ3EKF2490V/C403099',
    'CGA3E3X7R1H224K080AE': 'TDK-CGA3E3X7R1H224K080AE/C2171795',
    'C1608X7R1H104K080AE': 'TDK-C1608X7R1H104K080AE/C2167477',
}
SELECTED_PARTS = {
    'R11': 'RP0603BRD075K62L',
    'R12': 'RC0805FR-072K2L',
    'R105': 'RT0603BRD07330KL',
    'R107': 'RT0603BRD07330KL',
    'D102': 'PMEG6010CEH-QX',
    'D103': 'PMEG6010CEH-QX',
    'D101': 'BAT54WS-7-F',
    'R101': 'ERJ-3EKF2202V',
    'R109': 'ERJ-3EKF2202V',
    'R102': 'ERJ-3EKF2201V',
    'R110': 'ERJ-3EKF1003V',
    'R112': 'ERJ-3EKF1003V',
    'C103': 'CC0603KRX7R9BB103',
    'C106': 'CC0603KRX7R9BB103',
    'C108': 'CC0603KRX7R9BB103',
    'R2': 'CRCW2010510KFKEF', 'R3': 'CRCW2010510KFKEF',
    'R6': 'CRCW20102M20FKEF', 'R7': 'CRCW20102M20FKEF',
    'R111': 'ERJ-3EKF2490V',
    'C104': 'CGA3E3X7R1H224K080AE', 'C105': 'CGA3E3X7R1H224K080AE',
    'C107': 'C1608X7R1H104K080AE', 'C109': 'C1608X7R1H104K080AE',
    'C110': 'C1608X7R1H104K080AE',
}
HV_RESISTORS = {'R2', 'R3', 'R6', 'R7'}
# Quote candidates use exact parts only. Explicitly track items requiring separate sourcing.
HOLD_FROM_CATALOG = {'L1': 'Zapas JLCPCB do potwierdzenia. Poprzedni odczyt 0.',
                     'U103': 'Zapas do potwierdzenia. Poprzedni odczyt LCSC 0.'}


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, fields, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def by_ref(board):
    return {fp.GetReference(): fp for fp in board.GetFootprints()}


def nets(footprints):
    return {(ref, pad.GetNumber()): pad.GetNetname() for ref, fp in footprints.items()
            for pad in fp.Pads() if pad.GetNetname()}


def verify_design(board, footprints, positions):
    base = by_ref(pcb.LoadBoard(str(OUT / MAIN / f'{MAIN}.kicad_pcb')))
    guard = by_ref(pcb.LoadBoard(str(OUT / GUARD / f'{GUARD}.kicad_pcb')))
    intended = nets(base)
    intended['J2', '2'] = '/S1_RETURN'
    for (ref, pin), net in nets(guard).items():
        if ref != 'J1':
            intended[ref_name(ref), pin] = guard_net(net, ref, ref_name(ref))
    source = ET.parse('work/revd_netlist.xml').getroot()
    schematic = {(node.get('ref'), node.get('pin')): net.get('name')
                 for net in source.findall('./nets/net') for node in net.findall('node')}
    assert intended == nets(footprints) == schematic
    assert len(footprints) == 93 and len(positions) == 79
    for ref, base_fp in base.items():
        assert base_fp.GetPosition() == footprints[ref].GetPosition(), ref
        assert abs((base_fp.GetOrientationDegrees() - footprints[ref].GetOrientationDegrees() + 180) % 360 - 180) < .001, ref
    assert board.GetCopperLayerCount() == 2
    assert pcb.ToMM(board.GetDesignSettings().GetBoardThickness()) == 1.6
    edge = [s for s in board.GetDrawings() if s.GetLayer() == pcb.Edge_Cuts]
    origin = board.GetDesignSettings().GetAuxOrigin()
    corners = {(pcb.ToMM(p.x - origin.x), pcb.ToMM(origin.y - p.y)) for s in edge
               for p in (s.GetStart(), s.GetEnd())}
    assert len(edge) == 4 and corners == {(0, 0), (96, 0), (0, 34), (96, 34)}
    for ref, entry in positions.items():
        fp = footprints[ref]
        assert bool(fp.GetAttributes() & pcb.FP_SMD), ref
        assert not any(p.GetDrillSize().x for p in fp.Pads()), ref
        center = fp.GetPosition()
        assert abs(float(entry['PosX']) - pcb.ToMM(center.x - origin.x)) < .000001, ref
        assert abs(float(entry['PosY']) - pcb.ToMM(origin.y - center.y)) < .000001, ref
        assert entry['Side'] == ('top' if fp.GetLayer() == pcb.F_Cu else 'bottom'), ref
        assert 0 <= float(entry['PosX']) <= 96 and 0 <= float(entry['PosY']) <= 34
    assert {ref for ref, fp in footprints.items() if fp.GetAttributes() & pcb.FP_SMD} == positions.keys()

    pads = [p for fp in footprints.values() for p in fp.Pads()]
    vias = [t for t in board.GetTracks() if isinstance(t, pcb.PCB_VIA)]
    tracks = [t for t in board.GetTracks() if not isinstance(t, pcb.PCB_VIA)]
    zones = list(board.Zones())
    assert len(zones) == 4 and all(z.IsFilled() and z.GetFilledArea() > 0 for z in zones)
    boxes = [(i.GetNetname(), i.GetBoundingBox()) for i in [*pads, *vias, *tracks]]
    boxes += [(z.GetNetname(), z.GetFilledPolysList(z.GetLayer()).BBox()) for z in zones]
    band = pcb.ToMM(min(b.GetLeft() for n, b in boxes if n and not n.startswith(('/P_', 'unconnected-'))) -
                   max(b.GetRight() for n, b in boxes if n.startswith('/P_')))
    assert band >= 8.19
    width = min(pcb.ToMM(t.GetWidth()) for t in tracks)
    via_drill = min(pcb.ToMM(v.GetDrillValue()) for v in vias)
    via_margin = min(pcb.ToMM(v.GetWidth(pcb.F_Cu) - v.GetDrillValue()) for v in vias)
    pth_pads = [p for p in pads if p.GetAttribute() == pcb.PAD_ATTRIB_PTH]
    pth_ring = min(pcb.ToMM(min(p.GetSize().x-p.GetDrillSize().x,
                               p.GetSize().y-p.GetDrillSize().y)) / 2 for p in pth_pads)
    assert width >= .1 and via_drill >= .2 and via_margin >= .15 and pth_ring >= .18
    erc = (DEST / 'ERC.rpt').read_text(encoding='utf-8-sig')
    drc = (DEST / 'DRC.rpt').read_text(encoding='utf-8-sig')
    assert 'Errors 0  Warnings 0' in erc
    assert all('Found 0 ' + n in drc for n in ('DRC violations', 'unconnected pads', 'Footprint errors'))
    return len(intended), band, width, via_drill, via_margin / 2, pth_ring, origin, vias


def make_bom(footprints, positions):
    full = {}
    base_bom = read_csv(OUT / 'BOM_Zasilacz_RevB.csv')
    guard_bom = read_csv(OUT / GUARD / 'BOM_RevB2.csv')
    base_metadata = {item['Oznaczenie']: item for item in base_bom}
    guard_functions = {
        'U101': 'Zasilanie logiki 3,3 V i opóźnienie PG',
        'U102': 'Detekcja nadmiernego spadku na K1/K2',
        'U103': 'Pamięć wyłączenia',
        'U104': 'Bramka Schmitta sterująca PhotoMOS',
        'U105': 'Rozwarcie pętli S1/TH1',
        'D101': 'Kasowanie po zaniku PG',
        'D102': 'Separacja wejścia LDO',
        'D103': 'Ochrona LDO przed napięciem wstecznym',
    }
    for item in base_bom:
        ref = item['Oznaczenie']
        full[ref] = (item['Parametry'], item['MPN'], item['Źródło'], item['Uwagi montażowe'])
    for item in guard_bom:
        if item['Ref'] != 'J1':
            full[ref_name(item['Ref'])] = (item['Wartość'], item['MPN'], '', '')
    assert full.keys() == {ref for ref in footprints if not ref.startswith('TP')}
    assert len(full) == 87
    rows, quote, excluded = [], [], []
    for ref, (value, mpn, original_source, notes) in full.items():
        fp = footprints[ref]
        fp_id = fp.GetFPID()
        footprint = str(fp_id.GetLibNickname()) + ':' + str(fp_id.GetLibItemName())
        selected = SELECTED_PARTS.get(ref, mpn)
        if mpn and selected != mpn:
            notes = (f'Część do wyceny zamiast {mpn}. {notes}').strip()
        mpn = selected
        code_path = CATALOG.get(mpn, '')
        code = code_path.split('/')[-1]
        source = (JLC + code_path if '/' in code_path else LCSC + code + '.html') if code else original_source
        if ref == 'T1':
            plan = 'RFQ transformatora EE16 i montaż THT'
        elif ref in {'J1', 'J2', 'J3'}:
            plan = 'Montaż wiązki po obsadzeniu'
        elif ref not in positions:
            plan = 'Osobne uzgodnienie montażu THT'
        elif ref in HOLD_FROM_CATALOG:
            plan = 'RFQ części / dostawa własna'
            notes = (HOLD_FROM_CATALOG[ref] + ' ' + notes).strip()
        elif code:
            plan = 'Do importu i sprawdzenia w JLCPCB'
            if ref in HV_RESISTORS:
                notes = 'Vishay CRCW2010, 400 V DC/RMS wg karty. Potwierdzić udar i rozkład napięcia. ' + notes
        else:
            plan = 'RFQ / dobrać i zweryfikować dokładny MPN'
        side = 'Top' if fp.GetLayer() == pcb.F_Cu else 'Bottom'
        meta = base_metadata.get(ref, {})
        manufacturer = meta.get('Producent', '')
        if mpn.startswith(('RC0805', 'RT0603', 'RP0603', 'CC0603')):
            manufacturer = 'Yageo'
        elif mpn.startswith(('CGA3', 'C1608', 'C3225')):
            manufacturer = 'TDK'
        elif mpn.startswith(('ERJ-', 'ERA-', 'AQY')):
            manufacturer = 'Panasonic'
        elif mpn.startswith('CRCW'):
            manufacturer = 'Vishay'
        elif not manufacturer:
            manufacturer = {'U101': 'Texas Instruments', 'U102': 'Texas Instruments',
                            'U103': 'Texas Instruments', 'U104': 'Texas Instruments',
                            'D101': 'Diodes Incorporated', 'D102': 'Nexperia',
                            'D103': 'Nexperia', 'C102': 'Murata'}.get(ref, '')
        function = meta.get('Nazwa i funkcja') or guard_functions.get(
            ref, 'Polaryzacja lub nastawa ochrony' if ref.startswith('R') else 'Filtr lub opóźnienie ochrony')
        alternative_source = meta.get('Dystrybutor alternatywny', '')
        if not alternative_source:
            alternative_source = 'LCSC / zakup zewnętrzny' if code else 'Wycena po MPN'
        availability = ('Zapas montażowy JLCPCB do potwierdzenia' if code
                        else 'Brak potwierdzonego kodu w katalogu montażowym')
        if ref in HOLD_FROM_CATALOG:
            availability = HOLD_FROM_CATALOG[ref]
        row = {'Ref': ref, 'Nazwa i funkcja': function, 'Parametry': value, 'Producent': manufacturer,
               'MPN': mpn, 'Footprint': footprint, 'LCSC Part #': code,
               'Ilość na PCB': 1, 'Zakup alternatywny': alternative_source,
               'Cena jednostkowa prototyp / seria': 'Do wyceny',
               'Koszt pozycji prototyp / seria': 'Do wyceny',
               'Dostępność': availability, 'Zamiennik do weryfikacji': meta.get('Zamiennik do weryfikacji', ''),
               'Strona': side, 'Plan montażu': plan, 'Źródło': source, 'Uwagi': notes}
        rows.append(row)
        (quote if plan == 'Do importu i sprawdzenia w JLCPCB' else excluded).append(row)

    path = DEST / 'JLCPCB_PCBA_DO_WYCENY'
    path.mkdir(exist_ok=True)
    fields = list(rows[0])
    write_csv(DEST / 'BOM_pelny_RevD.csv', fields, rows)
    write_csv(path / 'Pozycje_poza_importem.csv', fields, excluded)

    def cpl_rows(references):
        for ref in references:
            p = positions[ref]
            yield {'Designator': ref, 'Mid X': p['PosX'], 'Mid Y': p['PosY'],
                   'Layer': p['Side'].title(), 'Rotation': f"{float(p['Rot']) % 360:.6f}"}

    cpl_fields = ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation']
    quote_refs = {row['Ref'] for row in quote}
    write_csv(path / 'CPL_JLCPCB.csv', cpl_fields, cpl_rows(ref for ref in positions if ref in quote_refs))
    write_csv(DEST / 'CPL_pelny_79_SMD.csv', cpl_fields, cpl_rows(positions))
    grouped = defaultdict(list)
    for row in quote:
        assert re.fullmatch(r'C[0-9]+', row['LCSC Part #'])
        grouped[(row['MPN'], row['Footprint'], row['LCSC Part #'])].append(row['Ref'])
    bom_fields = ['Comment', 'Designator', 'Footprint', 'LCSC Part #']
    write_csv(path / 'BOM_JLCPCB.csv', bom_fields,
              ({'Comment': mpn, 'Designator': ','.join(refs), 'Footprint': footprint.split(':', 1)[1],
                'LCSC Part #': code} for (mpn, footprint, code), refs in grouped.items()))
    bom_refs = [ref for row in read_csv(path / 'BOM_JLCPCB.csv') for ref in row['Designator'].split(',')]
    cpl_refs = [row['Designator'] for row in read_csv(path / 'CPL_JLCPCB.csv')]
    assert Counter(bom_refs) == Counter(cpl_refs) == Counter(quote_refs)
    assert quote_refs | {row['Ref'] for row in excluded} == full.keys()
    assert not quote_refs.intersection(row['Ref'] for row in excluded)
    return len(quote), len(excluded), len(grouped)


def zip_fabrication(origin, vias):
    fab = Path('work/revd_gerber')
    layers = ['gbl', 'gbs', 'gbp', 'gbo', 'gm1', 'gtl', 'gts', 'gtp', 'gto']
    files = [next(fab.glob(f'{NAME}-*.{ext}')) for ext in layers]
    drill = fab / f'{NAME}-PTH.drl'
    outline = files[layers.index('gm1')].read_text()
    edge_points = {(int(x), int(y)) for x, y in re.findall(r'X(\d+)Y(\d+)D0[12]\*', outline)}
    assert edge_points == {(0, 0), (0, 34000000), (96000000, 0), (96000000, 34000000)}
    drilled = {(float(x), float(y)) for x, y in
               re.findall(r'^X([0-9.]+)Y([0-9.]+)', drill.read_text(), re.MULTILINE)}
    for via in vias:
        p = via.GetPosition()
        assert (round(pcb.ToMM(p.x-origin.x), 3), round(pcb.ToMM(origin.y-p.y), 3)) in drilled, p
    assert len(drilled) == len(vias) + 23
    with ZipFile(DEST / 'RevD_Gerber_JLCPCB.zip', 'w', ZIP_DEFLATED) as archive:
        for file in [*files, drill]:
            archive.write(file, file.name)
    with ZipFile(DEST / 'RevD_Gerber_JLCPCB.zip') as archive:
        assert len(archive.namelist()) == 10 and archive.testzip() is None


if __name__ == '__main__':
    board = pcb.LoadBoard(str(DEST / f'{NAME}.kicad_pcb'))
    footprints = by_ref(board)
    positions = {row['Ref']: row for row in read_csv(Path('work/revd_cpl.csv'))}
    pins, band, width, drill, via_ring, pth_ring, origin, vias = verify_design(board, footprints, positions)
    quote, outside, groups = make_bom(footprints, positions)
    zip_fabrication(origin, vias)
    side_counts = Counter(p['Side'] for p in positions.values())
    report = f"""# Weryfikacja projektu i plików Rev D

- ERC i DRC z porównaniem PCB ze schematem przeszły bez naruszeń. Zero niepołączonych padów i rozbieżności. Raporty KiCad zawierają wykaz pominiętych reguł.
- Skrypt porównał {pins} przypisań pin–sieć w źródłach B1/B2, schemacie Rev D i PCB Rev D. Sprawdził też zachowanie położeń i obrotów elementów B1.
- Obrys z Gerbera i PCB ma 96 × 34 mm. Dwie warstwy, laminat 1,6 mm. Najwęższa ścieżka {width:.3f} mm. Najmniejszy otwór przelotki {drill:.3f} mm, najmniejszy pierścień przelotki {via_ring:.3f} mm i padu THT {pth_ring:.3f} mm. Są to wartości nominalne projektu.
- Cztery wypełnienia termiczne. Po uwzględnieniu padów, ścieżek, przelotek i wypełnionej miedzi prosty pas między sieciami pierwotnymi i wtórnymi ma {band:.3f} mm w rzucie na oś X. Izolacja kompletnego zasilacza pozostaje do weryfikacji.
- Wspólny początek Gerbera, wierceń i CPL znajduje się w lewym dolnym rogu płytki. Zweryfikowano współrzędne {len(vias)} przelotek z plikiem wierceń oraz wszystkich 79 pozycji SMD (góra {side_counts['top']}, dół {side_counts['bottom']}) z projektem. Współrzędne strony dolnej mają tę samą orientację X/Y. Obroty części należy zatwierdzić w podglądzie JLCPCB.
- Pełny BOM ma 87 pozycji montażowych. Pakiet do importu ma {quote} pozycji ({groups} grup MPN), z tym samym zestawem oznaczeń w BOM i CPL. Pozostałe {outside} pozycji wykazano oddzielnie. Sześć gołych pól TP101–TP106 służy do prób i nie wchodzi do BOM.
"""
    (DEST / 'Weryfikacja_RevD.md').write_text(report, encoding='utf-8')
    print(f'{pins} pin-net pairs, {band:.3f} mm P/S, {width:.3f} mm tracks, '
          f'{via_ring:.3f} mm via ring, {pth_ring:.3f} mm PTH ring, {quote}/{outside} quote/outside')

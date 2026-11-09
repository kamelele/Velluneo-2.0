import csv
import json
from pathlib import Path

out = Path('outputs')
with (out / 'BOM_E27_RevA.csv').open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    previous = {r['Oznaczenie']: r for r in reader if r['Zespół / wariant'].startswith('Zasilacz')}

names = {
    'F1': ('DigiKey 9094779','3.33','1','1.9518','100','Aktywny w katalogu.','https://www.digikey.com/en/products/detail/schurter-inc/3403-0271-23/9094779'),
    'R1': ('DigiKey 28721869','1.47','1','0.6691','100','Potwierdzona pozycja katalogowa.','https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/AC01000902209JBMCS/28721869'),
    'C2': ('DigiKey 6049847','1.95','1','0.8915','100','Potwierdzona pozycja katalogowa.','https://www.digikey.com/es/products/detail/rubycon/450BXW10MEFR10X16/6049847'),
    'BR1': ('DigiKey MB10SCT-ND','','','','','Potwierdzona pozycja katalogowa.','https://www.onsemi.com/download/data-sheet/pdf/mb10s-d.pdf'),
    'L1': ('DigiKey 2682552','','','','','JLCPCB bez zapasu przy weryfikacji.','https://www.we-online.com/components/products/datasheet/768772102.pdf'),
    'C6': ('DigiKey 10719163','','','','','Potwierdzona pozycja katalogowa.','https://www.digikey.sg/en/products/detail/nichicon/UCM1H471MNJ1MS/10719163'),
}
changed = set(names) | {'J2','J3','R10','R11','R14','R15'}
rows = []
parts = json.loads(Path('work/catalog_b.json').read_text(encoding='utf-8'))
for part in parts:
    ref = part['ref']
    old = previous.get(ref, {})
    row = old.copy() if ref not in changed else dict.fromkeys(fields, '')
    row.update({
        'Zespół / wariant': 'Zasilacz Rev B 66 × 34 mm', 'Oznaczenie': ref,
        'Nazwa i funkcja': part['function'], 'Parametry': part['val'], 'Producent': part['maker'],
        'MPN': part['part'], 'Obudowa / footprint': part['footprint'],
        'Ilość na płytce / zespole': 1,
        'Uwagi montażowe': part['notes'] if ref in changed | {'RV1'} else old.get('Uwagi montażowe', part['notes']),
    })
    if ref in names:
        seller,p1,q1,p2,q2,status,source = names[ref]
        row.update(dict(zip(
            ('Dystrybutor alternatywny','USD/szt. 1 lub MOQ','Próg mały [części]',
             'USD/szt. większy próg','Próg duży [części]','Dostępność i cykl życia','Źródło',
             'Koszt pozycji USD przy progu małym','Koszt pozycji USD przy progu dużym'),
            (seller,p1,q1,p2,q2,status,source,p1,p2))))
    elif ref in {'R10','R11','R14','R15'}:
        row['Dostępność i cykl życia'] = 'Potwierdzić zakup dokładnego MPN i tolerancję przed zamówieniem.'
        row['Dystrybutor alternatywny'] = 'RFQ'
    elif ref in {'J2','J3'}:
        row['Dystrybutor alternatywny'] = 'RFQ wiązki'
        row['Dostępność i cykl życia'] = 'Złącze blokowane poza płytką. Dobór po próbach mechanicznych.'
    if ref == 'L1':
        row['JLCPCB / LCSC'] = 'C7194056'
    rows.append(row)

assert len(rows) == len({r['Oznaczenie'] for r in rows})
with (out / 'BOM_Zasilacz_RevB.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

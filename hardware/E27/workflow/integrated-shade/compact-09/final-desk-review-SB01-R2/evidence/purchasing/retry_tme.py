from pathlib import Path
import runpy,time,json
H=Path(__file__).resolve().parent
# Reuse acquisition parser without executing its final concurrent acquisition.
s=(H/'acquire.py').read_text(encoding='utf-8').split('data=list(concurrent.futures.')[0]
ns={'__file__':str(H/'acquire.py')};exec(compile(s,'acquire-helper','exec'),ns)
items=[('R4','https://www.tme.eu/pl/details/erj6enf1242v/smd-resistors/panasonic/'),('R6','https://www.tme.eu/pl/details/smd1206-3.65r-1%25/rezystory-smd/royalohm/1206s4f365kt5e/'),('D1','https://www.tme.eu/pl/details/us1m-13-f/smd-universal-diodes/diodes-incorporated/'),('TME-SHIPPING','https://www.tme.eu/pl/how-to-buy/7428/Sposob-i-koszty-transportu/')]
data=[]
for item in items:
 d=ns['get'](item);data.append(d);(H/'retry-tme.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8');print(item[0],d.get('http_status'),d.get('error'),flush=True);time.sleep(10)

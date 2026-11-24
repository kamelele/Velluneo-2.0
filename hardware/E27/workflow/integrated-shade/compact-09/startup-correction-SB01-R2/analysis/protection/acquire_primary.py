from pathlib import Path
import urllib.request,json,hashlib,datetime
O=Path(__file__).resolve().parent
urls={'PI-LYT':'https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf','Bourns-FW':'https://www.bourns.com/docs/product-datasheets/fw.pdf','TDK-MOV':'https://www.tdk-electronics.tdk.com/inf/70/db/var/SIOV_Leaded_StandarD.pdf','WE-T1':'https://www.we-online.com/components/products/datasheet/7687709152.pdf','WE-L1':'https://www.we-online.com/components/products/datasheet/768772332.pdf','Diodes-US1M':'https://www.diodes.com/datasheet/download/US1M.pdf','Diodes-MB10S':'https://www.diodes.com/datasheet/download/MB10S.pdf'}
rows=[]
for n,u in urls.items():
 r={'name':n,'url':u,'date_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as h:b=h.read();r['status']=h.status
  assert b.startswith(b'%PDF'),b[:30]
  (O/(n+'.pdf')).write_bytes(b);r['sha256']=hashlib.sha256(b).hexdigest();r['bytes']=len(b)
 except Exception as e:r['error']=str(e)
 rows.append(r)
(O/'primary-acquisition.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))

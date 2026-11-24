from pathlib import Path
import json,urllib.request,hashlib,datetime,re,concurrent.futures
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;P=H.parents[1]/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,t):
  if not self.skip and t.strip():self.out.append(t.strip())
rows=json.loads((P/'procurement.SB01.json').read_text(encoding='utf-8'))['parts'];items=[]
for r in rows:
 ref='-'.join(r['refs']);url=r['url']
 if ref=='L1':url='https://www.digikey.pl/pl/products/detail/vishay-beyschlag-draloric-bc-components/PR02FS0201000KR500/6691142'
 if ref=='RF1':url='https://www.digikey.pl/pl/products/detail/bourns-inc/FW20A47R0JA/4211449'
 if 'tme.eu' in url:url=url.replace('/en/','/pl/')
 items.append((ref,url))
items+=[('U1-DK','https://www.digikey.pl/pl/products/detail/power-integrations/LYT1603D/5801479'),('R6-DK','https://www.digikey.pl/pl/products/result?keywords=1206S4F365KT5E'),('DK-SHIPPING','https://www.digikey.pl/pl/help-support/delivery-information/shipping-rates'),('TME-SHIPPING','https://www.tme.eu/pl/how-to-buy/4752/transport/')]
def get(item):
 ref,url=item;d={'ref':ref,'url':url,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept-Language':'pl-PL,pl;q=0.9,en;q=0.8'})
  with urllib.request.urlopen(req,timeout=25)as r:b=r.read();d.update(http_status=r.status,final_url=r.url,response_date=r.headers.get('Date'),sha256=hashlib.sha256(b).hexdigest())
  (H/(ref+'.html')).write_bytes(b);s=b.decode('utf-8',errors='replace');t=Text();t.feed(s);t='\n'.join(t.out);(H/(ref+'.txt')).write_text(t,encoding='utf-8');d['products']=[]
  for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):
   try:
    o=json.loads(x)
    if isinstance(o,dict)and o.get('@type')=='Product':d['products'].append(o)
   except ValueError:pass
  d['stock_contexts']=re.findall(r'.{0,45}(?:w magazynie|In Stock|in stock|Stock:|dostępn|Available|Minimalna ilość|Minimum order|Cena netto|Net price).{0,100}',t,re.I)[:20]
 except Exception as e:d['error']=str(e)
 return d
data=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,items));(H/'acquisition.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps([{k:r.get(k)for k in ['ref','http_status','error','stock_contexts']}for r in data],ensure_ascii=True))

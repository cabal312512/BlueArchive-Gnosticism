"""Download a bounded primary-text collection and record exact source fingerprints."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / '01_sources' / 'gnostic_readings' / 'downloads'
SOURCES = [
 ('AJ-L', 'Apocryphon of John — long recension', 'https://www.gnosis.org/naghamm/apocjn-long.html'),
 ('AJ-S', 'Apocryphon of John — short recension', 'https://www.gnosis.org/naghamm/apocjn-short.html'),
 ('AJ-M', 'Apocryphon of John — Meyer translation', 'https://www.gnosis.org/naghamm/apocjn-meyer.html'),
 ('AJ-D', 'Apocryphon of John — Davies translation', 'https://www.gnosis.org/naghamm/apocjn-davies.html'),
 ('HA', 'Hypostasis of the Archons', 'https://www.gnosis.org/naghamm/hypostas.html'),
 ('OW', 'On the Origin of the World', 'https://www.gnosis.org/naghamm/origin.html'),
 ('TT', 'Tripartite Tractate', 'https://www.gnosis.org/naghamm/tripart.htm'),
 ('VE', 'A Valentinian Exposition', 'https://www.gnosis.org/naghamm/valex.html'),
 ('GT', 'Gospel of Truth', 'https://www.gnosis.org/naghamm/gostruth.html'),
 ('EUG', 'Eugnostos the Blessed', 'https://www.gnosis.org/naghamm/eugn.html'),
 ('SJC', 'Sophia of Jesus Christ', 'https://www.gnosis.org/naghamm/sjc.html'),
 ('TP', 'Trimorphic Protennoia', 'https://www.gnosis.org/naghamm/trimorph.html'),
 ('EG', 'Holy Book of the Great Invisible Spirit', 'https://www.gnosis.org/naghamm/goseqypt.html'),
 ('ALL', 'Allogenes — Turner annotated translation', 'https://gnosis.org/naghamm/allogenes-jdt-ln.html'),
 ('ZOS', 'Zostrianos — Turner indexed translation', 'https://www.gnosis.org/naghamm/zostr-jdt-indexed.html'),
 ('FLORA', 'Ptolemy: Letter to Flora', 'https://www.gnosis.org/library/flora.htm'),
 ('PS-30', 'Pistis Sophia, chapter 30', 'https://www.gnosis.org/library/pistis-sophia/ps034.htm'),
 ('PS-INTRO', 'Pistis Sophia, Mead introduction', 'https://gnosis.org/library/pistis-sophia/ps003.htm'),
] + [(f'IR-{n}', f'Irenaeus: Against Heresies I.{n}', f'https://www.newadvent.org/fathers/01031{n:02}.htm') for n in [1,2,3,4,5,6,7,11,12,24,29,30]] + [
 ('HIPP-VI', 'Hippolytus: Refutation, book VI', 'https://www.newadvent.org/fathers/050106.htm'),
 ('HIPP-VII', 'Hippolytus: Refutation, book VII', 'https://www.newadvent.org/fathers/050107.htm'),
 ('NARBONNE-STUDIES', 'Salut gnostique et metaphysique plotinienne: Cinq etudes', 'https://www.pulaval.com/libreacces/9782763759319.pdf'),
 ('TURNER-2001-VERIFIED', 'Turner: Sethian Gnosticism and the Platonic Tradition', 'https://christgnostic.com/wp-content/uploads/2023/02/Turner-J.D.-Sethian-Gnosticism-and-the-Platonic-Tradition.pdf'),
 ('PS-MEAD', 'Pistis Sophia — Mead 1921', 'https://iapsop.com/ssoc/1921__mead___pistis_sophia.pdf'),
 ('THOMASSEN-CH', 'The Valentinian reception of Gnostic protology — open-access chapter', 'https://www.degruyterbrill.com/document/doi/10.1515/9783110705829-009/pdf?licenseType=free'),
]

class Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
        if tag in ('p','br','div','h1','h2','h3','h4','li','tr'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
        if tag in ('p','div','li'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def fetch(item):
    sid,title,url=item
    base={'id':sid,'title':title,'url':url}
    try:
        request=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; local research archive)'})
        with urlopen(request,timeout=22) as response:
            data=response.read(); final=response.url
        if not data: raise ValueError('Empty response; not verified content')
        is_pdf=data.startswith(b'%PDF')
        ext='.pdf' if is_pdf else '.html'
        (DEST/(sid+ext)).write_bytes(data)
        if not is_pdf:
            parser=Plain(); parser.feed(data.decode('utf-8',errors='replace'))
            plain=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',''.join(parser.parts))
            (DEST/(sid+'.txt')).write_text(plain,encoding='utf-8')
        return {**base,'status':'downloaded','final_url':final,'bytes':len(data),'sha256':sha256(data).hexdigest(),'file':str((DEST/(sid+ext)).relative_to(ROOT)),'downloaded_utc':datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        return {**base,'status':'failed','error':str(exc)}

if __name__=='__main__':
    DEST.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        records=list(pool.map(fetch,SOURCES))
    path=DEST.parent/'download_manifest.json'
    previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    merged={r['id']:r for r in previous}
    merged.update({r['id']:r for r in records})
    path.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for record in records: print(record['id'],record['status'],record.get('bytes',record.get('error')))

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Check(HTMLParser):
 def __init__(self,path):super().__init__();self.path=path;self.ids=set();self.links=[];self.quizzes=0;self.chapters=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:
   if d['id'] in self.ids:errors.append((str(self.path),'duplicate id',d['id']))
   self.ids.add(d['id'])
  if d.get('class')=='quiz':self.quizzes+=1
  if d.get('class')=='chapter':self.chapters+=1
  for attr in ('href','src'):
   if attr in d:self.links.append(d[attr])
parsed={}
for p in ROOT.glob('*.html'):
 c=Check(p);c.feed(p.read_text());parsed[p.resolve()]=c
for p,c in parsed.items():
 for link in c.links:
  if link.startswith(('http:','https:','data:')):continue
  u=urlsplit(link);dest=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not dest.exists():errors.append((str(p),'missing path',link))
  elif u.fragment and dest in parsed and unquote(u.fragment) not in parsed[dest].ids:errors.append((str(p),'missing anchor',link))
coverage=json.loads((ROOT/'coverage.json').read_text()); main=parsed[(ROOT/'index.html').resolve()]
assert main.chapters==coverage['chapters']==50
assert main.quizzes==coverage['quiz_questions']==99
assert len(list((ROOT/'assets').rglob('*.jpg')))==coverage['pdf_pages']==956
sources=coverage['sources'];files={s['file'] for s in sources}
originals=set()
for folder,ext in [('351 Slide TH','*.pdf'),('Network','*.pdf'),('DataCommunication_and_Networking','ch*.ppt'),('PKA','*.pka')]:
 originals.update(str(p.relative_to(ROOT.parent)) for p in (ROOT.parent/folder).glob(ext))
assert files==originals,(files^originals)
assert not errors,errors[:20]
report={'result':'PASS','html_files':len(parsed),'links_and_image_paths_checked':sum(len(c.links) for c in parsed.values()),'broken_links':0,'duplicate_ids':0,'study_chapters':main.chapters,'quiz_questions':main.quizzes,'pdf_images':956,'source_files_catalogued':len(files),'note':'Static structure and local links checked. Browser visual/interactive preview could not run because the environment denies required Chrome socket operations. Calculator logic separately checked with known subnet examples and invalid inputs.'}
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))

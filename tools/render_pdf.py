from pathlib import Path
import concurrent.futures,subprocess,json,re
root=Path('/home/krittanon/Downloads/351')
def render(p):
 rel=p.relative_to(root); slug=re.sub(r'[^a-zA-Z0-9_-]','_',p.stem)
 if not slug.strip('_'):slug='subnet-examples'
 folder=root/'translations/assets'/slug;folder.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['pdftoppm','-jpeg','-jpegopt','quality=76','-scale-to','1250',str(p),str(folder/'page')],capture_output=True)
 return {'file':str(rel),'asset':slug,'images':len(list(folder.glob('page-*.jpg'))),'error':r.stderr.decode() if r.returncode else ''}
paths=list((root/'351 Slide TH').glob('*.pdf'))+list((root/'Network').glob('*.pdf'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(render,paths))
(root/'translations/_sources/pdf_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False))

from pathlib import Path
import re,json,html,urllib.parse,ipaddress
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'translations'
e=lambda s:html.escape(str(s),quote=True)
url=lambda s:urllib.parse.quote(str(s),safe='/#?=')
CSS=(OUT/'style.css').read_text(); JS=(OUT/'app.js').read_text()
text=(OUT/'เนื้อหาติว.md').read_text()
heading_map=json.loads((OUT/'tools/หัวข้อย่อย.json').read_text())
chapters={}
for match in re.finditer(r'^# \[([^]]+)\] ([^\n]+)\n(.*?)(?=^# \[|\Z)',text,re.M|re.S):
 ident,title,body=match.groups();chapters[ident]={'id':ident,'title':title,'body':body}

def inline(t):return re.sub(r'`([^`]+)`',r'<code>\1</code>',e(t))
def md(t):
 lines=t.strip().splitlines();out=[];i=0
 while i<len(lines):
  l=lines[i].strip()
  if not l:i+=1;continue
  if l.startswith('```'):
   i+=1;code=[]
   while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
   out.append('<pre><code>'+e('\n'.join(code))+'</code></pre>');i+=1;continue
  if l.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=lines[i].strip().strip('|').split('|')
    if not all(re.match(r'^\s*:?-+:?\s*$',c) for c in cells):rows.append(cells)
    i+=1
   out.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+inline(c.strip())+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
  if l.startswith('? '):
   q,a=l[2:].split(' || ',1);out.append('<details class="quiz"><summary>ลองตอบ: '+inline(q)+'</summary><p><strong>เฉลยและเหตุผล:</strong> '+inline(a)+'</p></details>');i+=1;continue
  if l.startswith('! '):out.append('<p class="key"><strong>จำให้ได้:</strong> '+inline(l[2:])+'</p>');i+=1;continue
  if re.match(r'^\d+\. ',l):
   lis=[]
   while i<len(lines) and re.match(r'^\d+\. ',lines[i].strip()):lis.append(re.sub(r'^\d+\. ','',lines[i].strip()));i+=1
   out.append('<ol>'+''.join('<li>'+inline(x)+'</li>' for x in lis)+'</ol>');continue
  out.append('<p>'+inline(l)+'</p>');i+=1
 return '\n'.join(out)

def cards(ch,local=False):
 out=[]
 for n,m in enumerate(re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',ch['body'],re.M|re.S),1):
  title,body=m.groups();out.append(f'<article class="card" data-search id="c-{ch["id"]}-{n}"><h3>{e(title)}</h3>{md(body)}<a class="back" href="#top">กลับสารบัญ ↑</a></article>')
 return ''.join(out)

network_map={1:['01'],2:['02'],3:['01','08','15'],4:['03','04','05'],5:['04','N5'],6:['07'],7:['10','11'],8:['14'],9:['19','20','21','SUB'],10:['23','25','26','27'],11:['31','32']}
map351={1:['K1','01','02','03','07','08','31'],2:['K2','25','26','27','23'],3:['K3','11','23','24'],4:['K4','19','20','21','22','SUB'],5:['K5','10','12','13','14','15']}
net_titles={1:'พื้นฐานการสื่อสารข้อมูล',2:'แบบจำลองเครือข่าย',3:'องค์ประกอบและโครงสร้างเครือข่าย',4:'ข้อมูลและสัญญาณ',5:'การส่งผ่านข้อมูลดิจิทัลและ Interface',6:'สื่อกลางส่งข้อมูล',7:'การตรวจจับข้อผิดพลาดและ Flow/Error Control',8:'เครือข่าย LAN ไร้สาย',9:'TCP/IP และ Subnet',10:'โปรโตคอล Transport และ Application',11:'ความปลอดภัยบนเครือข่าย'}
source_records=[]
manifest=json.loads((OUT/'_sources/pdf_manifest.json').read_text())
for item in manifest:
 p=Path(item['file']);stem=p.stem
 if p.parent.name=='Network':
  n=int(re.search(r'chapter(\d+)',stem,re.I)[1]);sid=f'network-{n:02}';group='network';related=network_map[n];title=f'Network บท {n} — {net_titles[n]}'
 elif stem.startswith('Chapter_'):
  n=int(stem.split('_')[1]);sid=f'351-{n:02}';group='351';related=map351[n];title=chapters[f'K{n}']['title']
 else:
  sid='subnet-examples' if 'Subnet' in stem else 'subnet-scans';group='subnet';related=['SUB','19'];title='ตัวอย่างหา Subnet — เฉลยพร้อมตรวจค่าคลาดเคลื่อน' if 'Subnet' in stem else 'Subnetting — เอกสารภาพ 4 สไลด์ต่อหน้า'
 pages=(OUT/'_sources'/f'{stem}.txt').read_text().split('\f')
 if pages and not pages[-1].strip():pages.pop()
 assert len(pages)==item['images'],(stem,len(pages),item['images'])
 imgs=sorted((OUT/'assets'/item['asset']).glob('*.jpg'),key=lambda p:int(re.search(r'-(\d+)\.jpg$',p.name)[1]))
 source_records.append({'id':sid,'group':group,'file':str(p),'title':title,'related':related,'pages':pages,'images':[str(p.relative_to(OUT)) for p in imgs],'kind':'pdf'})
for p in sorted((OUT/'_sources').glob('ch*.json')):
 n=int(p.stem[2:]);source_records.append({'id':f'dcn-{n:02}','group':'dcn','file':f'DataCommunication_and_Networking/ch{n:02}.ppt','title':f'Data Communication {n} — '+chapters[f'{n:02}']['title'],'related':[f'{n:02}'],'pages':json.loads(p.read_text())['slides'],'images':[],'kind':'ppt'})
for i,p in enumerate(sorted((ROOT/'PKA').glob('*.pka')),1):
 name=p.name
 if name.startswith('5.2'):lab='LAB1'
 elif name.startswith('5.3'):lab='LAB2'
 elif name.startswith('5.4'):lab='LAB3'
 elif name.startswith('5.5'):lab='LAB4'
 elif name.startswith('8.1.2.11'):lab='LAB5'
 elif name.startswith('8.1.2.13'):lab='LAB6'
 elif name.startswith('8.1.2.15'):lab='LAB7'
 elif name.startswith('11_'):lab='LAB8'
 else:lab='LAB9'
 source_records.append({'id':'pka-'+lab.lower(),'group':'lab','file':str(p.relative_to(ROOT)),'title':chapters[lab]['title'],'related':['LAB0',lab],'pages':[],'images':[],'kind':'pka'})
source_records.sort(key=lambda x:({'351':0,'subnet':1,'network':2,'dcn':3,'lab':4}[x['group']],x['id']))
for ch in chapters.values():
 cid=ch['id'];groups=set()
 if cid.isdigit():groups.add('dcn')
 if cid.startswith('K'):groups.add('351')
 if cid.startswith('LAB'):groups.add('lab')
 if cid=='SUB':groups.add('subnet')
 for s in source_records:
  if cid in s['related']:groups.add(s['group'])
 ch['groups']=' '.join(sorted(groups))

def page(title,header,body,options='',is_source=False):
 return '<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="เอกสารอ่าน 351 ภาษาไทย แปลเรียบเรียง ติว สรุป สูตร แบบฝึก พร้อมต้นฉบับออฟไลน์"><title>'+e(title)+'</title><style>'+CSS+'</style></head><body id="top"><a class="skip" href="#main">ข้ามไปเนื้อหา</a><header>'+header+'</header><div class="toolbar"><div class="tools">'+options+'<label for="search">ค้นหา</label><input id="search" type="search" placeholder="คำไทย / English / สูตร" autocomplete="off"><button id="reset">ล้างตัวกรอง</button><button id="theme" aria-label="สลับพื้นหลังสว่างหรือมืด">สว่าง/มืด</button><button id="fontDown" aria-label="ลดขนาดตัวอักษร">ก−</button><button id="fontUp" aria-label="เพิ่มขนาดตัวอักษร">ก+</button><button id="print">พิมพ์ / PDF ที่แสดง</button><small id="count" aria-live="polite"></small></div></div><main id="main">'+body+'<p id="empty" hidden>ไม่พบหัวข้อที่ตรงกับคำค้น ลองล้างตัวกรองหรือใช้คำสั้นลง</p></main><a class="float-top" href="#top" aria-label="กลับด้านบน">สารบัญ ↑</a><footer>351 · เอกสารภาษาไทยสำหรับอ่านทบทวน · แยกต้นฉบับและคำอธิบายเสริม · เปิดไฟล์นี้อ่านได้แบบออฟไลน์</footer><script>'+JS+'</script></body></html>'

def original_link(s):return '<a href="'+url('../'+s['file'])+'">เปิดไฟล์ต้นฉบับ '+e(Path(s['file']).name)+'</a>'
def tile(s):
 count=(str(len(s['pages']))+' หน้า PDF' if s['kind']=='pdf' else str(len(s['pages']))+' บล็อกข้อความที่สกัด' if s['kind']=='ppt' else 'คู่มือแนวทำและตรวจผล · ยังไม่ยืนยัน config ภายใน')
 return f'<a class="tile" href="source-{s["id"]}.html">{e(s["title"])}<small>{e(count)}</small></a>'

def calculator():return '''<section class="catalog calculator" id="calculator"><h2>เครื่องคำนวณ IPv4 Subnet</h2><p>ลองทำมือจากบท SUB ก่อน แล้วใช้ตรวจ Network, Broadcast, Mask, จำนวน Address และช่วง Host หากต้องการจำนวน Subnet ให้ใส่ Parent prefix ด้วย</p><form id="subnetForm"><label>IPv4 address<input id="ipInput" value="192.168.10.77" inputmode="decimal" required aria-label="IPv4 address"></label><label>Prefix /p<input id="prefixInput" type="number" min="0" max="32" value="27" required></label><label>Parent /q (เว้นว่างได้)<input id="parentInput" type="number" min="0" max="32" placeholder="เช่น 24"></label><button type="submit">คำนวณและอธิบายผล</button></form><div id="calcResult" class="table-scroll" aria-live="polite"></div><p class="note">/31 แสดงบริบท point-to-point และ /32 แสดง address เดียว โดยไม่ใช้สูตร −2 แบบเหมารวม</p></section>'''

pdfcount=sum(len(s['pages']) for s in source_records if s['kind']=='pdf');pptcount=sum(len(s['pages']) for s in source_records if s['kind']=='ppt');quizcount=text.count('\n? ')
header=f'''<p class="eyebrow">351 · DATA COMMUNICATION & COMPUTER NETWORKS</p><h1>แปลไทย · เสริมติว · สรุปเครือข่าย</h1><p>ชุดอ่านครอบคลุมไฟล์ในโฟลเดอร์ 351: สไลด์ 351 บท 1–5, Subnetting, Network บท 1–11, Data Communication บท 1–32 และคู่มือประกอบ Packet Tracer 9 กิจกรรม</p><div class="stats"><span>{len(chapters)} บทอ่าน/ติว</span><span>{quizcount} คำถามพร้อมเหตุผล</span><span>{pdfcount} หน้า PDF เปิดเทียบได้</span><span>32 ไฟล์ PPT · 9 กิจกรรม</span></div><div class="banner"><strong>วิธีอ่าน:</strong> เนื้อหาภาษาไทยเป็นการแปลเรียบเรียงและอธิบายตามหัวข้อร่วมกับตัวอย่างเสริม ไม่ใช่คำแปลเทียบทุกบรรทัดหรือทุกภาพของทุกสไลด์ เปิดหน้า “เอกสารตามไฟล์” เพื่อดูต้นฉบับครบตามที่สกัดได้ โดยข้อความอังกฤษในส่วนต้นฉบับยังคงไว้สำหรับตรวจเทียบ ส่วน PKA เป็นคู่มือแนวทำ ยังไม่ได้ตรวจคำตอบภายในกิจกรรม</div><p class="note">คงบริบทเทคโนโลยีของเอกสารเดิม แยกตัวอย่างสมมติและจุดแก้ค่าคลาดเคลื่อนชัดเจน ไม่อ้างว่าตัวเลขที่เขียน “ปัจจุบัน” ในสไลด์เก่าเป็นข้อมูลล่าสุด · เก็บทั้งโฟลเดอร์ translations ไว้ด้วยกันสำหรับภาพ และเก็บไว้ข้างโฟลเดอร์ต้นฉบับหากต้องการลิงก์เปิดไฟล์เดิม</p>'''
body='<section class="catalog"><h2>เริ่มอ่านตรงไหนดี</h2><div class="grid"><a class="tile" href="#chapter-K1">เริ่มจากสไลด์ 351 บท 1–5<small>ภาพรวม Internet → Application → Transport → Network → Link</small></a><a class="tile" href="#chapter-SUB">ติว Subnet และแก้ตัวอย่างต้นฉบับ<small>8 ตัวอย่าง, VLSM, /31 และ /32</small></a><a class="tile" href="#chapter-REV">สรุปสูตรและทบทวนก่อนสอบ<small>คู่คำที่สับสน พร้อมโจทย์เชื่อมหลายบท</small></a><a class="tile" href="#chapter-LAB0">เริ่มฝึก Packet Tracer<small>แนวทำและตรวจผลครบ 9 หัวข้อ</small></a><a class="tile" href="#calculator">เครื่องคำนวณ Subnet<small>ตรวจผลพร้อม Parent prefix</small></a><a class="tile" href="#source-catalog">เอกสารตามไฟล์ต้นฉบับ<small>ครบ 59 ไฟล์เนื้อหา ไม่รวมไฟล์ล็อก ~$ch06.ppt</small></a></div><p><span id="readCount"></span> <span class="note">บันทึกการอ่านในเบราว์เซอร์นี้เมื่อระบบอนุญาต</span></p><div class="progress"><div id="readBar"></div></div></section>'
body+='<nav class="catalog" aria-label="สารบัญบทอ่าน"><h2>สารบัญบทอ่านและติว</h2><div class="grid">'+''.join(f'<a class="tile" href="#chapter-{ch["id"]}">{e(ch["title"])}</a>' for ch in chapters.values())+'</div></nav>'
body+='<section class="catalog" id="source-catalog"><h2>เอกสารตามไฟล์ต้นฉบับ</h2><p>หน้าแต่ละไฟล์มีบทภาษาไทยที่เกี่ยวข้องและต้นฉบับให้ตรวจเทียบ ส่วน PDF มีภาพทุกหน้า; PPT เป็นข้อความจากระเบียนภายใน ลำดับอาจไม่ตรงสไลด์ในโปรแกรมและยังไม่รวมตัวอักษรในรูป; PKA มีลิงก์ไฟล์และคู่มือแนวทำ</p>'
for group,label in [('351','351 Slide TH'),('subnet','Subnetting'),('network','Network 11 บท'),('dcn','Data Communication 32 บท'),('lab','Packet Tracer 9 กิจกรรม')]:body+='<h3>'+label+'</h3><div class="grid">'+''.join(tile(s) for s in source_records if s['group']==group)+'</div>'
body+='</section>'+calculator()
for ch in chapters.values():
 if ch['id'].isdigit():
  source=json.loads((OUT/'_sources'/f'ch{ch["id"]}.json').read_text())['slides']; headings=[]
  for raw in source:
   for line in re.split(r'[\r\n\v]',raw):
    m=re.match(r'^(\d{1,2}-\d{1,2})\s+(.+)',line.strip())
    if m:
     num,eng=m.groups();eng=eng.strip();assert eng in heading_map,(ch['id'],eng);headings.append('<tr><td>'+e(num)+'</td><td>'+e(heading_map[eng])+'</td><td lang="en">'+e(eng)+'</td></tr>')
  if headings:
   source_sections='<article class="card" data-search id="c-'+ch['id']+'-source-topics"><h3>แปลหัวข้อย่อยตามต้นฉบับ</h3><p class="note">ลำดับและหมายเลขตามข้อความในไฟล์ แม้ต้นฉบับใช้เลขหัวข้อซ้ำก็เก็บไว้เพื่อเทียบได้</p><div class="table-scroll"><table><thead><tr><th>หัวข้อ</th><th>ภาษาไทย</th><th>ต้นฉบับ</th></tr></thead><tbody>'+''.join(headings)+'</tbody></table></div></article>'
   ch['source_sections']=source_sections
 refs=[s for s in source_records if ch['id'] in s['related']]
 links=' · '.join(f'<a href="source-{s["id"]}.html">{e(Path(s["file"]).name)}</a>' for s in refs)
 body+=f'<section class="chapter" id="chapter-{ch["id"]}" data-groups="{ch["groups"]}"><div class="chapter-title"><button class="read" data-id="{ch["id"]}" aria-pressed="false">ทำเครื่องหมายว่าอ่านแล้ว</button><h2>{e(ch["title"])}</h2><p>คำแปลเรียบเรียง · อธิบายเสริม · สรุป · คำถามพร้อมเฉลย</p>'+(('<p>อ่านเทียบไฟล์: '+links+'</p>') if links else '')+'</div>'+ch.get('source_sections','')+cards(ch)+'</section>'
options='<label for="group">ชุด</label><select id="group"><option value="">ทุกชุด</option><option value="351">351 Slide TH</option><option value="dcn">Data Communication</option><option value="network">Network</option><option value="subnet">Subnetting</option><option value="lab">Packet Tracer</option></select><label for="chapterSelect">บท</label><select id="chapterSelect"><option value="">ทุกบท</option>'+''.join(f'<option value="chapter-{ch["id"]}">{e(ch["title"])}</option>' for ch in chapters.values())+'</select><button id="answers">เปิดเฉลยทั้งหมด</button><button id="printAll">พิมพ์ทุกบท</button>'
main=page('351 — แปลไทย เสริมติว สรุป',header,body,options)
(OUT/'index.html').write_text(main)
(OUT/'351-แปลไทย-เสริมติว-สรุป.html').write_text(main)
for s in source_records:
 primary=chapters[s['related'][0]]
 header='<p class="eyebrow"><a href="index.html">← หน้ารวม 351</a></p><h1>'+e(s['title'])+'</h1><p>'+original_link(s)+'</p><p class="note">เส้นทางต้นฉบับ: '+e(s['file'])+'</p>'
 if s['kind']=='ppt':header+='<div class="banner">คำแปลเรียบเรียงและคำอธิบายอยู่ในบทอ่านด้านล่าง ส่วนข้อความต้นฉบับเก็บไว้ตรวจเทียบ ยังไม่ใช่คำแปลภาษาไทยทุกบรรทัดของสไลด์ บล็อกข้อความสกัดจากไฟล์ PPT รุ่นเก่าอาจมี master/ข้อความที่ไม่แสดงและไม่รับรองลำดับสไลด์จริง; ภาพและสูตรที่เป็นภาพให้เปิดไฟล์ต้นฉบับ</div>'
 elif s['kind']=='pdf':header+='<div class="banner">บทภาษาไทยที่เกี่ยวข้องอยู่ก่อนภาคต้นฉบับ แต่ละหน้า PDF มีภาพครบสำหรับอ่านแผนภาพและตรวจข้อความที่สกัดผิดหรือแตกบรรทัด เนื้อหาไทยเดิมในสไลด์คงไว้ในส่วนต้นฉบับ ส่วนอธิบายเสริมแยกออกมาให้อ่านง่าย</div>'
 else:header+='<div class="banner">คู่มือนี้อ้างอิงหัวข้อกิจกรรมจากชื่อไฟล์ ยังไม่ได้อ่าน topology, Addressing Table หรือ answer network ภายใน PKA จึงต้องใช้ค่าจริงจาก instructions เมื่อเปิดใน Packet Tracer และยังไม่ได้ตรวจคะแนนกิจกรรม</div>'
 b='<nav class="catalog"><h2>ทางลัด</h2><div class="grid">'+''.join(f'<a class="tile" href="#chapter-{cid}">{e(chapters[cid]["title"])}</a>' for cid in s['related'])
 if s['pages']:b+='<a class="tile" href="#source-section">ต้นฉบับตามหน้า / บล็อกข้อความ</a>'
 b+='</div></nav>'
 for cid in s['related']:
  ch=chapters[cid];b+=f'<section class="chapter" id="chapter-{cid}"><div class="chapter-title"><h2>{e(ch["title"])}</h2><p><a href="index.html#chapter-{cid}">เปิดบทนี้ในเล่มรวม</a></p></div>'+ch.get('source_sections','')+cards(ch)+'</section>'
 if s['pages']:
  b+='<section class="source-chapter" id="source-section"><div class="chapter-title"><h2>ต้นฉบับสำหรับตรวจเทียบ</h2><p>'+('เรียงตามหน้า PDF' if s['kind']=='pdf' else 'เรียงตามระเบียนข้อความที่สกัดจาก PPT ไม่รับรองลำดับหน้าที่แสดงในโปรแกรม')+'</p></div><nav class="source-nav" aria-label="ข้ามไปต้นฉบับ">'+''.join(f'<a href="#page-{i}">{i}</a>' for i in range(1,len(s['pages'])+1))+'</nav>'
  for i,raw in enumerate(s['pages'],1):
   clean=raw.replace('\r','\n').replace('\v','\n').strip();first=next((x.strip() for x in clean.splitlines() if x.strip()),'ต้นฉบับเป็นภาพ/ไม่มีข้อความที่สกัดได้');label='หน้า' if s['kind']=='pdf' else 'บล็อกข้อความ'
   b+=f'<article class="slide" data-search id="page-{i}"><h2>{label} {i} — {e(first[:120])}</h2>'
   if s['kind']=='pdf':
    img=s['images'][i-1];b+='<details><summary>ดูภาพต้นฉบับหน้า '+str(i)+'</summary><a href="'+url(img)+'" target="_blank" rel="noopener"><img class="source-image" loading="lazy" decoding="async" src="'+url(img)+'" alt="'+e(s['title'])+' หน้า '+str(i)+'"></a><p class="note">คลิกภาพเพื่อเปิดขยาย</p></details>'
   b+='<details><summary>อ่านข้อความต้นฉบับที่สกัดได้ '+(' (ไทย/อังกฤษตามไฟล์)' if s['kind']=='pdf' else '(อังกฤษตามไฟล์)')+'</summary><pre class="source-text">'+e(clean if clean else 'หน้านี้ไม่มีข้อความที่สกัดได้ กรุณาดูภาพต้นฉบับ')+'</pre></details><p class="note">ทบทวนภาษาไทย: '+''.join(f'<a class="pill" href="#chapter-{cid}">{e(chapters[cid]["title"])}</a>' for cid in s['related'])+'</p><a class="back" href="#top">กลับสารบัญ ↑</a></article>'
  b+='</section>'
 (OUT/f'source-{s["id"]}.html').write_text(page(s['title'],header,b,'<button id="answers">เปิดเฉลยทั้งหมด</button>',True))
report={'chapters':len(chapters),'quiz_questions':quizcount,'pdf_files':sum(s['kind']=='pdf' for s in source_records),'pdf_pages':pdfcount,'ppt_files':32,'ppt_text_blocks':pptcount,'pka_files':9,'source_files_total':len(source_records),'scope':'Thai topic-based translated explanations and tutoring; not a line-by-line translation of every slide. PDF page images preserved. PPT text only; PKA internal content not verified.','sources':[{k:v for k,v in s.items() if k not in ['pages','images']}|{'extracted_blocks':len(s['pages'])} for s in source_records]}
(OUT/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(OUT/'อ่านก่อน.txt').write_text('เปิด index.html หรือ 351-แปลไทย-เสริมติว-สรุป.html ด้วยเบราว์เซอร์\n\nชุดนี้มี '+str(len(chapters))+' บทอ่านภาษาไทยและ '+str(quizcount)+' คำถามทบทวน พร้อมตัวอย่างคำนวณ สรุปและเครื่องคำนวณ subnet\nเป็นคำแปลเรียบเรียงตามหัวข้อและเสริมติว ไม่ใช่คำแปลเทียบทุกบรรทัดของทุกสไลด์\nต้นฉบับ PDF มีภาพครบ '+str(pdfcount)+' หน้า ส่วนข้อความอังกฤษในภาคต้นฉบับยังคงภาษาเดิม\nPPT เก็บข้อความจากระเบียนในไฟล์ ไม่รับรองลำดับสไลด์/ข้อความในภาพ\nPKA ทั้ง 9 มีคู่มือแนวทำตามหัวข้อชื่อไฟล์ ยังไม่ได้ตรวจ topology หรือเฉลยภายในไฟล์\n\nทุกอย่างอ่านออฟไลน์ได้ ไม่ต้องติดตั้งหรือรัน server เก็บโฟลเดอร์ assets ไว้กับ HTML\nลิงก์ไฟล์ต้นฉบับชี้ไปโฟลเดอร์ข้าง translations จึงควรเก็บโครงสร้างเดิมไว้\nพิมพ์/PDF ที่แสดงจะพิมพ์เนื้อหาตามตัวกรอง เปิดเฉลยก่อนพิมพ์หากต้องการเฉลย\nปุ่มอ่านแล้ว/ขนาดตัวอักษร/พื้นหลังบันทึกใน localStorage เมื่อเบราว์เซอร์อนุญาต\nไฟล์ ~$ch06.ppt เป็นไฟล์ล็อกของ Office ไม่ใช่บทเนื้อหา จึงไม่นับเป็นเอกสารเรียน\n\nเนื้อหาที่แก้ไขได้: เนื้อหาติว.md\nสร้าง HTML ซ้ำ: python3 translations/tools/build.py (รันจากโฟลเดอร์ 351)\nรายละเอียดขอบเขต: coverage.json\n')
print(json.dumps({k:v for k,v in report.items() if k!='sources'},ensure_ascii=False,indent=2))

from pathlib import Path
import re, html
import markdown
ROOT=Path(__file__).parent
E=html.escape
CSS='''
.reading{font-size:18px;line-height:1.95}.reading h2{font-size:29px;line-height:1.55;border-bottom:2px solid #d8e6f2;padding-bottom:15px;margin:0 0 26px}.reading h3{font-size:22px;color:#164a83;line-height:1.6;margin:32px 0 12px}.reading p{max-width:84ch;margin:16px 0}.reading strong{color:#163f6b}.reading article{background:white;border:1px solid #d5dfeb;border-radius:14px;padding:clamp(20px,4vw,46px);margin:24px 0;scroll-margin-top:100px}.reading pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#10213f;color:#e7f2ff;padding:20px;border-radius:10px;font-size:15px;line-height:1.75}.reading code{font-family:Consolas,monospace;overflow-wrap:anywhere}.reading :not(pre)>code{background:#edf2f8;padding:2px 5px;border-radius:4px}.reading table{font-size:16px;line-height:1.8;min-width:550px}.reading .table-scroll{overflow-x:auto;margin:20px 0}.reading th{background:#eaf1fa}.reading td{vertical-align:top}.reading li{margin:10px 0}.reading blockquote{border-left:4px solid #188674;margin-left:0;padding-left:20px}.reading-toc{columns:2;column-gap:30px;padding-left:24px}.reading-toc li{break-inside:avoid;margin:9px 0}.reading article[hidden]{display:none}.reading-tools{background:#edf3fa;border:1px solid #cbd9ec;padding:15px;border-radius:12px}.reading-empty{padding:20px;background:#fff6e6}.reading a{overflow-wrap:anywhere}.reader-toplink{font-size:14px}.reading[style]{--reader-font:18px}.reading{font-size:var(--reader-font,18px)}
@media(max-width:650px){.reading{font-size:17px}.reading h2{font-size:24px}.reading h3{font-size:20px}.reading-toc{columns:1}.reading pre{font-size:13px}.reading article{padding:20px 16px}.reading p{line-height:1.95}}
@media print{.reading-tools,.reading-toc-box,.reader-toplink{display:none!important}.reading{font-size:12pt;line-height:1.8}.reading h2{font-size:20pt;break-after:avoid}.reading h3{font-size:15pt;break-after:avoid}.reading article{break-before:page;break-inside:auto;border:0;padding:0;margin:0}.reading article[hidden]{display:none!important}.reading pre{color:black;background:#f3f3f3;border:1px solid #bbb;font-size:10pt;break-inside:avoid}.reading table{font-size:10pt;min-width:0}.reading tr{break-inside:avoid}.reading .table-scroll{overflow:visible}.reading p,.reading li{orphans:3;widows:3}}
'''
JS='''
(()=>{const root=document.getElementById('reading');if(!root)return;
const query=root.querySelector('[data-read-search]'),select=root.querySelector('[data-read-select]'),articles=[...root.querySelectorAll('article[data-read-index]')],status=root.querySelector('[data-read-status]');
function filter(){let n=0,term=query.value.trim().toLocaleLowerCase();articles.forEach(a=>{a.hidden=(select.value!=='all'&&a.dataset.readIndex!==select.value)||(term&&!a.textContent.toLocaleLowerCase().includes(term));if(!a.hidden)n++});status.textContent=`แสดง ${n} / ${articles.length} บท`;root.querySelector('[data-read-empty]').hidden=n>0}
query.addEventListener('input',filter);select.addEventListener('change',filter);
root.querySelector('[data-read-reset]').onclick=()=>{query.value='';select.value='all';filter()};
root.querySelector('[data-read-print]').onclick=()=>window.print();let font=18;
root.querySelector('[data-read-larger]').onclick=()=>{font=Math.min(26,font+1);root.style.setProperty('--reader-font',font+'px')};root.querySelector('[data-read-smaller]').onclick=()=>{font=Math.max(15,font-1);root.style.setProperty('--reader-font',font+'px')};
root.querySelectorAll('[data-read-jump]').forEach(link=>link.addEventListener('click',()=>{query.value='';select.value='all';filter()}));filter();
})();
'''
def render():
    source=(ROOT/'บทอ่านละเอียด.md').read_text()
    chunks=re.split(r'^## (.+)$',source,flags=re.M)
    intro=markdown.markdown(chunks[0],extensions=['tables','fenced_code'])
    chapters=[]
    for i in range(1,len(chunks),2):
        title=chunks[i]; body=markdown.markdown(chunks[i+1],extensions=['tables','fenced_code'])
        body=re.sub(r'(<table>.*?</table>)',r'<div class="table-scroll">\1</div>',body,flags=re.S)
        chapters.append((title,body))
    toc='<ol class="reading-toc">'+''.join(f'<li><a data-read-jump href="#read-ch-{i}">{E(title)}</a></li>' for i,(title,body) in enumerate(chapters))+'</ol>'
    controls='<div class="tools reading-tools noprint"><label>เลือกบท <select data-read-select><option value="all">ทุกบท</option>'+''.join(f'<option value="{i}">{E(t)}</option>' for i,(t,b) in enumerate(chapters))+'</select></label><label>ค้นหา <input type="search" data-read-search placeholder="เช่น ACK, subnet, RPO"></label><button data-read-reset>แสดงทุกบท</button><button data-read-smaller aria-label="ลดขนาดเนื้อหา">ก−</button><button data-read-larger aria-label="เพิ่มขนาดเนื้อหา">ก+</button><button data-read-print>พิมพ์ / บันทึก PDF</button><span data-read-status role="status"></span></div>'
    articles=''.join(f'<article id="read-ch-{i}" data-read-index="{i}"><h2>{E(title)}</h2>{body}<p class="reader-toplink"><a data-read-jump href="#reading-top">กลับสารบัญ ↑</a></p></article>' for i,(title,body) in enumerate(chapters))
    return '<div class="reading" id="reading"><div class="box" id="reading-top">'+intro+'</div><div class="box reading-toc-box"><h2>เลือกบทที่อยากเข้าใจก่อน</h2>'+toc+'</div>'+controls+'<p class="reading-empty" data-read-empty hidden>ไม่พบบทที่ตรงกับการค้นหา ลองเปลี่ยนคำหรือกดแสดงทุกบท</p>'+articles+'</div>'
def standalone(content):
    return '<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>351 บทอ่านละเอียด — เข้าใจเครือข่ายและ Cloud</title><style>body{margin:0;background:#eef2f6;color:#15243b;font-family:Tahoma,sans-serif}*{box-sizing:border-box}.wrap{max-width:1100px;margin:auto;padding:24px 18px 70px}.box{background:white;border:1px solid #d5dfeb;border-radius:14px;padding:25px;margin:20px 0}h1{font-size:clamp(26px,4vw,38px);line-height:1.5}a{color:#1746a2}button,input,select{font:inherit;padding:8px 12px;border:1px solid #c1cfdf;border-radius:8px;background:white;max-width:100%}button{cursor:pointer}.tools{display:flex;align-items:center;gap:12px;flex-wrap:wrap}table{border-collapse:collapse;width:100%}th,td{border:1px solid #c8d6e6;padding:10px;text-align:left}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #d99824;outline-offset:3px}'+CSS+'@media print{@page{size:A4;margin:17mm}body{background:white}.wrap{padding:0;max-width:none}.noprint{display:none!important}.box{border:0;padding:0}}</style></head><body><main class="wrap"><p class="noprint"><a href="351-สไลด์อ่านสอบ-ข้อกา200ข้อ.html">← เปิดสไลด์และข้อกา 200 ข้อ</a></p>'+content+'</main><script>'+JS+'</script></body></html>'
if __name__=='__main__':
    (ROOT/'351-บทอ่านละเอียด.html').write_text(standalone(render()))
    print('Built detailed reader')

from pathlib import Path
import struct,json
U=lambda b:struct.unpack('<%dI'%(len(b)//4),b)
def stream(path):
 b=path.read_bytes(); sz=1<<struct.unpack_from('<H',b,30)[0]; fatids=list(U(b[76:512])); nxt=struct.unpack_from('<I',b,68)[0]
 sec=lambda i:b[(i+1)*sz:(i+2)*sz]
 while nxt<0xfffffffa:
  v=U(sec(nxt));fatids+=list(v[:-1]);nxt=v[-1]
 fat=[]
 for i in fatids:
  if i<0xfffffffa: fat+=list(U(sec(i)))
 def chain(i):
  out=bytearray();seen=set()
  while i<0xfffffffa and i not in seen:
   seen.add(i);out+=sec(i);i=fat[i]
  return bytes(out)
 dirs=chain(struct.unpack_from('<I',b,48)[0]); entries=[]
 for i in range(0,len(dirs),128):
  x=dirs[i:i+128]; n=struct.unpack_from('<H',x,64)[0]
  if n>=2: entries.append((x[:n-2].decode('utf-16le'),struct.unpack_from('<I',x,116)[0],struct.unpack_from('<Q',x,120)[0]))
 for name,start,length in entries:
  if name=='PowerPoint Document':return chain(start)[:length]
 raise ValueError(path)
def records(b):
 pos=0
 while pos+8<=len(b):
  flags,typ,n=struct.unpack_from('<HHI',b,pos); data=b[pos+8:pos+8+n]
  if n>len(b)-pos-8:break
  yield typ,data,flags
  pos+=8+n

def texts(b):
 out=[]
 for typ,d,flags in records(b):
  if typ==4000:out.append(d.decode('utf-16le',errors='replace'))
  elif typ==4008:out.append(d.decode('cp1252',errors='replace'))
  elif flags&15==15:out.extend(texts(d))
 return out
all_decks=[]
for p in sorted(Path('DataCommunication_and_Networking').glob('ch*.ppt')):
 b=stream(p); slides=[]; outlines=[]
 def walk(b):
  for typ,d,flags in records(b):
   if typ==1006:slides.append('\n'.join(texts(d)))
   elif typ==4080:outlines.extend(texts(d))
   elif flags&15==15:walk(d)
 walk(b)
 Path('translations/_sources',p.stem+'.json').write_text(json.dumps({'slides':slides,'outlines':outlines},ensure_ascii=False,indent=2))
 Path('translations/_sources',p.stem+'.txt').write_text('\n\f\n'.join(slides)+'\nOUTLINE\n'+'\n'.join(outlines))
 print(p.stem,len(slides),sum(map(len,slides)),len(outlines),repr(' '.join(outlines)[:100]))

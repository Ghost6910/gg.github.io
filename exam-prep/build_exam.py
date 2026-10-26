from pathlib import Path
import json, html, random
from build_reading import render as render_reading, standalone, CSS as READING_CSS, JS as READING_JS
OUT=Path(__file__).parent
sections=[]
def section(name,slides,rows):
    qs=[]
    for line in rows.strip().splitlines():
        parts=line.split('|')
        assert len(parts)==6,(name,line)
        q,a,b,c,d,e=parts
        qs.append(dict(q=q,options=[a,b,c,d],explain=e,cat=name))
    assert len(qs)==25,(name,len(qs))
    sections.append(dict(name=name,slides=slides,questions=qs))
section('OSI และ Internet Stack',[
('ภาพรวมเส้นทางข้อมูล',['แอปสร้างข้อมูล → Transport → Network → Link → Physical','ฝั่งรับถอดส่วนหุ้มย้อนลำดับจนถึงแอป','จำด้วยการเปิดเว็บ: HTTP → TCP → IP → Ethernet/Wi-Fi → สื่อ'], 'แต่ละชั้นใช้บริการของชั้นล่าง และให้บริการชั้นบน'),
('OSI 7 ชั้น จำจากบนลงล่าง',['7 Application: บริการให้แอป เช่น HTTP, DNS','6 Presentation: รูปแบบข้อมูล การเข้ารหัส การบีบอัด','5 Session: จัดการบทสนทนา • 4 Transport: สื่อสารระหว่าง process','3 Network: IP และ routing • 2 Data Link: frame/MAC • 1 Physical: bit/สัญญาณ'], 'ชื่อชั้นกับหน้าที่ต้องจับคู่ได้ ไม่ใช่จำลำดับอย่างเดียว'),
('TCP/IP เทียบกับ OSI',['Internet stack แบบ 5 ชั้น: Application, Transport, Network, Link, Physical','TCP/IP แบบ 4 ชั้นรวม Link + Physical เป็น Network access','OSI ชั้น 5–7 มักรวมอยู่ใน Application ของ TCP/IP'], 'ข้อสอบถามจำนวนชั้น ต้องดูว่าใช้แบบจำลอง 4, 5 หรือ 7 ชั้น'),
('ชื่อข้อมูลและที่อยู่',['TCP segment / UDP datagram → IP packet → Link frame → bits','Port ระบุบริการ/process • IP ระบุ interface ในเชิงเครือข่าย • MAC ใช้ส่งบนลิงก์','Switch Ethernet โดยทั่วไปทำงานชั้น 2 • Router ชั้น 3 • Repeater ชั้น 1'], 'อุปกรณ์จริงอาจทำหลายชั้น ให้ตอบตามหน้าที่ที่โจทย์ระบุ'),
('Delay และ Throughput',['Transmission delay = L/R โดย L เป็นบิต และ R เป็นบิตต่อวินาที','Propagation delay = ระยะทาง/ความเร็วสัญญาณ','End-to-end delay รวม processing + queueing + transmission + propagation','Throughput ถูกจำกัดด้วยคอขวด ไม่ใช่ผลบวกความเร็วทุกลิงก์'], '1,500 bytes บน 10 Mb/s → 12,000/10,000,000 = 1.2 ms'),
('Encapsulation ข้าม Router',['ในกรณีไม่ใช้ NAT: IP ต้นทางและปลายทางโดยทั่วไปคงเดิม','Router ลด TTL และสร้าง frame ใหม่บนลิงก์ขาออก','MAC ต้นทาง/ปลายทางเปลี่ยนตามลิงก์ ไม่ได้ใช้ MAC ของเว็บเซิร์ฟเวอร์ตลอดทาง'], 'แยกปลายทาง IP ออกจาก next-hop MAC เสมอ')],'''
OSI ชั้นใดรับผิดชอบ routing เป็นหลัก|Network|Transport|Presentation|Physical|Network ใช้ที่อยู่เชิงตรรกะและเลือกทางข้ามเครือข่าย
การส่งบิตเป็นสัญญาณบนสายตรงกับชั้นใด|Physical|Application|Session|Network|Physical จัดการสัญญาณและสื่อส่งข้อมูล
MAC address เกี่ยวข้องโดยตรงกับชั้นใด|Data Link|Transport|Session|Application|Ethernet frame ใช้ MAC ในชั้น Data Link
Port number ใช้ระบุสิ่งใดเป็นหลัก|บริการหรือ process ปลายทาง|หมายเลขสาย LAN|ความยาวคลื่นแสง|ตำแหน่งในตู้ rack|Transport ใช้ port เพื่อส่งข้อมูลให้ process ที่เหมาะสม
HTTP อยู่ในชั้นใดของ Internet stack|Application|Link|Physical|Network|HTTP กำหนดการแลกเปลี่ยนข้อความของเว็บ
TCP อยู่ชั้นใด|Transport|Application|Data Link|Physical|TCP ให้บริการ byte stream ระหว่าง process
IP อยู่ชั้นใด|Network|Session|Physical|Presentation|IP ส่ง packet ระหว่างเครือข่าย
หน่วยข้อมูลของ Ethernet เรียกว่าอะไร|Frame|TCP segment|HTTP cookie|DNS zone|Ethernet เป็นเทคโนโลยีชั้นลิงก์ หน่วยข้อมูลคือ frame
Encapsulation หมายถึงอะไร|เพิ่มข้อมูลควบคุมแต่ละชั้นหุ้มข้อมูล|ลบทุก header ก่อนส่ง|แปลง IP เป็นชื่อโดเมนเท่านั้น|เลือกช่อง Wi-Fi อัตโนมัติ|การหุ้มข้อมูลเพิ่ม header และบางชั้นมี trailer
Decapsulation เกิดอย่างไรที่ผู้รับ|ถอดข้อมูลควบคุมจากชั้นล่างขึ้นชั้นบน|เพิ่ม header ซ้ำทุกชั้น|เปลี่ยนทุก frame เป็น broadcast|ลบ payload ทั้งหมด|ผู้รับตรวจและถอดส่วนหุ้มย้อนลำดับการส่ง
OSI ชั้นใดเกี่ยวกับรูปแบบข้อมูลตามแบบจำลอง|Presentation|Network|Physical|Data Link|Presentation ครอบคลุมการแทนข้อมูล บีบอัด และเข้ารหัสในเชิงแบบจำลอง
OSI ชั้นใดจัดการบทสนทนา|Session|Physical|Network|Data Link|Session เป็นชั้นที่ 5
ข้อใดเรียง Internet stack จากบนลงล่างถูกต้อง|Application Transport Network Link Physical|Physical Link Application Transport Network|Network Application Physical Link Transport|Transport Application Link Physical Network|ข้อมูลลงตามลำดับก่อนถูกส่งเป็นสัญญาณ
แบบ TCP/IP 4 ชั้นรวมชั้นใดของแบบ 5 ชั้น|Link กับ Physical|Application กับ Network|Transport กับ Physical|Network กับ Application|แบบ 4 ชั้นใช้ Network access รวมหน้าที่ลิงก์และสื่อ
อุปกรณ์ใดส่งต่อโดยดู IP ปลายทางเป็นหลัก|Router|Repeater|Hub แบบดั้งเดิม|Patch panel|Router ใช้ routing table ส่งต่อ packet
Ethernet switch ทั่วไปเลือกพอร์ตส่งต่อจากอะไร|MAC ปลายทาง|HTTP method|ชื่อผู้ใช้เว็บ|TCP window เท่านั้น|Switch ชั้น 2 ใช้ MAC table
Repeater ทำงานหลักที่ชั้นใด|Physical|Application|Transport|Session|Repeater ฟื้นสัญญาณเพื่อส่งต่อ
ข้อมูล 1000 bytes ส่งที่ 1 Mb/s ใช้ transmission delay เท่าไร|8 ms|1 ms|1000 ms|0.008 ms|1000 คูณ 8 หาร 1000000 วินาที เท่ากับ 8 ms
ลิงก์ยาว 2000 km สัญญาณเร็ว 200000 km/s มี propagation delay เท่าไร|10 ms|1 ms|100 ms|1000 ms|2000/200000 เท่ากับ 0.01 วินาที
ลิงก์ต่ออนุกรม 100 20 50 Mb/s คอขวดตามอุดมคติคือเท่าไร|20 Mb/s|170 Mb/s|100 Mb/s|50 Mb/s|อัตราส่งต่อเนื่องถูกจำกัดด้วยลิงก์ช้าที่สุด
เวลารอคิวใน router จัดเป็น delay ชนิดใด|Queueing|Propagation|Encoding เท่านั้น|Session|Queueing เปลี่ยนตามปริมาณจราจรและคิว
ข้าม router โดยไม่ใช้ NAT ที่อยู่ใดโดยทั่วไปยังคงเดิม|IP ต้นทางและปลายทาง|MAC ของทุก frame|TTL|Ethernet FCS|Router เปลี่ยน frame และลด TTL แต่ไม่ได้ทำ NAT ตามเงื่อนไข
TTL ของ IPv4 มีหน้าที่หลักใด|จำกัดการวนของ packet|กำหนดความยาวสาย|เข้ารหัส payload|กำหนด port เว็บ|Router ลด TTL และทิ้ง packet เมื่อหมด
Protocol หมายถึงข้อใด|กติกาของรูปแบบและการแลกเปลี่ยนข้อความ|ยี่ห้ออุปกรณ์เท่านั้น|ชนิดสายไฟเท่านั้น|ความเร็วซีพียู|คู่สื่อสารต้องเข้าใจกติกาตรงกัน
การเพิ่มอัตราส่ง R โดยคง L เท่าเดิมทำให้สิ่งใดลดลงโดยตรง|Transmission delay|ระยะทางลิงก์|Propagation speed|จำนวนชั้น OSI|จากสูตร L/R เมื่อ R เพิ่ม เวลาผลักบิตลงลิงก์ลดลง
''')
section('Application และ Web',[
('TCP กับ UDP',['TCP: reliable byte stream เรียงลำดับ มี flow/congestion control','UDP: ไม่ตั้ง connection และไม่รับประกันการส่งถึง/ลำดับด้วยตัวมันเอง','TCP handshake: SYN → SYN-ACK → ACK','TCP นับ sequence ตาม byte ไม่ใช่จำนวน segment'], 'Seq=1000 ส่ง payload 200 bytes ครบต่อเนื่อง → ACK=1200'),
('Web และ HTTP',['Client ส่ง request → server ส่ง response','GET ขอ representation • POST ส่งข้อมูลให้ประมวลผล','200 สำเร็จ • 301 ย้ายถาวร • 404 ไม่พบ • 500 server error','HTTPS คือ HTTP ที่ได้รับการปกป้องด้วย TLS; ตรวจ certificate และชื่อโดเมน'], 'HTTPS ไม่ใช่หลักฐานว่าเนื้อหาของเว็บไซต์เชื่อถือได้เสมอ'),
('DNS และ DHCP',['DNS แปลงชื่อเป็นข้อมูล เช่น A=IPv4, AAAA=IPv6, MX=mail server','Cache ช่วยลด delay/โหลด; TTL ของ DNS ระบุอายุ cache','DHCP แจก IP, mask, gateway, DNS; DORA = Discover Offer Request ACK'], 'DNS ช่วยรู้ปลายทาง แต่ไม่ได้ส่งหน้าเว็บให้เรา'),
('Port ที่ควรจำ',['HTTP TCP 80 • HTTPS โดยทั่วไป TCP 443; HTTP/3 ใช้ QUIC บน UDP 443','DNS UDP/TCP 53 • DHCPv4 server UDP 67 / client UDP 68','SSH TCP 22 • Telnet TCP 23 • SMTP TCP 25','POP3 TCP 110 • IMAP TCP 143 • FTP control TCP 21'], 'Port เป็นค่าที่ใช้โดยทั่วไป ผู้ดูแลเปลี่ยนการตั้งค่าได้'),
('Email และรูปแบบระบบ',['SMTP: ส่ง/ถ่ายทอดอีเมล • IMAP: จัดการ mailbox บน server • POP3: รับเมล','Client-server มี server ให้บริการ; P2P โหนดทำหน้าที่ได้ทั้งรับและให้','Cookie เป็นข้อมูลประกอบสถานะที่ browser ส่งกลับตามขอบเขตที่กำหนด'], 'HTTP เป็น stateless แต่แอปสร้าง session ด้วย cookie/token ได้'),
('ไล่เหตุเปิดเว็บไม่ได้',['ตรวจ Link/Wi-Fi → IP/mask → gateway → เส้นทาง → DNS → บริการเว็บ','เข้า IP ได้แต่ชื่อไม่ได้: ตรวจ DNS; ping ไม่ผ่านอาจเป็นเพราะ ICMP ถูกบล็อก','Ping ผ่านยืนยันการตอบ ICMP ไม่ได้ยืนยันว่า TCP 443 หรือ HTTP ใช้งานได้'], 'ทดสอบเป็นชั้นและใช้หลักฐาน ไม่ด่วนสรุปจากอาการเดียว')],'''
โปรโตคอลใดให้ reliable byte stream|TCP|UDP|IP|ARP|TCP ส่งซ้ำและเรียง byte ให้แอป
UDP มีคุณสมบัติใด|ไม่รับประกันการส่งถึงด้วยตัวมันเอง|รับประกันไม่มีข้อมูลหาย|มี handshake แบบ TCP ทุกครั้ง|เรียงข้อมูลให้เสมอ|แอปที่ใช้ UDP สามารถเพิ่ม reliability ของตนเองได้
TCP handshake ที่ถูกต้องคืออะไร|SYN SYN-ACK ACK|ACK FIN SYN|GET POST ACK|Discover Offer ACK|TCP ตั้ง connection ด้วย three-way handshake
TCP Seq 500 ส่งข้อมูล 100 bytes ครบ ผู้รับคาดหวัง ACK ใด|600|501|100|599|ACK ระบุหมายเลข byte ถัดไปที่คาดหวัง
HTTP GET ใช้ทำอะไรโดยหลัก|ขอ representation ของทรัพยากร|แจก IP อัตโนมัติ|หา MAC ของ gateway|เลือกเส้นทาง OSPF|GET เป็น method สำหรับดึง representation
HTTP 404 หมายถึงอะไร|ไม่พบทรัพยากรที่ร้องขอ|สำเร็จเสมอ|ย้ายถาวร|DNS cache หมดอายุ|404 เป็นสถานะ Not Found
HTTP 500 หมายถึงอะไร|ข้อผิดพลาดภายใน server|พบทรัพยากร|ต้องเปลี่ยนสาย LAN|client ได้ IP ใหม่|500 เป็นสถานะฝั่ง server
HTTPS เพิ่มสิ่งใดให้ HTTP|การปกป้องการสื่อสารด้วย TLS|การรับประกันเนื้อหาถูกต้องทุกเรื่อง|การแจก IP|การแทน routing table|TLS ให้การเข้ารหัส ความครบถ้วน และการยืนยันตัวตนตามการตรวจสอบ
DNS A record เก็บอะไร|IPv4 address|IPv6 address|MAC ของ switch|หมายเลข VLAN|A จับคู่ชื่อกับ IPv4
DNS AAAA record เก็บอะไร|IPv6 address|IPv4 address|รหัสผ่านอีเมล|TCP sequence|AAAA ใช้ที่อยู่ IPv6
DNS MX record ใช้ระบุอะไร|Mail server ของโดเมน|Subnet mask|Default VLAN|ลำดับสายสี|MX ระบุ mail exchanger
DNS ใช้ port มาตรฐานใด|53|80|22|67|DNS ใช้ทั้ง UDP และ TCP port 53 ตามกรณี
HTTP ปกติใช้ TCP port ใดโดยทั่วไป|80|443|25|23|80 เป็นพอร์ตมาตรฐานของ HTTP แบบไม่ใช้ TLS
HTTPS โดยทั่วไปใช้ port ใด|443|110|68|21|HTTPS โดยทั่วไปใช้ TCP 443 และ HTTP/3 ใช้ UDP 443
SSH ใช้ TCP port ใดโดยทั่วไป|22|23|53|143|SSH ใช้พอร์ต 22 และเข้ารหัส session
เหตุใด Telnet จึงไม่เหมาะกับการส่งรหัสผ่านบนเครือข่ายที่ไม่เชื่อถือ|ไม่เข้ารหัสการสื่อสารโดยตัวมันเอง|ใช้ได้แค่ใยแก้ว|ไม่มี client|ต้องใช้ IPv6 เท่านั้น|Telnet ส่งข้อมูลแบบ plaintext ควรเลือก SSH เมื่อเหมาะสม
SMTP มีหน้าที่หลักใด|ส่งและถ่ายทอดอีเมล|แปลงชื่อโดเมน|แจก MAC address|เลือกช่องสัญญาณ|SMTP ใช้ส่งเมลระหว่าง client/server และระหว่าง server
IMAP เหมาะกับกรณีใด|จัดการ mailbox จากหลายอุปกรณ์บน server|คำนวณ subnet mask|ทำ Ethernet CRC|แจก route OSPF|IMAP คงข้อมูลและสถานะ mailbox ที่ server
FTP control connection โดยทั่วไปใช้ TCP port ใด|21|20|80|25|Port 21 ใช้ควบคุม ส่วนช่องข้อมูลขึ้นกับโหมด
DHCPv4 เรียงขั้นตอนหลักอย่างไร|Discover Offer Request ACK|ACK Request Offer Discover|SYN SYN-ACK ACK FIN|GET DNS POST ACK|ลำดับ DORA ใช้ขอและยืนยันการเช่า IP
DHCPv4 server รับข้อความที่ UDP port ใด|67|68|53|22|Server ใช้ 67 ส่วน client ใช้ 68
HTTP cookie ช่วยทำอะไร|ประกอบการติดตามสถานะของแอป|แทน subnet mask|เข้ารหัสสายไฟ|เพิ่มกำลังส่ง AP|Cookie ช่วยเชื่อม request กับสถานะหรือ session ตามที่แอปออกแบบ
เข้าเว็บไซต์ด้วย IP ได้แต่ใช้ชื่อไม่ได้ ควรตรวจอะไรเป็นลำดับต้น|DNS configuration|สีสายทั้งแปดเส้นเท่านั้น|ขนาดจอ|ชื่อ VLAN อย่างเดียว|อาการชี้ไปที่การ resolve ชื่อ แม้ต้องพิจารณาการตั้งค่าเว็บร่วมด้วย
Ping server ผ่านแต่เปิดเว็บไม่ได้ ข้อใดถูกต้อง|ต้องตรวจพอร์ตและบริการเว็บต่อ|HTTP ต้องปกติแน่นอน|DNS ถูกเสมอ|สายขาดแน่นอน|ICMP ตอบไม่ได้ยืนยันว่า TCP หรือ HTTP พร้อมให้บริการ
HTTP 301 หมายถึงอะไร|ย้ายทรัพยากรอย่างถาวร|ไม่พบทรัพยากร|server error ภายใน|ยืนยัน DHCP lease|301 เป็นสถานะ Moved Permanently
''')
section('Routing และ Subnet',[
('Forwarding กับ Routing',['Routing สร้าง/เรียนรู้เส้นทาง • Forwarding ส่ง packet ตามตาราง','Static route ตั้งเอง; Dynamic route เรียนรู้ด้วย protocol','Default route IPv4 = 0.0.0.0/0 ใช้เมื่อไม่มี prefix ที่จำเพาะกว่า'], 'Router เลือก longest prefix match จาก route ที่ติดตั้งแล้ว'),
('เลือก Route อย่าสลับขั้นตอน',['ตอนสร้าง routing table: เส้นทางไป prefix เดียวกันจากต่างแหล่งเปรียบเทียบ AD','ภายใน protocol ใช้ metric ตามกติกาของ protocol','ตอนส่ง packet: เลือก prefix ที่ match ยาวที่สุด; /24 ชนะ /16','Cisco ค่าเริ่มต้นตัวอย่าง: connected 0, static 1, OSPF 110, RIP 120'], 'อย่าใช้ AD ของ /0 มาชนะ /24 ในการ forwarding'),
('IPv4 และ Prefix',['IPv4 32 bits; /n คือจำนวนบิตส่วน network','จำนวน address = 2^(32−n); subnet IPv4 ปกติมี usable host = จำนวนทั้งหมด−2','/24 = 255.255.255.0 • /26 = 255.255.255.192 • /27 = 255.255.255.224','ข้อยกเว้น /31 point-to-point และ /32 ไม่ใช้สูตร host−2 แบบทั่วไป'], 'Network = IP AND mask; broadcast คือ host bits เป็น 1 ทั้งหมด'),
('ตัวอย่าง Subnet /26',['192.168.1.70/26: block size 64 → ช่วง 64–127','Network 192.168.1.64 • Broadcast 192.168.1.127','Usable 192.168.1.65–126 มี 62 hosts','ต้องรองรับ 50 hosts → /26 พอ; /27 มีเพียง 30'], 'นับจำนวน address ทั้งหมดกับ usable hosts แยกกัน'),
('Routing Protocol และ Gateway',['RIP: distance vector ใช้ hop count; OSPF: link state ใช้ cost','Default gateway เป็น router interface ใน subnet ของ host โดยทั่วไป','ARP หา MAC ของ next hop บนลิงก์ IPv4; NAT แปลงที่อยู่ตามกฎ','Private IPv4: 10/8, 172.16/12, 192.168/16'], 'ปลายทางต่าง subnet ให้ส่ง frame ไป gateway ไม่ใช่ ARP หาเว็บ server ที่อยู่นอก LAN'),
('อ่านผังเครือข่าย',['Star มีจุดศูนย์กลาง • Bus ใช้ backbone ร่วม • Ring เชื่อมเป็นวง','Full mesh n โหนด ใช้ n(n−1)/2 ลิงก์ เมื่อแต่ละคู่เชื่อมกันโดยตรง','Router แบ่ง broadcast domain; VLAN แยก broadcast domain เชิงตรรกะ','ตรวจ IP/mask แต่ละ interface และ route ไป-กลับก่อนสรุปว่า ping ได้'], '4 โหนด full mesh → 4×3/2 = 6 ลิงก์')],'''
Routing ต่างจาก forwarding อย่างไร|Routing หาเส้นทาง ส่วน forwarding ส่งตามตาราง|Routing คือเข้ารหัส ส่วน forwarding คือ DNS|ทั้งคู่เป็นการต่อสายเท่านั้น|Forwarding ใช้ได้เฉพาะ Wi-Fi|Control plane สร้างเส้นทางและ data plane ส่ง packet
มี route 10.0.0.0/8 และ 10.1.2.0/24 ปลายทาง 10.1.2.5 เลือกอะไร|10.1.2.0/24|10.0.0.0/8|ต้องทิ้งเสมอ|เลือกแบบสุ่ม|/24 match ยาวกว่า /8
Default route IPv4 เขียนอย่างไร|0.0.0.0/0|255.255.255.255/32|127.0.0.1/8|224.0.0.0/4|/0 match ได้ทุกปลายทางแต่จำเพาะน้อยที่สุด
Static route หมายถึงอะไร|เส้นทางที่ผู้ดูแลกำหนดเอง|เส้นทางที่ RIP เรียนรู้เท่านั้น|สายที่ไม่มีสัญญาณ|ARP entry ทุกชนิด|Static route ตั้งค่าโดยผู้ดูแล
OSPF จัดเป็น routing แบบใด|Link state|Distance vector แบบ RIP|Application proxy|Physical encoding|OSPF ใช้ข้อมูล link state เพื่อคำนวณเส้นทาง
RIP ใช้ metric หลักใด|Hop count|กำลังแสง|หมายเลข port|ชื่อเครื่อง|RIP นับ hop และกำหนด 16 เป็น unreachable
Cisco default AD ของ static route ทั่วไปคือเท่าไร|1|0|110|120|Connected เป็น 0 และ static ปกติเป็น 1
AD ใช้เปรียบเทียบกรณีใด|ต่างแหล่ง route ไปยัง prefix เดียวกัน|ความยาวสีสาย|HTTP status ต่างชนิด|ความยาวรหัสผ่าน|AD ใช้ความน่าเชื่อถือแหล่ง route ไม่แทน longest prefix match
IPv4 มีความยาวเท่าไร|32 bits|48 bits|64 bits|128 bits|IPv4 มี 4 octets รวม 32 bits
/24 ตรงกับ mask ใด|255.255.255.0|255.255.0.0|255.255.255.192|255.0.0.0|24 บิตแรกเป็น 1 เหลือ host 8 บิต
/26 มี usable hosts ใน subnet IPv4 ปกติกี่เครื่อง|62|64|30|126|2 ยกกำลัง 6 ลบ network และ broadcast เหลือ 62
/27 มี address ทั้งหมดกี่ค่า|32|30|64|16|32 ลบ 27 เหลือ 5 host bits จึงมี 32 ค่า
192.168.1.70/26 มี network address ใด|192.168.1.64|192.168.1.0|192.168.1.70|192.168.1.128|ช่วง /26 เพิ่มครั้งละ 64 และ 70 อยู่ช่วง 64–127
Broadcast ของ 192.168.1.70/26 คืออะไร|192.168.1.127|192.168.1.63|192.168.1.255|192.168.1.64|บิต host เป็น 1 ทั้งหมดจึงเป็นปลายช่วง 127
Subnet IPv4 ปกติที่เล็กที่สุดสำหรับ 50 hosts คืออะไร|/26|/27|/28|/29|/26 มี 62 usable ส่วน /27 มี 30
ข้อใดเป็น private IPv4|172.20.1.1|172.40.1.1|8.8.8.8|1.1.1.1|172.16.0.0 ถึง 172.31.255.255 เป็น private
เครื่องจะส่งไปต่าง subnet โดยทั่วไปต้องส่ง frame ให้ใคร|Default gateway|DNS server เสมอ|ทุกเครื่องในโลก|DHCP server เสมอ|Gateway รับ packet เพื่อ route ต่อไป
ARP ใน IPv4 ใช้ทำอะไร|หา MAC ของ next hop บนลิงก์|หา port ของ HTTP|แจก subnet mask|เข้ารหัส packet|ARP resolve IPv4 เป็น MAC ใน broadcast domain
Router ช่วยแบ่งสิ่งใดโดยทั่วไป|Broadcast domain|อักขระใน URL|TCP payload เป็นตัวอักษร|DNS zone เสมอ|Router ไม่ส่งต่อ layer-2 broadcast ข้าม interface ตามปกติ
Full mesh 5 โหนดต้องใช้ลิงก์ตรงระหว่างคู่กี่เส้น|10|5|20|25|5 คูณ 4 หาร 2 เท่ากับ 10
Topology ที่มีอุปกรณ์กลางเชื่อมทุกโหนดคืออะไร|Star|Bus|Ring|Linear chain|Star มีศูนย์กลาง เช่น switch
Topology แบบ bus พึ่งพาสิ่งใดร่วมกัน|Backbone หลัก|Router แยกทุกคู่|เส้นใยสองวงเสมอ|Cloud region|Bus ใช้สื่อหลักร่วมกัน
NAT ทำหน้าที่ใด|แปลงที่อยู่ IP ตามกฎ|แจกชื่อ SSID|แก้ไขสีสาย|แทนที่ DNS ทุกกรณี|NAT เปลี่ยนที่อยู่ และ PAT แปลง port ร่วมด้วยได้
192.168.10.33/27 อยู่ช่วง usable ใด|192.168.10.33–62|192.168.10.1–30|192.168.10.65–94|192.168.10.32–63|Network คือ 32 broadcast 63 จึงใช้ host 33–62
มี /24 ที่ AD 110 และ /0 ที่ AD 1 ติดตั้งแล้ว ปลายทาง match ทั้งคู่เลือกอะไร|/24|/0|AD เฉลี่ย|ทิ้งเพราะ AD ต่างกัน|ตอน forwarding ใช้ longest prefix match จากเส้นทางที่ติดตั้งแล้ว
''')
section('Link Layer และ LAN',[
('บริการของ Link Layer',['Framing กำหนดขอบเขต frame • MAC addressing • Medium access','Error detection เช่น CRC ตรวจความผิดพลาด แต่ไม่ได้แก้ข้อมูลโดยตัวมันเอง','Reliability ขึ้นกับเทคโนโลยี ไม่ใช่ทุกลิงก์มี ACK/retransmission'], 'TCP reliability คนละระดับกับ link-layer reliability'),
('Ethernet Frame และ Switch',['Frame มี source/destination MAC, type/length, payload และ FCS','Switch เรียนรู้ source MAC กับพอร์ตขาเข้า','Known unicast ส่งไปพอร์ตที่เรียนรู้; unknown unicast flood ภายใน VLAN ยกเว้นพอร์ตรับ','Broadcast MAC = FF:FF:FF:FF:FF:FF'], 'การเรียนรู้ดู source; การตัดสินใจส่งต่อดู destination'),
('Collision และ Broadcast Domain',['Switch แยก collision domain ตามพอร์ต; full-duplex ไม่มี collision ตามปกติ','Hub แบบเก่าให้หลายเครื่องแชร์ collision domain','VLAN แต่ละวงเป็น broadcast domain แยกกัน; ต้อง route เพื่อข้าม VLAN','Trunk พา traffic หลาย VLAN; 802.1Q ใช้ tag ระบุ VLAN'], 'Switch ทั้งตัวไม่จำเป็นต้องมี broadcast domain เดียว หากแบ่ง VLAN'),
('Medium Access และ Duplex',['Ethernet แบบ shared half-duplex เดิมใช้ CSMA/CD','Ethernet switched full-duplex ไม่ต้องใช้ CSMA/CD','Wi-Fi ใช้ CSMA/CA เพราะตรวจ collision ระหว่างส่งได้ยาก','Half-duplex ผลัดกันส่ง • Full-duplex ส่งและรับพร้อมกัน'], 'CD = detect; CA = avoid'),
('Error Detection และการวนลูป',['Parity ตรวจข้อผิดพลาดบางรูปแบบ • CRC ใช้ตรวจความผิดพลาดแบบ polynomial','FCS ผิด → โดยทั่วไปทิ้ง frame ไม่ใช่แก้ทุกบิตให้เอง','STP สร้าง topology ที่ไม่เกิด loop ใน LAN ที่มีเส้นทางซ้ำ','Loop อาจทำให้ broadcast storm และ MAC table ไม่นิ่ง'], 'STP บล็อกบางเส้นทางเพื่อคงเส้นสำรองโดยไม่เกิด loop'),
('ARP ข้าม Subnet: ภาพจำ',['Host A → Switch → Router → Switch → Server','A ส่ง IP ถึง server แต่ MAC ปลายทางของ frame แรกคือ gateway','Router ถอด frame และสร้าง frame สำหรับลิงก์ถัดไป','Frame ขาออกมี MAC ต้นทางของ interface router บนลิงก์นั้น'], 'ทุก hop ใช้ link addressing ตามบริบทลิงก์ ไม่ใช่ end-to-end MAC')],'''
หน้าที่หลักของ framing คืออะไร|กำหนดขอบเขตหน่วยข้อมูลบนลิงก์|หา DNS server|เข้ารหัสอีเมล|กำหนด route BGP|Framing แยกข้อมูลเป็น frame ที่ผู้รับตีความได้
Ethernet switch เรียนรู้ MAC table จากข้อมูลใด|Source MAC และพอร์ตรับ|Destination IP และ DNS|HTTP cookie|ชื่อ SSID|Source MAC บอกว่าเครื่องต้นทางอยู่ทางพอร์ตใด
Known unicast ที่พอร์ตปลายทางต่างจากพอร์ตรับควรถูกส่งอย่างไร|ส่งออกพอร์ตที่ MAC table ระบุ|ส่งทุกพอร์ตทุก VLAN|ส่งกลับพอร์ตรับเสมอ|ทิ้งเสมอ|Switch ใช้ destination MAC ค้นพอร์ตที่เรียนรู้
Unknown unicast ถูกจัดการโดย switch ทั่วไปอย่างไร|Flood ใน VLAN เดียวกันยกเว้นพอร์ตรับ|Route ออกทุกเครือข่าย|ส่งไป DNS เท่านั้น|แก้ MAC เป็น IP|ยังไม่รู้พอร์ตจึงกระจายเฉพาะขอบเขต VLAN
Ethernet broadcast MAC คือข้อใด|FF:FF:FF:FF:FF:FF|00:00:00:00:00:00|127.0.0.1|255.255.255.0|MAC broadcast มีทั้ง 48 บิตเป็น 1
MAC address Ethernet โดยทั่วไปยาวเท่าไร|48 bits|32 bits|16 bits|128 bits|EUI-48 มี 6 octets
FCS ใน Ethernet ใช้ทำอะไร|ตรวจความผิดพลาดของ frame|เลือก default route|แจก IP|เก็บรหัสผ่าน|FCS เก็บค่าตรวจ CRC
CRC ที่ตรวจพบความผิดพลาดทำอะไรได้โดยตรง|ระบุว่า frame ผิดพลาดตามความสามารถการตรวจ|แก้ทุกบิตได้เสมอ|รับรองไม่ถูกโจมตี|คำนวณ subnet ให้|CRC เป็น error detection ไม่ใช่กลไกแก้บิตทั่วไป
Ethernet switched full-duplex ใช้ CSMA/CD หรือไม่|ไม่ใช้ในการทำงาน full-duplex ปกติ|ใช้ตรวจ collision ทุก frame|ใช้แทน DNS|ใช้เฉพาะพอร์ต 443|ไม่มีการแย่งสื่อร่วมแบบ half-duplex
Ethernet shared half-duplex แบบเดิมใช้วิธีใด|CSMA/CD|CSMA/CA|OSPF|DORA|CSMA/CD ตรวจ collision บนสื่อร่วม
Wi-Fi ใช้แนวทางใดเข้าถึงสื่อ|CSMA/CA|CSMA/CD แบบ Ethernet เดิม|SMTP|NAT|Wi-Fi ลดโอกาสชนด้วยการฟังสื่อและ backoff
Hub แบบดั้งเดิมทำให้พอร์ตอยู่ในอะไร|Collision domain ร่วมกัน|คนละ broadcast domain เสมอ|คนละ IP subnet เสมอ|คนละ DNS zone|Hub กระจายสัญญาณและทุกเครื่องแชร์สื่อ
Switch ช่วยแยก collision domain อย่างไร|โดยทั่วไปแยกตามพอร์ต|ทั้งตัวยังแชร์เหมือน hub เสมอ|แยกตาม URL|แยกตาม DNS cache|แต่ละพอร์ตเป็นลิงก์แยก
VLAN ใช้แบ่งอะไรเป็นหลัก|Broadcast domain เชิงตรรกะ|ความยาวบิต TCP|กำลังแสง|HTTP method|แต่ละ VLAN แยกการกระจาย broadcast
เครื่องต่าง VLAN ต้องใช้อะไรสื่อสาร IP ข้ามกัน|Routing ระหว่าง VLAN|Hub เพียงอย่างเดียว|สาย crossover เพียงอย่างเดียว|เปลี่ยนชื่อเครื่อง|ต้องมีอุปกรณ์หรือฟังก์ชันชั้น 3
Trunk link มีหน้าที่อะไร|ขนส่ง traffic ได้หลาย VLAN|ขยายกำลังคลื่นเท่านั้น|แจก DHCP ทุกครั้ง|แปลง IPv4 เป็น IPv6 เสมอ|Trunk รวมหลาย VLAN บนลิงก์เดียว
802.1Q เกี่ยวข้องกับอะไร|VLAN tagging|DNS caching|HTTP encryption|กำหนดชื่อ SSID|802.1Q กำหนด tag เพื่อระบุ VLAN
STP มีวัตถุประสงค์หลักใด|ป้องกัน loop ชั้น 2|เพิ่ม port TCP|แจก IPv6|เข้ารหัส Wi-Fi|STP เลือก topology ที่ไม่เกิด loop
Layer-2 loop อาจทำให้เกิดอะไร|Broadcast storm|DNS TTL เพิ่มเอง|สายใยแก้วกลายเป็นทองแดง|TCP port เปลี่ยนทุกเครื่อง|Frame วนและถูกทำสำเนาส่งต่อเพิ่มได้
Full-duplex หมายถึงอะไร|ส่งและรับพร้อมกันได้|ส่งได้ทิศเดียว|ผลัดกันส่งเท่านั้น|ส่งได้เฉพาะ broadcast|Full-duplex ใช้การส่งทั้งสองทิศพร้อมกัน
Half-duplex หมายถึงอะไร|สื่อสารสองทิศแต่ผลัดกัน|รับพร้อมส่งเสมอ|มีสายครึ่งเส้น|ใช้ได้เฉพาะแสง|ตัวอย่างเชิงหลักการคือวิทยุกดพูด
Host ส่ง IP ไป server ต่าง subnet MAC ปลายทาง frame แรกคืออะไร|MAC ของ default gateway|MAC ของ server ระยะไกลเสมอ|MAC ของ DNS เสมอ|MAC ศูนย์ทั้งหมด|การส่งบนลิงก์แรกต้องถึง next hop
หาก switch รู้ว่าปลายทางอยู่พอร์ตเดียวกับที่รับ frame จะทำอย่างไรโดยทั่วไป|ไม่ส่ง frame กลับพอร์ตนั้น|Flood ทุก VLAN|เปลี่ยน IP ปลายทาง|ตั้ง default route ใหม่|ไม่ต้องส่งกลับไปยังส่วนเครือข่ายที่ frame มาจาก
ARP request บน Ethernet ปกติส่งแบบใด|Broadcast ใน VLAN|Unicast ถึงทุก router ในโลก|Multicast IPv6 เท่านั้น|TCP stream|ผู้ถามยังไม่รู้ MAC ของ IPv4 เป้าหมายจึง broadcast
Parity แบบบิตเดียวรับรองตรวจข้อผิดพลาดทุกชนิดหรือไม่|ไม่รับรอง โดยเฉพาะจำนวนบิตพลิกเป็นคู่|รับรองทุกกรณี|แก้ได้ทุกบิต|แทน CRC และ TLS ได้ทั้งหมด|Even หรือ odd parity อาจไม่เปลี่ยนเมื่อพลิกจำนวนบิตเป็นคู่
''')
section('LAN Cabling',[
('เลือกสื่อให้เหมาะกับงาน',['UTP: คู่สายบิดเกลียว ไม่มีชิลด์; STP มีชิลด์ ต้องติดตั้งและต่อกราวด์เหมาะสม','Fiber ส่งด้วยแสง ทน EMI และเหมาะระยะไกล; ยังต้องเลือก transceiver/ชนิด fiber ให้ตรง','ทองแดงใช้สัญญาณไฟฟ้า; ใยแก้วไม่ได้ใช้หัว RJ-45 ตามปกติ'], 'อย่าเลือกจากความเร็วอย่างเดียว ต้องดูระยะ สภาพแวดล้อม และมาตรฐานลิงก์'),
('หัวต่อและคู่สาย',['สาย Ethernet twisted pair ทั่วไปมี 4 คู่ รวม 8 เส้น','หัว 8P8C มักเรียก RJ-45 ในการเรียน LAN','การบิดเกลียวช่วยลดสัญญาณรบกวนและ crosstalk','อย่าคลายเกลียวปลายสายยาวเกินจำเป็น'], 'คู่สายจริงสำคัญกว่าตรวจเพียง pin 1 ถึง pin 8 ตรงกัน'),
('T568A และ T568B',['ลำดับ pin ตามมาตรฐานเมื่อจัดหัวให้ตรงทิศ; ต้องตรวจทิศหัวก่อนนับ','T568A: ขาวเขียว เขียว ขาวส้ม น้ำเงิน ขาวน้ำเงิน ส้ม ขาวน้ำตาล น้ำตาล','T568B: ขาวส้ม ส้ม ขาวเขียว น้ำเงิน ขาวน้ำเงิน เขียว ขาวน้ำตาล น้ำตาล','A กับ B สลับคู่สีเขียวและส้ม; น้ำเงินและน้ำตาลคงเดิม'], 'จำคู่และ pin ด้วย: A pin1 ขาวเขียว; B pin1 ขาวส้ม'),
('Straight-through และ Crossover',['Straight-through ใช้มาตรฐานเดียวกันสองปลาย เช่น B–B','Crossover แบบ 10/100 ใช้ A–B สลับคู่ส่ง/รับ','กฎเดิม PC–switch ใช้ straight; switch–switch ใช้ crossover เมื่อไม่มี Auto MDI-X','Auto MDI-X ช่วยสลับคู่ให้อัตโนมัติในอุปกรณ์ที่รองรับ'], 'กฎแบบเก่าต้องมีเงื่อนไข ไม่มี Auto MDI-X ไม่ใช่ตายตัวกับทุกอุปกรณ์ปัจจุบัน'),
('ระยะและความเร็วที่ชอบถาม',['1000BASE-T ใช้ครบ 4 คู่; Cat5e รองรับ 1 Gb/s ตาม channel ที่ได้มาตรฐาน','Channel copper LAN ทั่วไปสูงสุด 100 m รวม patch cord; permanent link ทั่วไป 90 m','Cat6A รองรับ 10GBASE-T ที่ 100 m ภายใต้เงื่อนไขมาตรฐาน','10G บน Cat6 ขึ้นกับระยะและ crosstalk จึงไม่ควรเหมารวมว่าได้ 100 m'], 'ความเร็วต้องพิจารณาทั้งสาย หัวต่อ ระยะ NIC และ switch'),
('ทดสอบสายและ PoE',['Open: วงจรขาด • Short: ลัดวงจร • Miswire: ต่อผิด pin • Split pair: จับคู่ผิด','Continuity tester อย่างเดียวอาจตรวจ split pair หรือคุณภาพ bandwidth ไม่ครบ','PoE ส่งไฟและข้อมูลบนสาย Ethernet ในระบบที่รองรับ','ตรวจ Link LED → การเข้าหัว → cable test → speed/duplex → IP configuration'], 'ไฟ Link ติดเป็นหลักฐานชั้นล่าง ไม่ใช่ยืนยันว่า routing และแอปถูกต้อง')],'''
สาย UTP ต่างจาก STP อย่างไร|UTP ไม่มีชิลด์ ส่วน STP มีชิลด์|UTP ใช้แสง ส่วน STP ใช้เสียง|UTP มีเพียงเส้นเดียว|STP ไม่ต้องมีตัวนำ|ทั้งสองเป็น twisted pair แต่ต่างเรื่อง shielding
การบิดเกลียวคู่สายช่วยเรื่องใด|ลดการรบกวนและ crosstalk|เพิ่มจำนวน IP|แทน firewall|ทำให้สายไม่ต้องมีหัว|การจัดคู่ช่วยลดผลสัญญาณรบกวน
สาย twisted pair Ethernet ทั่วไปมีตัวนำกี่เส้น|8|2|4|16|มี 4 คู่รวม 8 เส้น
หัวสาย LAN ทองแดงที่มักเรียก RJ-45 มีตำแหน่งสัมผัสกี่ตำแหน่ง|8|4|6|12|หัว 8P8C มี 8 ตำแหน่งและ 8 หน้าสัมผัส
T568B pin 1 เป็นสีใด|ขาวส้ม|ขาวเขียว|น้ำเงิน|น้ำตาล|T568B เริ่มขาวส้ม แล้วส้ม
T568A pin 1 เป็นสีใด|ขาวเขียว|ขาวส้ม|ขาวน้ำเงิน|น้ำตาล|T568A เริ่มขาวเขียว แล้วเขียว
T568A และ T568B สลับคู่สีใด|เขียวกับส้ม|น้ำเงินกับน้ำตาล|น้ำเงินกับเขียว|ส้มกับน้ำตาล|คู่สีเขียวและส้มสลับตำแหน่ง
เข้าหัวแบบ B ทั้งสองปลายเป็นสายใด|Straight-through|Crossover แบบ A-B|Rollover|Fiber|มาตรฐานเดียวกันสองปลายเป็น straight-through
สาย A-B ตามบทเรียน 10/100 เป็นสายชนิดใด|Crossover|Straight-through|Coaxial|Single-mode fiber|A-B สลับคู่ส่งและรับของ 10/100
PC ต่อ switch ตามกฎเก่าโดยไม่มี Auto MDI-X ควรใช้สายใด|Straight-through|Crossover|Rollover|สายโทรศัพท์ 2 เส้น|อุปกรณ์ต่างบทบาทตามกฎเดิมใช้สายตรง
Switch ต่อ switch 10/100 ไม่มี Auto MDI-X ตามกฎเดิมใช้สายใด|Crossover|Straight-through|Console rollover|สาย USB เท่านั้น|ต้องไขว้คู่ส่งรับเมื่ออุปกรณ์ไม่สลับเอง
Auto MDI-X ช่วยอะไร|ปรับการไขว้คู่ส่งรับอัตโนมัติ|แจก IP อัตโนมัติ|ตรวจ DNS|เข้ารหัส Wi-Fi|คุณสมบัตินี้ช่วยลดข้อจำกัดการเลือกสายตรงหรือไขว้
1000BASE-T ใช้สายกี่คู่ในการรับส่งข้อมูล|4 คู่|1 คู่|2 คู่|3 คู่|Gigabit Ethernet แบบนี้ใช้ทั้งสี่คู่
Channel twisted pair LAN ทั่วไปกำหนดระยะรวมเท่าไร|100 m|10 m|500 m|10 km|ค่าทั่วไปคือ permanent link 90 m บวก patch cords รวม 10 m
Permanent link ทองแดงตามแบบติดตั้งทั่วไปยาวไม่เกินเท่าไร|90 m|100 m|150 m|1 km|ส่วนสายถาวรมักจำกัด 90 m เพื่อเผื่อ patch cords
Cat5e ที่ติดตั้งได้มาตรฐานรองรับอะไรโดยทั่วไป|1000BASE-T ที่ channel 100 m|10 Gb/s ที่ 100 km|แสงเท่านั้น|ไม่มี Ethernet|Cat5e รองรับ Gigabit Ethernet ตามข้อกำหนด channel
ตัวเลือกใดเหมาะกับ 10GBASE-T ที่ 100 m ตามมาตรฐานสาย|Cat6A|Cat3|สายโทรศัพท์แบน|Coaxial TV|Cat6A ออกแบบรองรับ 10GBASE-T ที่ 100 m
Fiber ส่งข้อมูลด้วยอะไร|แสง|กระแสลม|เสียงในท่อ|คลื่นบนคู่ทองแดงเสมอ|ใยแก้วใช้สัญญาณแสง
สื่อใดทนต่อ EMI ตามตัวกลางได้ดี|Fiber optic|UTP ทุกกรณีเท่ากัน|สายทองแดงเปลือย|สายโทรศัพท์ยาวไม่จำกัด|ใยแก้วไม่ใช้สัญญาณไฟฟ้าในตัวกลาง
Open circuit ของสายหมายถึงอะไร|ตัวนำขาดหรือไม่ต่อถึงกัน|ตัวนำสองเส้นแตะกัน|DNS เปิดอยู่|สายมี bandwidth สูง|วงจร open ไม่ต่อเนื่อง
Short circuit ของสายหมายถึงอะไร|ตัวนำสัมผัสกันผิดปกติ|ตัวนำขาดเพียงอย่างเดียว|IP ซ้ำเท่านั้น|หัวถูกสีครบ|การลัดวงจรทำให้วงจรที่ควรแยกเชื่อมกัน
Split pair หมายถึงอะไร|นำเส้นจากคนละคู่มาจับคู่สัญญาณ|ใช้ใยแก้วสองเส้น|แยก VLAN|ใช้สายตรงสองเส้น|Pin อาจต่อถึงกันแต่คู่บิดเกลียวผิด ทำให้ crosstalk สูง
PoE ให้ประโยชน์อะไร|ส่งไฟพร้อมข้อมูลให้อุปกรณ์ที่รองรับ|ทำ NAT แทน router|เข้ารหัสทุก frame|ยืด copper ได้ไม่จำกัด|เช่นจ่ายไฟให้ AP หรือ IP phone ผ่าน Ethernet
ไฟ Link ติดยืนยันเรื่องใดได้เหมาะสมที่สุด|มีการเชื่อมต่อระดับลิงก์ตามสถานะอุปกรณ์|DNS ถูกแน่นอน|เว็บไซต์ใช้งานได้แน่นอน|Default route ถูกแน่นอน|ต้องทดสอบ IP และบริการชั้นบนต่อ
เหตุใดไม่ควรคลายเกลียวปลายสายมากเกินจำเป็น|ทำให้คุณสมบัติลด crosstalk แย่ลง|ทำให้ IPv4 เปลี่ยนเป็น IPv6|ลดจำนวน port|ทำให้ DNS หมดอายุ|การคงรูปคู่เกลียวใกล้หัวช่วยรักษาคุณภาพสัญญาณ
''')
section('Cloud Computing',[
('Cloud คืออะไร',['ใช้ทรัพยากรคอมพิวเตอร์ที่จัดสรรได้ตามต้องการผ่านเครือข่าย','NIST: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service','การมี VM อย่างเดียวไม่ได้ทำให้ระบบมีคุณลักษณะ cloud ครบ'], 'จำ 5 คุณลักษณะ: ขอเอง–เข้าผ่านเครือข่าย–ใช้ pool–ยืดหด–วัดการใช้'),
('IaaS / PaaS / SaaS',['IaaS: ใช้ VM, storage, network; ลูกค้ามักดูแล guest OS และแอป','PaaS: ผู้ให้บริการดูแล platform/runtime; ลูกค้าเน้นโค้ดและข้อมูล','SaaS: ใช้แอปสำเร็จรูปผ่านบริการ; ลูกค้ายังต้องจัดการบัญชี สิทธิ์ และข้อมูลตามข้อตกลง'], 'ถามว่าใครดูแลอะไร ให้ดูขอบเขตบริการ ไม่ใช่ชื่อผลิตภัณฑ์อย่างเดียว'),
('Deployment Models',['Public: เปิดให้ใช้งานโดยสาธารณะตามบริการ','Private: จัดไว้ให้ใช้งานเฉพาะองค์กรหนึ่ง','Community: ใช้ร่วมโดยองค์กรที่มีข้อกำหนดร่วมกัน','Hybrid: เชื่อม cloud ตั้งแต่สองโครงสร้างที่แยกกันและรองรับการเคลื่อนย้ายข้อมูล/แอป'], 'Public/private เป็นรูปแบบการใช้งาน ไม่ใช่คำตัดสินว่าปลอดภัยหรือไม่ปลอดภัย'),
('Elasticity กับ Scalability',['Scalability: ความสามารถในการรองรับงานเพิ่มด้วยทรัพยากรที่มากขึ้น','Elasticity: ปรับเพิ่มและลดทรัพยากรตามความต้องการ','Scale up: เพิ่มพลังเครื่องเดิม • Scale out: เพิ่มจำนวนเครื่อง','Load balancer กระจายคำขอ; auto scaling ปรับจำนวน/ขนาดตามกฎ'], 'เพิ่มเครื่องโดยไม่ลดเมื่อโหลดหาย ยังไม่แสดงการยืดหดครบ'),
('ความพร้อมใช้และข้อมูล',['Availability ต้องดู SLA และสถาปัตยกรรม ไม่ใช่เชื่อว่า cloud ไม่เคยล่ม','Backup เก็บสำเนาสำหรับกู้คืน; replication ช่วยทำสำเนาแต่ไม่แทน backup ทุกกรณี','RPO: ยอมเสียข้อมูลย้อนหลังเท่าใด • RTO: ต้องกู้บริการภายในเท่าใด','Object storage เก็บเป็น object; block storage ให้ block สำหรับ volume'], 'Replication อาจทำสำเนาความผิดพลาดหรือการลบตามไปด้วย'),
('ต้นทุนและความปลอดภัย',['Measured service วัดการใช้ทรัพยากร; ค่าใช้จ่ายขึ้นกับ pricing และการใช้งานจริง','ระวัง VM เปิดทิ้ง storage snapshot และค่าโอนข้อมูลออก','Shared responsibility: ผู้ให้บริการกับลูกค้ามีหน้าที่ต่างกันตามบริการ','Least privilege, MFA, encryption, backup และการตรวจสิทธิ์ข้อมูลยังจำเป็น'], 'Cloud ไม่ได้รับประกันว่าถูกกว่าเสมอ ต้องวัดและคุมการใช้')],'''
ข้อใดเป็นคุณลักษณะ cloud ตาม NIST|On-demand self-service|ต้องติดตั้งเองทุกเครื่อง|ห้ามใช้เครือข่าย|ความจุตายตัวเสมอ|ผู้ใช้จัดสรรทรัพยากรได้ตามต้องการโดยไม่ต้องให้เจ้าหน้าที่ทำทุกครั้ง
Broad network access หมายถึงอะไร|เข้าถึงบริการผ่านเครือข่ายด้วยกลไกมาตรฐาน|ใช้ได้ในห้องเดียวเท่านั้น|ต้องมีสาย crossover ทุกเครื่อง|ห้ามใช้มือถือ|บริการเข้าถึงได้จาก client หลายประเภทตามการรองรับ
Resource pooling หมายถึงอะไร|รวมทรัพยากรให้บริการผู้ใช้หลายรายตามการจัดสรร|ทุกคนต้องใช้รหัสผ่านเดียว|ต้องเก็บข้อมูลในไฟล์เดียว|ไม่มีการแยกผู้เช่า|ทรัพยากรอยู่ใน pool และจัดให้ผู้ใช้ตามความต้องการ
Rapid elasticity เน้นอะไร|เพิ่มและลดทรัพยากรตามความต้องการได้รวดเร็ว|เพิ่ม IP แบบสุ่ม|ห้ามลดจำนวนเครื่อง|ใช้ฮาร์ดดิสก์ใหญ่ที่สุดเสมอ|Elasticity สอดคล้องกับโหลดที่ขึ้นลง
Measured service หมายถึงอะไร|วัดและติดตามปริมาณการใช้บริการ|บริการต้องฟรีทุกแบบ|คิดเงินเท่ากันทุกงาน|วัดความยาวสายเท่านั้น|การวัดช่วยติดตามรายงานและควบคุมการใช้ทรัพยากร
โมเดลใดให้ลูกค้าดูแล guest OS ของ VM โดยทั่วไป|IaaS|SaaS|DNS|HTTP|IaaS ให้โครงสร้างพื้นฐาน ส่วน guest OS อยู่ในความรับผิดชอบลูกค้าตามบริการ
โมเดลใดให้ deploy โค้ดโดยไม่ดูแล OS พื้นฐานเป็นหลัก|PaaS|IaaS แบบ VM ดิบ|Ethernet|STP|PaaS จัดการ platform/runtime ให้ตามขอบเขตบริการ
การใช้แอปสำเร็จรูปออนไลน์จัดเป็นโมเดลใดโดยทั่วไป|SaaS|IaaS|Physical layer|Private IP|SaaS ให้ซอฟต์แวร์ในรูปบริการ
Cloud ที่จัดไว้ใช้เฉพาะองค์กรหนึ่งคืออะไร|Private cloud|Public cloud|Community cloud เสมอ|Open Wi-Fi|Private cloud ใช้เฉพาะองค์กร แม้ผู้ดูแลหรือสถานที่อาจต่างกัน
Cloud ที่เปิดให้สาธารณะสมัครใช้ตามบริการคืออะไร|Public cloud|Private cloud|VLAN|Loopback|Public cloud เปิดให้ใช้งานทั่วไปตามเงื่อนไขผู้ให้บริการ
องค์กรที่มีข้อกำหนดร่วมกันใช้ cloud ร่วมกันเป็นโมเดลใด|Community cloud|Public DNS|Transport cloud|Full mesh เสมอ|Community cloud รองรับกลุ่มองค์กรที่มีข้อกำหนดร่วม
การเชื่อม private และ public cloud เพื่อทำงานร่วมกันตรงกับอะไร|Hybrid cloud|SaaS เท่านั้น|Single host|Rollover|Hybrid ประกอบ cloud แยกกันที่เชื่อมด้วยเทคโนโลยีรองรับการใช้ร่วม
เพิ่ม RAM ให้เครื่องเดิมเป็นการ scale แบบใด|Scale up|Scale out|Scale in|Broadcast|Vertical scaling เพิ่มความสามารถเครื่องเดิม
เพิ่มจำนวน VM หลายเครื่องเป็นการ scale แบบใด|Scale out|Scale up|Scale down|Subnetting|Horizontal scaling เพิ่มจำนวน instance
Load balancer ทำหน้าที่ใด|กระจายคำขอไปหลาย backend|รับรองข้อมูลไม่มีวันหาย|แทน DNS ทุกกรณี|ทำสาย LAN ให้ยาวไม่จำกัด|ช่วยกระจายโหลดและอาจตรวจสุขภาพ backend
Auto scaling ใช้ทำอะไร|ปรับทรัพยากรอัตโนมัติตามกฎหรือโหลด|เข้ารหัสทุกไฟล์อัตโนมัติเสมอ|แก้ source code ให้ถูกทุกครั้ง|ป้องกันค่าใช้จ่ายได้ทั้งหมด|ต้องกำหนดนโยบาย ขอบเขต และเฝ้าดูต้นทุน
มี VM ในห้อง server เพียงอย่างเดียวพิสูจน์ว่าเป็น cloud ครบหรือไม่|ยังไม่พอ ต้องดูคุณลักษณะบริการ|พอเสมอ|เป็น SaaS เสมอ|เป็น public เสมอ|Virtualization เป็นเทคโนโลยีหนึ่ง แต่ไม่เท่ากับคุณลักษณะ cloud ครบ
Shared responsibility หมายถึงอะไร|ผู้ให้บริการและลูกค้ารับผิดชอบต่างส่วนตามบริการ|ผู้ให้บริการดูแลทุกอย่างเสมอ|ลูกค้าไม่ต้องดูแลบัญชี|ไม่ต้องมี backup|ขอบเขตต่างกันตาม IaaS PaaS SaaS และข้อตกลง
Least privilege คืออะไร|ให้สิทธิ์เท่าที่จำเป็นต่อหน้าที่|ให้ admin ทุกคน|เปิด storage สาธารณะทั้งหมด|ใช้บัญชีเดียวทั้งองค์กร|ลดสิทธิ์ส่วนเกินเพื่อลดผลกระทบและความเสี่ยง
RPO ใช้บอกอะไร|ปริมาณเวลาข้อมูลย้อนหลังที่ยอมสูญเสียได้|เวลากู้ระบบทั้งหมดเท่านั้น|ความเร็ว CPU|ความยาวสาย|RPO เป็นเป้าหมายการยอมเสียข้อมูลตามช่วงเวลา
RTO ใช้บอกอะไร|ระยะเวลาที่ตั้งเป้ากู้บริการกลับมา|จำนวน byte ใน frame|อายุ DNS cache|จำนวน VLAN|RTO เป็นเป้าหมายเวลากู้ระบบหลังหยุดชะงัก
เหตุใด replication ไม่แทน backup ทุกกรณี|การลบหรือข้อมูลเสียอาจถูกทำสำเนาตาม|Replication ไม่คัดลอกข้อมูล|Backup ใช้เครือข่ายไม่ได้|ทั้งคู่เป็น DNS|ต้องมีสำเนาที่กู้ย้อนหลังได้ตามนโยบายและทดสอบการกู้
Object storage จัดเก็บข้อมูลแบบใด|Object พร้อม identifier และ metadata|เฉพาะ sector ให้ OS เสมอ|เฉพาะค่า MAC|เฉพาะ TCP connection|Object storage เข้าถึงผ่าน API หรือกลไกบริการที่กำหนด
ข้อใดทำให้ค่า cloud เพิ่มโดยไม่จำเป็น|เปิดทรัพยากรทิ้งแม้ไม่มีงาน|กำหนด budget alert|ลบทรัพยากรที่ไม่ใช้ตามนโยบาย|เลือกขนาดให้พอดีโหลด|ทรัพยากรที่คิดเงินอาจมีค่าใช้จ่ายแม้ไม่มีผู้ใช้แอป
SLA ด้าน availability หมายถึงอะไร|ข้อตกลงระดับบริการตามนิยามและเงื่อนไข|รับรองไม่มี downtime ทุกกรณี|สำเนา backup ทุกนาทีเสมอ|รหัสผ่านของ server|ต้องอ่านนิยาม วิธีวัด ข้อยกเว้น และการชดเชยในข้อตกลง
''')
section('Wireless',[
('Wi-Fi และบทบาทอุปกรณ์',['IEEE 802.11 คือ WLAN; IEEE 802.3 คือ Ethernet','AP เชื่อม client ไร้สายเข้าลิงก์เครือข่าย; ไม่จำเป็นต้องทำ routing/DHCP','Wireless router บ้านมักรวม AP + switch + router + NAT + DHCP','SSID คือชื่อเครือข่าย; BSSID ระบุ BSS โดยทั่วไปสัมพันธ์กับ MAC ของ AP radio'], 'อย่าเหมาว่า AP ทุกตัวเป็น default gateway'),
('โหมดและการเข้าถึงสื่อ',['Infrastructure: client ติดต่อผ่าน AP • Ad hoc: สื่อสารโดยไม่ใช้ AP ตามรูปแบบนั้น','CSMA/CA ฟังช่องสัญญาณ สุ่ม backoff และใช้ ACK ตามชนิด frame','Hidden node: client ได้ยิน AP แต่ไม่ได้ยินกันเอง','RTS/CTS ช่วยลดผล hidden node ได้บางกรณี แต่มี overhead'], 'Wi-Fi แบ่งเวลาใช้สื่อ ความเร็วโฆษณาไม่ใช่ throughput ที่รับประกัน'),
('ย่านและ Channel',['2.4 GHz มักไปได้ไกล/ทะลุสิ่งกีดขวางได้ดีกว่าในเงื่อนไขเทียบกัน แต่แออัด','5 GHz มีช่องให้จัดสรรมากกว่าในหลายบริบท; ระยะขึ้นกับกำลังส่ง วัสดุ และสภาพแวดล้อม','2.4 GHz แบบ 20 MHz นิยมวางช่อง 1, 6, 11 เพื่อลดการทับซ้อน','Channel ที่อนุญาตและกำลังส่งขึ้นกับประเทศ/ข้อกำหนดอุปกรณ์'], 'เพิ่ม channel width อาจเพิ่มอัตราส่งสูงสุด แต่กินสเปกตรัมและเพิ่มโอกาสรบกวน'),
('Security ที่ต้องแยก',['WEP และ WPA/TKIP เป็นแบบเก่าที่ควรหลีกเลี่ยง; WPA2-AES/CCMP หรือ WPA3 ตามการรองรับ','Personal ใช้รหัสร่วม; Enterprise มักใช้ 802.1X/EAP กับระบบยืนยันตัวตน','ซ่อน SSID หรือ MAC filtering ไม่ใช่การเข้ารหัสและไม่แทน security ที่เหมาะสม','เปลี่ยนรหัสผู้ดูแล และอย่าสับสน admin password กับรหัสเข้า Wi-Fi'], 'การเชื่อม SSID สำเร็จยังไม่รับประกันว่าได้ IP และออก Internet ได้'),
('Signal และ Throughput',['RSSI แบบ dBm: −50 dBm แรงกว่า −80 dBm','SNR = signal เทียบ noise; SNR สูงมักช่วยรองรับ modulation ที่สูงขึ้น','ระยะ กำแพง การรบกวน จำนวน client และ airtime กระทบ throughput','Roaming คือย้ายการเชื่อมต่อระหว่าง AP; ต้องมีการออกแบบ coverage/บริการรองรับ'], 'สัญญาณแรงอาจยังช้า หากช่องแออัดหรือ backhaul เป็นคอขวด'),
('ลำดับตรวจ Wi-Fi',['ตรวจ radio/NIC → SSID → security/key → association','ตรวจ DHCP/IP/mask/gateway/DNS → ping gateway → ทดสอบบริการ','IPv4 169.254.x.x มักเป็น link-local เมื่อไม่ได้ lease ในระบบที่รองรับ','ตรวจฝั่ง WAN และ NAT ของ wireless router เมื่อ LAN ได้แต่ Internet ไม่ได้'], 'แยกปัญหาการเชื่อมไร้สาย ออกจากปัญหา IP/DNS/WAN')],'''
Wi-Fi WLAN ใช้มาตรฐานตระกูลใด|IEEE 802.11|IEEE 802.3|IEEE 802.1Q เท่านั้น|RS-232|802.11 เป็นตระกูลมาตรฐาน WLAN
SSID คืออะไร|ชื่อเครือข่ายไร้สาย|รหัสผ่าน admin เสมอ|IP ของ DNS|Subnet mask|SSID ใช้ระบุชื่อ WLAN ที่ client เลือกเชื่อม
AP มีหน้าที่หลักใด|เชื่อม client ไร้สายเข้าระบบลิงก์|เป็น router เสมอ|เป็น DNS root เสมอ|จ่าย public IP เสมอ|AP ไม่จำเป็นต้องมี NAT routing หรือ DHCP
Wireless router สำหรับบ้านมักรวมอะไร|AP switch router NAT และ DHCP|เฉพาะ repeater อย่างเดียว|เฉพาะ mail server|เฉพาะสาย console|กล่องเดียวรวมหลายหน้าที่ แต่ยังต้องแยกแนวคิด
Infrastructure mode ใช้อะไรเป็นศูนย์กลางการเข้าถึง|Access point|DNS record|สาย console|FTP control|Client เชื่อมผ่าน AP
Ad hoc mode ตามแนวคิด WLAN คืออะไร|อุปกรณ์สื่อสารกันโดยไม่ผ่าน AP ในโหมดนั้น|ต้องผ่าน public cloud เสมอ|ใช้สาย LAN เท่านั้น|ใช้แต่ router ชั้น 3|ต่างจาก infrastructure ที่มี AP
CSMA/CA มุ่งทำอะไร|ลดโอกาสชนก่อนส่ง|ตรวจ collision ระหว่างส่งเหมือนสายร่วมได้เสมอ|แปลง DNS|จัดสรร public IP|ใช้ฟังสื่อและ backoff รวมกลไกที่เกี่ยวข้อง
Hidden node เกิดจากอะไร|Client ได้ยิน AP แต่ไม่ได้ยินกันเอง|ปิดชื่อ SSID เท่านั้น|DNS ไม่มี AAAA|สาย fiber สั้นเกินไป|Client อาจส่งชนกันที่ AP แม้ฟังแล้วคิดว่าช่องว่าง
RTS/CTS ช่วยลดปัญหาใดบางกรณี|Hidden node|IP ซ้ำทุกชนิด|DNS poisoning ทุกกรณี|สาย LAN ขาด|การจองสื่อช่วยให้สถานีอื่นทราบช่วงใช้งาน แต่มี overhead
ชุด channel 2.4 GHz ที่นิยมสำหรับ 20 MHz คืออะไร|1 6 11|1 2 3|3 4 5|8 9 10|ชุด 1 6 11 ลดการทับซ้อนตามการจัดช่องทั่วไป
ข้อใดอธิบาย 2.4 GHz เทียบ 5 GHz ได้เหมาะสม|มักครอบคลุมและผ่านสิ่งกีดขวางได้ดีกว่าเมื่อเงื่อนไขเทียบกัน|เร็วกว่าเสมอทุกสถานการณ์|ไม่มีการรบกวน|ใช้ได้ช่องเดียวทั่วโลก|การแพร่คลื่นยังขึ้นกับกำลังส่ง เสาอากาศและสิ่งแวดล้อม
การเพิ่ม channel width มีผลแลกเปลี่ยนใด|อาจเพิ่มอัตราส่งแต่ใช้สเปกตรัมมากขึ้น|ลดการใช้สเปกตรัมเสมอ|ทำให้ไม่มี noise|รับประกันระยะเพิ่มสองเท่า|ช่องกว้างใช้ความถี่มากขึ้นและอาจรับการรบกวนมากขึ้น
มาตรฐานความปลอดภัยใดเก่าและไม่ควรเลือก|WEP|WPA3|WPA2-AES|802.1X ร่วม EAP ที่เหมาะสม|WEP มีจุดอ่อนทางการเข้ารหัสที่ทราบกัน
WPA2 แบบ AES ใช้กลไกข้อมูลใดโดยทั่วไป|CCMP|WEP เท่านั้น|Telnet|FTP|AES-CCMP เป็นวิธีที่ใช้กับ WPA2 ตามบริบทนี้
Enterprise Wi-Fi มักใช้กลไกใด|802.1X/EAP|HTTP 404|ARP เพียงอย่างเดียว|NAT เพียงอย่างเดียว|Enterprise ใช้การยืนยันตัวตนรายผู้ใช้หรืออุปกรณ์ตามระบบ
การซ่อน SSID เพียงอย่างเดียวปลอดภัยเพียงพอหรือไม่|ไม่พอ และไม่ใช่การเข้ารหัส|พอและแทน WPA ได้|ป้องกันดักฟังได้ทั้งหมด|ทำให้ไม่ต้องมีรหัส admin|ชื่อเครือข่ายยังอาจค้นพบได้จาก traffic
MAC filtering มีข้อจำกัดสำคัญใด|MAC อาจถูกปลอมและไม่เข้ารหัสข้อมูล|เพิ่มความลับเทียบเท่า TLS เสมอ|ทำให้ไม่ต้องใช้ WPA|ป้องกันการโจมตีทุกแบบ|ใช้เป็นส่วนประกอบได้แต่ไม่แทนการยืนยันตัวตนและเข้ารหัส
ค่า RSSI ใดแรงกว่าเมื่อวัดแบบเดียวกัน|-50 dBm|-80 dBm|-90 dBm|-100 dBm|ค่าที่ติดลบน้อยกว่าหมายถึงกำลังรับสูงกว่า
SNR สูงโดยทั่วไปสื่อถึงอะไร|สัญญาณเด่นกว่า noise มากขึ้น|Noise สูงกว่าสัญญาณเสมอ|DNS ตอบเร็วแน่นอน|ไม่มี client อื่น|SNR คืออัตราส่วนสัญญาณต่อสัญญาณรบกวน
PHY rate ของ Wi-Fi เท่ากับ throughput แอปเสมอหรือไม่|ไม่เท่า เพราะมี overhead และการแบ่ง airtime|เท่าเสมอ|มากกว่าได้ไม่จำกัดเสมอ|ไม่เกี่ยวกับสื่อเลย|ACK การรอส่ง การส่งซ้ำ และ protocol ลดอัตราข้อมูลแอป
Roaming หมายถึงอะไร|ย้ายการเชื่อมต่อระหว่าง AP|เปลี่ยนสายเป็น fiber|แปลง HTTP เป็น DNS|เพิ่ม VLAN ทุก packet|การเคลื่อนที่และการออกแบบเครือข่ายกำหนดความต่อเนื่องของบริการ
เชื่อม SSID ได้แต่มี 169.254.x.x ควรตรวจอะไร|DHCP และการตั้งค่า IP|ขนาดหน้าจอ|ลำดับ OSI ชั้น 7 อย่างเดียว|ชื่อไฟล์รูป|ที่อยู่ link-local มักชี้ว่าไม่ได้ DHCP lease ในระบบที่รองรับ
พิมพ์รหัส Wi-Fi ถูกแล้วออก Internet ไม่ได้ ข้อใดถูกต้อง|ยังต้องตรวจ IP gateway DNS และ WAN|Internet ต้องใช้ได้แน่นอน|AP เสียแน่นอน|ต้องเปลี่ยน MAC ทันที|การยืนยันตัวตนสำเร็จไม่ยืนยันบริการชั้นบน
BSSID โดยทั่วไปใช้ระบุอะไร|BSS โดยสัมพันธ์กับ MAC ของ AP radio|รหัสผ่าน cloud|Subnet mask|HTTP method|SSID เป็นชื่อ ส่วน BSSID ระบุชุดบริการพื้นฐาน
ข้อใดช่วยลดปัญหา Wi-Fi ช้าในห้องที่ AP หลายตัวใช้ช่องทับซ้อน|วาง channel และ airtime ใหม่ตามการสำรวจ|เพิ่มกำลังส่งทุกตัวสูงสุดเสมอ|ซ่อน SSID อย่างเดียว|เปลี่ยน DNS อย่างเดียวเสมอ|ต้องจัดช่องและ coverage จากการสำรวจ ไม่เพิ่มกำลังส่งโดยไม่มีข้อมูล
''')
section('Cisco และ Packet Tracer',[
('โหมดคำสั่ง IOS',['Router> คือ user EXEC; enable → Router# privileged EXEC','configure terminal → Router(config)# global configuration','interface g0/0 → Router(config-if)#; ชื่อ interface ขึ้นกับรุ่น','exit กลับหนึ่งระดับ; end หรือ Ctrl+Z กลับ privileged EXEC'], 'คำสั่งต้องใช้ในโหมดที่ถูกต้อง ไม่ใช่ใส่ทุกคำสั่งที่ prompt เดียว'),
('ตั้งค่า Interface: ตัวอย่าง',['enable → configure terminal → interface g0/0','ip address 192.168.10.1 255.255.255.0','no shutdown → end','show ip interface brief ตรวจ IP และสถานะ interface'], 'นี่เป็นตัวอย่าง IOS; เลือก interface และ IP ให้ตรง topology จริง'),
('อ่านคำสั่งตรวจสอบ',['show ip interface brief: สรุป IP และ up/down','show ip route: routing table; C=connected, L=local, S=static, O=OSPF, R=RIP ตาม IOS','show running-config: config ปัจจุบัน • show startup-config: config สำหรับเริ่มระบบ','show mac address-table: MAC table ของ switch'], 'administratively down มักต้องตรวจ shutdown/no shutdown'),
('Static Route และการบันทึก',['ตัวอย่าง: ip route 192.168.20.0 255.255.255.0 10.0.0.2','Default route: ip route 0.0.0.0 0.0.0.0 10.0.0.2','Next-hop ต้องเข้าถึงได้ และปลายทางต้องมี route กลับด้วย','copy running-config startup-config เก็บ config เพื่อใช้หลัง reboot'], 'ping ไปได้ต้องมีเส้นทางตอบกลับและไม่มีนโยบายที่บล็อก'),
('การทดสอบใน Packet Tracer',['Realtime ดูการทำงานทั่วไป; Simulation ดูเหตุการณ์ protocol ทีละขั้น','เริ่มจาก ping gateway แล้วจึง ping ข้าม subnet และทดสอบบริการ','ตรวจ link, IP/mask, gateway, route ไป-กลับ, ACL และบริการตามลำดับ','Check Results เทียบ rubric ของกิจกรรม แต่ไม่แทนการเข้าใจเหตุการณ์'], 'ไม่ใช่เฉลยไฟล์ PKA ที่ยังไม่ได้ตรวจ topology จริง'),
('อ่านผังแบบลงมือทำ',['เขียนตาราง Device / Interface / IP / Mask / Gateway ก่อนตั้งค่า','แยกแต่ละ LAN/VLAN และวงเชื่อม router เป็นคนละ subnet','ตรวจว่าสายต่อ interface ถูกและ interface เปิดใช้งาน','เมื่อทดสอบล้มเหลว ใช้หลักฐานชี้ว่าหยุดที่ hop หรือชั้นใด'], 'ลองวาด 2 LAN ผ่าน 2 router แล้วใส่ static route ทั้งขาไปและขากลับ')],'''
Prompt Router> แสดงโหมดใดโดยทั่วไป|User EXEC|Global configuration|Interface configuration|ROMMON เสมอ|เครื่องหมาย > เป็น user EXEC ใน IOS ตามปกติ
คำสั่งใดเข้า privileged EXEC จาก user EXEC|enable|configure terminal|no shutdown|ip route|enable เปลี่ยนจาก > เป็น # เมื่อผ่านเงื่อนไขการยืนยันตัวตน
Prompt Router# โดยทั่วไปเป็นโหมดใด|Privileged EXEC|Interface configuration|Line configuration|DHCP pool configuration|Privileged EXEC ใช้คำสั่งตรวจสอบและเข้าตั้งค่าได้
คำสั่งใดเข้า global configuration จาก privileged EXEC|configure terminal|show ip route|ping|copy startup-config running-config|configure terminal เข้าสู่โหมด (config)#
คำสั่ง interface g0/0 ใช้ทำอะไร|เข้าโหมดตั้งค่า interface นั้น|เปิด DNS|บันทึก config|ลบ route ทุกเส้น|ชื่อ interface จริงขึ้นกับรุ่นอุปกรณ์
คำสั่ง ip address 192.168.1.1 255.255.255.0 ใน interface mode ทำอะไร|กำหนด IPv4 และ mask|กำหนด DNS A record|สร้าง VLAN tag ทุกพอร์ต|กำหนด SSID|ตั้งที่อยู่บน interface ที่กำลังเลือก
คำสั่งใดเปิด interface ที่ถูก shutdown|no shutdown|shutdown|disable dns|erase startup-config|no shutdown ยกเลิกการปิด interface ทางการตั้งค่า
สถานะ administratively down มักหมายถึงอะไร|Interface ถูกปิดด้วยการตั้งค่า|DNS server ล่มแน่นอน|สายขาดแน่นอน|OSPF เลือกเส้นผิดเสมอ|ตรวจ shutdown และการเปิดใช้งาน interface
คำสั่งใดสรุป IP และสถานะ interface|show ip interface brief|show clock|show users|show version เท่านั้น|แสดงรายการ interface IP และ status/protocol
คำสั่งใดดู routing table|show ip route|show mac address-table|show vlan brief|show clock|routing table แสดง prefix next hop และแหล่ง route
รหัส C ใน show ip route บน IOS โดยทั่วไปหมายถึงอะไร|Connected|Cloud|CRC failed|Console password|C เป็นเครือข่ายที่เชื่อมตรงและติดตั้งตามสถานะ interface
รหัส O ใน show ip route โดยทั่วไปมาจากอะไร|OSPF|HTTP|DHCP|ARP|O แสดง route จาก OSPF
คำสั่งใดดูการตั้งค่าที่ใช้อยู่ปัจจุบัน|show running-config|show startup-config|show clock|show arp เท่านั้น|running-config คือ configuration ที่กำลังใช้งาน
คำสั่งใดดู configuration ที่ใช้ตอนเริ่มระบบ|show startup-config|show running-config|show interfaces เท่านั้น|show mac address-table|startup-config เป็นข้อมูลที่เก็บไว้สำหรับเริ่มระบบ
คำสั่งใดบันทึก config ปัจจุบันเพื่อใช้หลัง reboot|copy running-config startup-config|copy startup-config running-config|show running-config|reload โดยไม่บันทึก|คัดลอก configuration ปัจจุบันไปยัง startup configuration
คำสั่งใดตั้ง default route ผ่าน 10.0.0.2|ip route 0.0.0.0 0.0.0.0 10.0.0.2|ip route 255.255.255.255 255.255.255.255 10.0.0.2|ip address 0.0.0.0 10.0.0.2|show ip route 10.0.0.2|ปลายทางและ mask เป็นศูนย์ระบุ default route
ip route 192.168.20.0 255.255.255.0 10.0.0.2 ระบุ next hop ใด|10.0.0.2|192.168.20.0|255.255.255.0|0.0.0.0|อาร์กิวเมนต์สุดท้ายในตัวอย่างนี้คือ next-hop IP
คำสั่ง exit ในโหมดตั้งค่าทั่วไปทำอะไร|กลับหนึ่งระดับ|บันทึก config เสมอ|ลบ interface|reboot ทันที|exit ออกจากโหมดย่อยกลับสู่โหมดก่อนหน้า
คำสั่ง end จาก configuration mode ทำอะไร|กลับ privileged EXEC|ปิด router|ลบ startup-config|เข้า interface แรก|end กลับ prompt # โดยไม่ต้อง exit ทีละระดับ
คำสั่งใดดู MAC table ของ switch IOS ตามปกติ|show mac address-table|show ip route|show clock|show startup-config เท่านั้น|แสดง MAC ที่เรียนรู้และพอร์ตใน VLAN ที่เกี่ยวข้อง
Ping ข้าม router ต้องมีเงื่อนไขใดนอกเหนือจากเส้นทางขาไป|มีเส้นทางขากลับและไม่มีนโยบายบล็อก|ต้องใช้ VLAN 1 ทุกวง|ต้องเป็นสาย crossover ทุกเส้น|ต้องใช้ public IP ทุกเครื่อง|ICMP echo reply ต้องกลับถึงต้นทางด้วย
Packet Tracer Simulation mode ช่วยเรื่องใด|ดูเหตุการณ์ protocol และ packet ทีละขั้น|รับรอง network จริงเหมือนทุกประการ|แก้ config ให้ถูกอัตโนมัติทุกครั้ง|ยกเลิก subnet mask|ใช้สังเกตการแลกเปลี่ยน protocol ในแบบจำลอง
PC ping gateway ไม่ผ่าน ควรตรวจอะไรก่อนเหมาะสมที่สุด|Link IP mask gateway และ interface ฝั่ง LAN|เปลี่ยน cloud provider|ลบทุก route ทันที|ตั้ง HTTP cookie|เริ่มตรวจชั้นใกล้ตัวก่อนวิเคราะห์เส้นทางไกล
IP interface เป็น up แต่ line protocol down ควรทำอย่างไร|ตรวจลิงก์และการตั้งค่าชั้นล่างตามชนิด interface|สรุปว่า DNS ผิดทันที|สรุปว่าเว็บถูกบล็อกทันที|เปลี่ยน SSID เสมอ|สถานะ physical กับ line protocol ช่วยแยกปัญหา แต่ต้องดูชนิดลิงก์
เหตุใดควรทำตาราง IP ก่อนตั้ง topology|ลด IP ซ้ำและช่วยตรวจ subnet กับ gateway|เพื่อไม่ต้องทดสอบ|เพื่อไม่ต้องใช้ mask|ทำให้ router เลือก OSPF เอง|แผน addressing ช่วยให้ตั้งค่าและไล่ปัญหาอย่างเป็นระบบ
''')
assert sum(len(s['questions']) for s in sections)==200
answer_positions=list(range(4))*50
random.Random(3512026).shuffle(answer_positions)
for i,s in enumerate(sections):
    for j,q in enumerate(s['questions']):
        q['id']=i*25+j+1
        # Balance answer positions exactly, without changing the authored correct answer.
        correct=q['options'][0]; k=answer_positions[i*25+j]
        q['options']=q['options'][1:k+1]+[correct]+q['options'][k+1:]
        q['answer']=k
        assert len(set(q['options']))==4
sources=[
 ['เอกสารไทยในโฟลเดอร์: OSI, TCP/IP, Application, Link, Subnet และ Packet Tracer','../index.html'],
 ['NIST SP 800-145: The NIST Definition of Cloud Computing','https://csrc.nist.gov/pubs/sp/800/145/final'],
 ['Cisco: Understand Administrative Distance','https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html'],
 ['Cisco: LAN cabling and connector guide','https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6000-series-switches/21268-132.html'],
 ['Cisco: 10GBASE-T cabling guidance','https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/at-a-glance-c45-743937.html'],
 ['Cisco: Wireless LAN Configuration Guide — WPA2/AES-CCMP','https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/wlan/configuration/15-mt/wl-15-mt-book.pdf'],
 ['Cisco: Configure Route Selection for Routers','https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8651-21.html']]
(OUT/'exam-data.json').write_text(json.dumps(dict(sections=sections,sources=sources),ensure_ascii=False,indent=2))
DATA=json.dumps(dict(sections=sections,sources=sources),ensure_ascii=False).replace('</','<\\/')
page=r'''<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>351 • สไลด์อ่านสอบและข้อกา 200 ข้อ</title>
<style>
:root{--bg:#eef2f6;--ink:#15243b;--muted:#52617a;--brand:#1746a2;--line:#d5dfeb;--green:#126145;--red:#a12332}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,'Noto Sans Thai',sans-serif;line-height:1.75}button,select,input{font:inherit}button,a,select,input{touch-action:manipulation}button{cursor:pointer;border:1px solid var(--line);border-radius:10px;background:white;color:var(--ink);padding:9px 15px}button:hover{border-color:var(--brand)}button:focus-visible,a:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid #e89c27;outline-offset:3px}button.primary{background:var(--brand);color:white;border-color:var(--brand)}button[disabled]{opacity:.45;cursor:default}.top{background:#10213f;color:white;padding:24px max(20px,calc((100vw - 1150px)/2))}.eyebrow{color:#82dcca;letter-spacing:2px;font-size:13px}h1{font-size:clamp(25px,4vw,40px);line-height:1.4;margin:8px 0}h2{line-height:1.5}h3{margin:0 0 10px}.top p{max-width:880px;color:#d4dfef;margin-bottom:0}.nav{display:flex;gap:8px;flex-wrap:wrap;padding:12px 20px;position:sticky;top:0;background:#eef2f6f5;backdrop-filter:blur(10px);z-index:10;border-bottom:1px solid var(--line)}.nav button[aria-selected=true]{background:#1746a2;color:white}.wrap{max-width:1190px;margin:auto;padding:22px 20px 70px}.panel[hidden]{display:none}.box,.question,.chaptercard{background:white;border:1px solid var(--line);border-radius:15px;padding:23px;margin-bottom:18px}.note{border-left:4px solid #d59125;background:#fff6e6;padding:14px 18px;border-radius:6px;color:#634c22}.muted{color:var(--muted)}.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:15px 0}select,input[type=search]{padding:9px;border:1px solid var(--line);border-radius:9px;background:white;max-width:100%}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:15px}.cardlink{text-align:left;width:100%;height:100%;padding:20px;background:white;border-radius:13px}.cardlink strong{display:block;font-size:18px}.tag{font-size:12px;letter-spacing:.3px;color:var(--brand);font-weight:bold}.panel:fullscreen{background:var(--bg);overflow:auto;padding:20px}.slide{min-height:510px;background:white;border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 12px 35px #1734550d}.slidehead{padding:16px 30px;background:#10213f;color:#88e2cf;font-size:14px}.slidebody{padding:24px 38px}.slide h2{font-size:clamp(25px,3vw,34px);margin:0 0 20px}.slide li{font-size:clamp(18px,2vw,23px);margin:12px 0}.slide ul{padding-left:27px}.takeaway{background:#e8f5f0;padding:13px 18px;border-radius:10px;color:#174f3c;font-size:18px}.progress{height:5px;background:#d6e1f0}.progress span{display:block;background:#13a38c;height:100%}.diagram{display:flex;gap:5px;flex-wrap:wrap;margin:16px 0}.diagram span{border:1px solid #b4c8df;background:#edf4fc;border-radius:8px;padding:8px 13px}.opts{display:grid;gap:8px;margin-top:12px}.opt{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:9px;padding:12px;cursor:pointer}.opt:hover{background:#f1f6fc}.opt input{margin-top:7px;accent-color:var(--brand)}.opt.correct{background:#e6f5ec;border-color:#308b5d}.opt.wrong{background:#ffeded;border-color:#c85c64}.explain{padding:15px;background:#f2f6fa;border-radius:8px;margin-top:13px}.explain[hidden]{display:none}.qtitle{font-size:18px;margin:5px 0}.score{padding:20px;background:#e4edf9;border:1px solid #b5c9e8;border-radius:12px;margin:15px 0}.score:empty{display:none}.stat{font-weight:bold;font-size:22px}.allslide{break-inside:avoid}.allslide li{margin:9px 0}.answers-print{display:none}table{border-collapse:collapse;width:100%;font-size:15px}td,th{border:1px solid var(--line);padding:9px;text-align:left}a{color:var(--brand)}.footer{font-size:13px;color:var(--muted);margin-top:30px}.small{font-size:14px}#timer{font-variant-numeric:tabular-nums;font-weight:bold}.badge{display:inline-block;background:#e7eef9;border-radius:20px;padding:3px 12px;color:var(--brand);font-size:13px}details{margin:12px 0}summary{cursor:pointer;font-weight:bold}.qactions{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}@media(max-width:600px){.wrap{padding:16px 12px 40px}.slidebody{padding:20px}.slidehead{padding:13px 20px}.slide{min-height:540px}.box,.question{padding:17px}.nav{padding:8px;gap:5px}.nav button{font-size:14px;padding:8px 10px}.slide li{font-size:18px}}@media print{@page{size:A4;margin:16mm}body{background:white;color:black;font-size:11pt}.top{padding:0;color:black;background:white}.top p{color:black}.eyebrow{color:black}.nav,.tools,.noprint,.qactions,.footer{display:none!important}.wrap{padding:0;max-width:none}.panel[hidden]{display:none!important}.question,.box,.chaptercard{border:1px solid #bbb;box-shadow:none;border-radius:0;break-inside:avoid;padding:12px;margin:12px 0}.allslide{break-before:page;border:0;padding:10px 0}.allslide h2{font-size:23pt}.allslide li{font-size:16pt;margin:16px 0}.allslide .takeaway{font-size:14pt}.slide{box-shadow:none;min-height:0}.slidehead{color:black;background:white}.opt{border:0;padding:3px 7px}.opts{gap:0}.score{background:white}.answers-print{display:block;break-before:page}.explain{background:white}.print-hide-explain .explain{display:none!important}.print-hide-explain .opt.correct,.print-hide-explain .opt.wrong{background:white;border:0}.print-hide-explain input{appearance:none;width:12px;height:12px;border:1px solid black;border-radius:50%}a{color:black;text-decoration:none}.note{background:white;color:black}}
</style></head><body>
<header class="top"><div class="eyebrow">351 / EXAM STUDY KIT</div><h1>อ่านให้เข้าใจ แล้วฝึกกาจนคล่อง</h1><p>บทอ่านละเอียด 10 บท • สไลด์สรุป 48 หน้า • ข้อสอบปรนัย 4 ตัวเลือก 200 ข้อ • เฉลยพร้อมเหตุผล • จำลองสอบ 120 ข้อ • เปิดใช้แบบออฟไลน์</p></header>
<nav class="nav" aria-label="เมนูหลัก"><button data-tab="home" aria-selected="true">เริ่มอ่าน</button><button data-tab="detailed" aria-selected="false">บทอ่านละเอียด</button><button data-tab="slides" aria-selected="false">สไลด์</button><button data-tab="all" aria-selected="false">อ่านทุกหน้า / พิมพ์</button><button data-tab="quiz" aria-selected="false">ฝึกข้อกา 200 ข้อ</button><button data-tab="mock" aria-selected="false">จำลองสอบ 120 ข้อ</button></nav>
<main class="wrap">
<section id="home" class="panel"><div class="box"><span class="badge">ขอบเขตจากภาพที่ส่งมา</span><h2>ครบหัวข้อเครือข่าย + Cloud + Wireless + Cisco</h2><p>Internet Protocol Stack and OSI Model, Application Layer Services, Routing, Link Layer Services, LAN Cabling, Principle of Cloud Computing และ Cloud Computing and Services รวมถึงผังเครือข่าย Wireless และ Cisco จากภาพที่สอง</p><p class="note">ภาพระบุยอดสอบ 120 ข้อ แต่จำนวนย่อยอ่านได้ไม่ครบและยังจับคู่ทุกหัวข้อไม่ได้ ชุดนี้จึงเป็นข้อสอบฝึกที่แต่งขึ้น ไม่ใช่ข้อสอบจริงหรือการยืนยันสัดส่วนจากอาจารย์ คำว่า “web_q 30” ในภาพยังตีความไม่ได้ชัด จึงครอบคลุม Web/HTTP และพื้นฐานเครือข่ายไว้ให้</p><p>เริ่มจากสไลด์ → ฝึกหมวดที่เพิ่งอ่าน → ตรวจเหตุผลของข้อผิด → ทำชุดจำลอง 120 ข้อ หากเวลาน้อย เริ่ม Cloud, Wireless, Routing/Subnet และ Link Layer แล้วทวนตาราง port กับคำสั่ง Cisco</p><div class="tools"><button class="primary" onclick="tab('detailed')">เปิดบทอ่านละเอียด</button><button id="startSlides">เปิดสไลด์หน้าแรก</button><button id="startQuiz">เริ่มฝึกข้อกา</button></div></div><div id="chapters" class="grid"></div><div class="box" style="margin-top:20px"><h2>แหล่งอ้างอิงและขอบเขต</h2><p>เรียบเรียงประกอบจากเอกสารเรียนไทยในโฟลเดอร์นี้ โดยเฉพาะบท 02, 07, 11–15, 19–23, 25–27, K1–K5, SUB และ LAB1–LAB9 เสริม Cloud ด้วย NIST และตรวจหลักเลือกเส้นทางกับเอกสาร Cisco ไม่มีเอกสาร Cloud ของอาจารย์อยู่ในชุดที่อ่าน จึงใช้หลักพื้นฐานทั่วไป</p><ul id="sources"></ul><p class="small muted">เนื้อหาส่วนเสริม เช่น Cloud และคำสั่ง IOS เป็นแนวทบทวน ไม่ใช่การรับรองคำสั่งของอุปกรณ์ทุกโมเดล ลิงก์อ้างอิงออนไลน์ต้องใช้ Internet ส่วนสไลด์และข้อสอบใช้ได้ออฟไลน์ทั้งหมด ลิงก์เอกสารเดิมต้องเก็บโครงสร้างโฟลเดอร์ไว้</p></div></section>
<section id="detailed" class="panel" hidden>__READING__</section>
<section id="slides" class="panel" hidden><div class="tools"><label>เลือกหมวด <select id="slideCat"></select></label><span id="slideNum" aria-live="polite"></span><button id="fullscreen">เต็มจอ</button></div><div id="slideHost"></div><div class="tools"><button id="prev">← ก่อนหน้า</button><button class="primary" id="next">ถัดไป →</button><span class="muted small">ใช้ปุ่มลูกศร ← → บนคีย์บอร์ดได้</span></div></section>
<section id="all" class="panel" hidden><div class="tools"><label>หมวด <select id="allCat"></select></label><button class="primary" id="printSlides">พิมพ์ / บันทึก PDF</button></div><div id="allHost"></div></section>
<section id="quiz" class="panel" hidden><div class="box"><h2>ฝึกข้อกา 200 ข้อ</h2><p>เลือกคำตอบ ก ข ค ง ได้ข้อเดียวต่อข้อ กดตรวจทีละข้อหรือส่งตรวจทั้งชุดที่แสดง ทุกข้อมีคำตอบที่ถูกที่สุดเพียงข้อเดียว</p><div class="tools"><label>หมวด <select id="quizCat"></select></label><label>ค้นหา <input type="search" id="search" placeholder="เช่น subnet, DNS, Cloud"></label><button id="checkQuiz" class="primary">ตรวจชุดที่แสดง</button><button id="resetQuiz">ล้างคำตอบฝึกทั้งหมด</button></div><div class="tools"><label><input type="checkbox" id="printKeys"> พิมพ์พร้อมเฉลยท้ายชุด</label><button id="printQuiz">พิมพ์ข้อสอบ / บันทึก PDF</button><span id="quizCount" class="muted"></span></div><p class="small muted">คำตอบฝึกบันทึกในเบราว์เซอร์นี้เมื่ออนุญาต localStorage; ชุดจำลองแยกคำตอบออกจากโหมดฝึก</p><div id="quizScore" class="score" aria-live="polite"></div></div><div id="quizHost"></div><div id="quizKeys" class="answers-print"></div></section>
<section id="mock" class="panel" hidden><div class="box"><h2>จำลองสอบ 120 ข้อ</h2><p>สุ่มจากคลัง 200 ข้อโดยไม่ซ้ำ ภายในแต่ละหมวดและสลับลำดับข้อ เฉลยจะเปิดหลังส่งตรวจ ไม่มีการสมมติเวลาสอบของอาจารย์</p><p class="note">สัดส่วนฝึกที่จัดไว้: OSI 10, Application 20, Routing/ผัง 15, Link 10, สาย LAN 10, Cloud 20, Wireless 20, Cisco 15 รวม 120 ข้อ ไม่ใช่สัดส่วนสอบที่ยืนยันจากภาพ</p><div class="tools"><button id="newMock" class="primary">เริ่มชุดใหม่ 120 ข้อ</button><button id="submitMock" disabled>ส่งตรวจชุดจำลอง</button><span id="timer" aria-live="off"></span><span id="mockDone" class="muted"></span></div><p class="small muted">กดเริ่มชุดใหม่อีกครั้งเพื่อล้างชุดจำลองเดิม ชุดจำลองเก็บเฉพาะระหว่างเปิดหน้านี้ รีเฟรชแล้วต้องเริ่มใหม่</p><div id="mockScore" class="score" aria-live="polite"></div></div><div id="mockHost"><p class="muted">กด “เริ่มชุดใหม่” เมื่อพร้อม แล้วทำให้ครบก่อนส่งตรวจ</p></div></section>
<p class="footer">สร้างเพื่อทบทวนตามหัวข้อในภาพ • ข้อสอบตัวอย่างไม่ใช่ข้อสอบจริง • ใช้เมนูพิมพ์ของเบราว์เซอร์เพื่อบันทึก PDF ภาษาไทย</p></main>
<script id="dataset" type="application/json">__DATA__</script>
<script>
'use strict';
const DATA=JSON.parse(document.getElementById('dataset').textContent), S=DATA.sections, Q=S.flatMap(s=>s.questions), letters=['ก','ข','ค','ง'];
const $=s=>document.querySelector(s),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const SL=S.flatMap((s,cat)=>s.slides.map((v,j)=>({cat,j,title:v[0],bullets:v[1],key:v[2]})));
let active='home',si=0,answers={},checked=new Set(),mock=[],ma={},submitted=false,start=0,finish=0;
try{const saved=JSON.parse(localStorage.getItem('351-exam-answers-v1')||'{}');if(saved&&typeof saved==='object')for(const q of Q)if(Number.isInteger(saved[q.id])&&saved[q.id]>=0&&saved[q.id]<4)answers[q.id]=saved[q.id]}catch(e){}
function save(){try{localStorage.setItem('351-exam-answers-v1',JSON.stringify(answers))}catch(e){}}
function tab(id){active=id;document.querySelectorAll('.panel').forEach(el=>el.hidden=el.id!==id);document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.tab===id)));window.scrollTo(0,0)}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>tab(b.dataset.tab));
function options(el,all){el.innerHTML=(all?'<option value="-1">ทุกหมวด</option>':'')+S.map((s,i)=>`<option value="${i}">${esc(s.name)}</option>`).join('')}
options($('#slideCat'),false);['allCat','quizCat'].forEach(id=>options($('#'+id),true));
$('#chapters').innerHTML=S.map((s,i)=>`<button class="cardlink" data-chapter="${i}"><span class="tag">บท ${String(i+1).padStart(2,'0')} / 6 สไลด์</span><strong>${esc(s.name)}</strong><span class="muted">ข้อ ${i*25+1}–${i*25+25} • 25 ข้อ</span></button>`).join('');
$('#chapters').onclick=e=>{const b=e.target.closest('[data-chapter]');if(b){si=+b.dataset.chapter*6;renderSlide();tab('slides')}};
$('#sources').innerHTML=DATA.sources.map(s=>`<li><a href="${esc(s[1])}" target="_blank" rel="noopener">${esc(s[0])}</a></li>`).join('');
function topology(s){if(s.title!=='อ่านผังเครือข่าย')return '';return `<svg viewBox="0 0 760 125" role="img" aria-label="ตัวอย่างสอง LAN ผ่าน router สองตัว แต่ละช่วงใช้ subnet แยกกัน" style="width:100%;max-height:125px"><g stroke="#577699" stroke-width="3"><path d="M110 45H270M330 45H490M550 45H690"/></g><g fill="#e8f0fb" stroke="#1746a2" stroke-width="2"><rect x="20" y="20" width="110" height="50" rx="9"/><rect x="260" y="20" width="80" height="50" rx="9"/><rect x="480" y="20" width="80" height="50" rx="9"/><rect x="650" y="20" width="100" height="50" rx="9"/></g><g font-family="Tahoma,sans-serif" font-size="16" text-anchor="middle" fill="#15243b"><text x="75" y="52">LAN A</text><text x="300" y="52">R1</text><text x="520" y="52">R2</text><text x="700" y="52">LAN B</text><text x="160" y="100">192.168.1.0/24</text><text x="410" y="100">10.0.0.0/30</text><text x="650" y="100">192.168.2.0/24</text></g></svg>`}
function bullets(s){return topology(s)+`<ul>${s.bullets.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`}
function renderSlide(){const s=SL[si];$('#slideCat').value=s.cat;$('#slideNum').textContent=`หน้า ${si+1} / ${SL.length}`;$('#prev').disabled=si===0;$('#next').disabled=si===SL.length-1;$('#slideHost').innerHTML=`<article class="slide"><div class="slidehead">${esc(S[s.cat].name)} • ${s.j+1}/6</div><div class="slidebody"><h2>${esc(s.title)}</h2>${si===0?'<div class="diagram"><span>Application</span><span>↓ Transport</span><span>↓ Network</span><span>↓ Link</span><span>↓ Physical</span></div>':''}${bullets(s)}<p class="takeaway"><strong>จำก่อนสอบ:</strong> ${esc(s.key)}</p></div><div class="progress"><span style="width:${(si+1)/SL.length*100}%"></span></div></article>`}
$('#prev').onclick=()=>{if(si>0){si--;renderSlide()}};$('#next').onclick=()=>{if(si<SL.length-1){si++;renderSlide()}};$('#slideCat').onchange=()=>{si=+$('#slideCat').value*6;renderSlide()};
document.addEventListener('keydown',e=>{if(active!=='slides'||/INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName))return;if(e.key==='ArrowRight'){$('#next').click();e.preventDefault()}if(e.key==='ArrowLeft'){$('#prev').click();e.preventDefault()}});
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('#slides').requestFullscreen()}catch(e){$('#fullscreen').textContent='ใช้เมนูเต็มจอของเบราว์เซอร์'}};
function renderAll(){let cat=+$('#allCat').value;$('#allHost').innerHTML=SL.map((s,i)=>({s,i})).filter(x=>cat<0||x.s.cat===cat).map(({s,i})=>`<article class="chaptercard allslide"><span class="tag">${esc(S[s.cat].name)} • หน้า ${i+1}/48</span><h2>${esc(s.title)}</h2>${bullets(s)}<p class="takeaway"><strong>จำก่อนสอบ:</strong> ${esc(s.key)}</p></article>`).join('')}
$('#allCat').onchange=renderAll;$('#printSlides').onclick=()=>window.print();$('#startSlides').onclick=()=>{si=0;renderSlide();tab('slides')};$('#startQuiz').onclick=()=>tab('quiz');
function selectedQuestions(){let cat=+$('#quizCat').value,term=$('#search').value.trim().toLocaleLowerCase();return Q.filter(q=>(cat<0||q.cat===S[cat].name)&&(!term||(q.q+' '+q.options.join(' ')+' '+q.cat).toLocaleLowerCase().includes(term)))}
function question(q,mode,n){let state=mode==='quiz'?answers:ma,reveal=mode==='quiz'?checked.has(q.id):submitted,chosen=state[q.id];return `<article class="question" id="${mode}-q${q.id}"><span class="tag">${mode==='mock'?'ลำดับ '+n+' • ':''}ข้อ ${q.id} / ${esc(q.cat)}</span><h3 class="qtitle">${esc(q.q)}</h3><div class="opts" role="radiogroup" aria-label="ข้อ ${q.id}">${q.options.map((o,k)=>`<label class="opt ${reveal&&k===q.answer?'correct':''} ${reveal&&chosen===k&&k!==q.answer?'wrong':''}"><input type="radio" name="${mode}-${q.id}" value="${k}" data-id="${q.id}" data-mode="${mode}" ${chosen===k?'checked':''} ${mode==='mock'&&submitted?'disabled':''}><span><strong>${letters[k]}.</strong> ${esc(o)}${reveal&&k===q.answer?' ✓ คำตอบถูก':''}${reveal&&chosen===k&&k!==q.answer?' ✕ ที่เลือก':''}</span></label>`).join('')}</div>${mode==='quiz'?`<div class="qactions noprint"><button data-check="${q.id}">ตรวจข้อนี้ / ดูเฉลย</button></div>`:''}<div class="explain" ${reveal?'':'hidden'}><strong>${chosen===undefined?'ยังไม่ได้ตอบ':chosen===q.answer?'ตอบถูก':'ตอบผิด'} • เฉลย ${letters[q.answer]}</strong><br>${esc(q.explain)}</div></article>`}
function renderQuiz(){let rows=selectedQuestions();$('#quizHost').innerHTML=rows.length?rows.map(q=>question(q,'quiz')).join(''):'<p>ไม่พบข้อที่ตรงกับการค้นหา</p>';$('#quizCount').textContent=`แสดง ${rows.length} / 200 ข้อ`;$('#quizKeys').innerHTML='<h2>เฉลยพร้อมเหตุผล</h2>'+rows.map(q=>`<p><strong>${q.id}. ${letters[q.answer]}</strong> — ${esc(q.explain)}</p>`).join('');$('#quizScore').innerHTML=''}
function score(rows,state){let done=rows.filter(q=>state[q.id]!==undefined).length,correct=rows.filter(q=>state[q.id]===q.answer).length;return `<div class="stat">${correct} / ${rows.length} คะแนน (${rows.length?Math.round(correct/rows.length*100):0}%)</div><p>ตอบแล้ว ${done} ข้อ • ถูก ${correct} • ผิด ${done-correct} • ยังไม่ตอบ ${rows.length-done}</p>`}
$('#quizCat').onchange=renderQuiz;$('#search').oninput=renderQuiz;
$('#quizHost').onclick=e=>{const b=e.target.closest('[data-check]');if(!b)return;let id=+b.dataset.check;checked.add(id);const el=$('#quiz-q'+id);el.outerHTML=question(Q[id-1],'quiz');$('#quizScore').innerHTML=''};
document.addEventListener('change',e=>{const t=e.target;if(!t.matches('input[data-mode]'))return;let id=+t.dataset.id;if(t.dataset.mode==='quiz'){answers[id]=+t.value;checked.delete(id);save();const y=window.scrollY;$('#quiz-q'+id).outerHTML=question(Q[id-1],'quiz');$('#quizScore').innerHTML='';window.scrollTo(0,y)}else{ma[id]=+t.value;updateTimer()}});
$('#checkQuiz').onclick=()=>{const rows=selectedQuestions();rows.forEach(q=>checked.add(q.id));renderQuiz();$('#quizScore').innerHTML=score(rows,answers);$('#quizScore').scrollIntoView({block:'center',behavior:'smooth'})};
$('#resetQuiz').onclick=()=>{answers={};checked.clear();save();renderQuiz()};
function printMode(){document.body.classList.toggle('print-hide-explain',!$('#printKeys').checked);$('#quizKeys').style.display=$('#printKeys').checked?'':'none'}
$('#printQuiz').onclick=()=>{printMode();window.print()};window.addEventListener('beforeprint',printMode);
function shuffled(a){const b=[...a];for(let i=b.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]}return b}
$('#newMock').onclick=()=>{const counts=[10,20,15,10,10,20,20,15];mock=shuffled(S.flatMap((s,i)=>shuffled(s.questions).slice(0,counts[i])));ma={};submitted=false;start=Date.now();finish=0;$('#mockScore').innerHTML='';$('#mockHost').innerHTML=mock.map((q,i)=>question(q,'mock',i+1)).join('');$('#submitMock').disabled=false;$('#submitMock').textContent='ส่งตรวจชุดจำลอง';updateTimer()};
$('#submitMock').onclick=()=>{if(!mock.length||submitted)return;submitted=true;finish=Date.now();$('#mockHost').innerHTML=mock.map((q,i)=>question(q,'mock',i+1)).join('');$('#mockScore').innerHTML=score(mock,ma)+'<table><thead><tr><th>หมวด</th><th>ถูก / ทั้งหมด</th></tr></thead><tbody>'+S.map(s=>{let rows=mock.filter(q=>q.cat===s.name);return `<tr><td>${esc(s.name)}</td><td>${rows.filter(q=>ma[q.id]===q.answer).length} / ${rows.length}</td></tr>`}).join('')+'</tbody></table><p>อ่านเหตุผลข้อผิด แล้วกลับไปทวนสไลด์ของหมวดที่คะแนนต่ำก่อนเริ่มรอบใหม่</p>';$('#submitMock').disabled=true;$('#submitMock').textContent='ตรวจแล้ว';updateTimer();$('#mockScore').scrollIntoView({block:'start',behavior:'smooth'})};
function updateTimer(){if(!start)return;let sec=Math.floor(((finish||Date.now())-start)/1000);$('#timer').textContent=`เวลาที่ใช้ ${Math.floor(sec/60)}:${String(sec%60).padStart(2,'0')}`;$('#mockDone').textContent=`ตอบแล้ว ${Object.keys(ma).length} / 120 ข้อ`}
setInterval(updateTimer,1000);renderSlide();renderAll();renderQuiz();
</script></body></html>'''
reading_content=render_reading()
page=page.replace('__DATA__',DATA).replace('__READING__',reading_content)
page=page.replace('</style>',READING_CSS+'</style>',1)
page=page.replace('</body>','<script>'+READING_JS+'</script></body>')
(OUT/'351-สไลด์อ่านสอบ-ข้อกา200ข้อ.html').write_text(page)
(OUT/'351-บทอ่านละเอียด.html').write_text(standalone(reading_content))
print('Created HTML:',len(SL if False else sections)*6,'slides,',sum(len(s['questions']) for s in sections),'questions')

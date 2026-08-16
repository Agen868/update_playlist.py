from http.server import BaseHTTPRequestHandler
import requests
import re
import html

# 📌 เปลี่ยนแผนยิงเข้าหาหน้าดูหลักแบบจำลองหน้าต่างบราวเซอร์เต็มรูปแบบ
def get_channel_params_real(channel_slug):
    session = requests.Session()
    
    # วิ่งเข้าหน้าสตรีมมิงตรงรุ่นที่พี่เปิดดูบนหน้าเว็บจริง (เช่น /tv/cinemax-278)
    page_url = f"https://kicksball.com/tv/{channel_slug}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://kicksball.com/tv",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
    }
    
    try:
        # เปิดหน้าเว็บจริงเพื่อแกะหาโค้ดผู้เล่นที่สร้างขึ้น ณ วินาทีนั้น
        response = session.get(page_url, headers=headers, timeout=8)
        response.encoding = 'utf-8'
        source_code = html.unescape(response.text)
        
        # 1. ค้นหาเลขเซสชัน (nimblesessionid) จากพารามิเตอร์เครื่องเล่นบนหน้าเว็บ
        session_id = ""
        session_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', source_code)
        if session_match:
            session_id = session_match.group(1)
            
        # 2. ค้นหาโทเคน (wmsAuthSign) ตัวยาวล่าสุดที่เว็บฉีดไว้ในสคริปต์
        token_str = ""
        token_patterns = [
            r'wmsAuthSign\s*=\s*[\'"]?([^\s"\'&;]+)',
            r'wmsAuthSign[\'"]?\s*[:=]\s*[\'"]?([^\s"\'&;}]+)'
        ]
        for pattern in token_patterns:
            token_match = re.search(pattern, source_code, re.IGNORECASE)
            if token_match:
                extracted_token = token_match.group(1).replace('{', '').replace('}', '')
                if "TOKEN" not in extracted_token:
                    token_str = extracted_token
                    break
                    
        # คืนค่ากรณีเจาะสำเร็จ
        if session_id and token_str:
            return f"nimblesessionid={session_id}&wmsAuthSign={token_str}"
            
    except Exception as e:
        print(f"Error fetching channel {channel_slug}: {e}")
        
    # ⚠️ แผนสำรอง (Fallback) หากช่องย่อยหลุด ให้ไปขโมยรหัสจากหน้าแรก (หน้าทีวีรวม) มาแชร์แช่ไว้แทน
    try:
        fallback_res = session.get("

 ", headers=headers, timeout=4)
        s_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', fallback_res.text)
        t_match = re.search(r'wmsAuthSign=([^\s"\'&;]+)', fallback_res.text)
        if s_match and t_match:
            return f"nimblesessionid={s_match.group(1)}&wmsAuthSign={t_match.group(1)}"
    except:
        pass
        
    # ตั๋วช่วยชีวิตใบสุดท้าย (ถ้าล่มทั้งหมด) เพื่อไม่ให้ไฟล์ส่งออกขาวโพลน
    return "nimblesessionid=241169&wmsAuthSign=c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 📌 สั่งระบุเจาะสแกนรายช่องตามชื่อทับศัพท์และตัวเลขลงท้ายบนหน้า URL ของเว็บจริง
        # (แก้ไขชื่อหลัง /tv/ ของแต่ละช่องตามลิงก์จริงที่พี่เปิดดูบนบราวเซอร์ได้เลยครับ)
        hbo_params = get_channel_params_real("hbo-276")        # ตัวอย่าง URL ช่อง HBO HD
        hbo_hits_params = get_channel_params_real("hbo-hits-277")  # ตัวอย่าง URL ช่อง HBO Hits
        cinemax_params = get_channel_params_real("cinemax-278")   # ระบุชื่อ cinemax-278 ตามเว็บของพี่เป๊ะๆ
        
        w3u_content = f"""{{
  "name": "SPORT LIVE",
  "author": "🍺 BEER-iPTV 🍺",
  "image": "https://googleusercontent.com",
  "stations": [
    {{
      "name": "HBO HD",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo/chunks.m3u8?{hbo_params}",
      "referer": "https://kicksball.com/",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "HBO Hits",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo-hits/chunks.m3u8?{hbo_hits_params}",
      "referer": "https://kicksball.com/",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "Cinemax",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/cinemax/chunks.m3u8?{cinemax_params}",
      "referer": "https://kicksball.com/",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }}
  ]
}}"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        self.wfile.write(w3u_content.encode('utf-8'))
        return
                                  

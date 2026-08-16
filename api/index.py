from http.server import BaseHTTPRequestHandler
import requests
import re
import html

# 📌 ฟังก์ชันเจาะรหัสสดรายช่องผ่านหมายเลข ID ผู้เล่นจริงบนเว็บ
def get_channel_params(channel_id):
    session = requests.Session()
    
    # เจาะทะลวงผ่านหน้าเครื่องเล่นย่อยของแต่ละช่องตรงตามเลข ID บนเว็บจริง
    player_url = f"https://kicksball.com{channel_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": f"https://kicksball.com{channel_id}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en;q=0.8"
    }
    
    session_id = ""
    token_str = ""
    
    try:
        response = session.get(player_url, headers=headers, timeout=6)
        response.encoding = 'utf-8'
        source_code = html.unescape(response.text)
        
        # แกะเลข nimblesessionid สดๆ ของช่องนั้นๆ
        session_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', source_code)
        if session_match:
            session_id = session_match.group(1)
            
        # แกะรหัสโทเคน wmsAuthSign สดๆ ของช่องนั้นๆ
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
    except:
        pass
        
    # ระบบสลับสายฉุกเฉินดึงจากหน้าหลักแก้ขัดหากช่องย่อยเกิดดึงหลุด เพื่อป้องกันจอดำ
    if not session_id or not token_str:
        try:
            fallback_res = session.get("https://kicksball.com278", headers=headers, timeout=4)
            s_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', fallback_res.text)
            t_match = re.search(r'wmsAuthSign=([^\s"\'&;]+)', fallback_res.text)
            if s_match and t_match:
                session_id = s_match.group(1)
                token_str = t_match.group(1)
        except:
            session_id = "241169"
            token_str = "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"
            
    return f"nimblesessionid={session_id}&wmsAuthSign={token_str}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 📌 ดึงพารามิเตอร์แยกตามตัวเลขไอดีหลัง URL หน้ารับชมทีวีของเว็บต้นทางจริง
        # (สมมุติเลขช่อง HBO และ HBO Hits ตามสถิติข้อมูลของเซิร์ฟเวอร์เดิม)
        hbo_params = get_channel_params("hbo-274")       # ตัวอย่าง ID ช่อง HBO HD
        hbo_hits_params = get_channel_params("hbo-hits-276")  # ตัวอย่าง ID ช่อง HBO Hits
        cinemax_params = get_channel_params("cinemax-278")   # ระบุเจาะจงเลข 278 ตามลิงก์ Cinemax จริงของพี่เป๊ะๆ
        
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

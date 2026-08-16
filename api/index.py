from http.server import BaseHTTPRequestHandler
import requests
import re
import html

# 📌 ฟังก์ชันพุ่งเจาะดึงรหัสโทเคนความปลอดภัย (wmsAuthSign) ตัวยาวล่าสุดอย่างเด็ดขาด
def get_clean_wms_token():
    session = requests.Session()
    # ดึงค่าผ่านหน้าแรกของเครื่องเล่นที่ปลอดภัยที่สุด
    target_url = "https://kicksball.com"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://kicksball.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # โทเคนสำรองชุดยาว (ตั๋วช่วยชีวิตใบสุดท้าย)
    default_token = "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"
    
    try:
        response = session.get(target_url, headers=headers, timeout=6)
        response.encoding = 'utf-8'
        source_code = html.unescape(response.text)
        
        # กวาดสายตาค้นหาเฉพาะรหัสลับ wmsAuthSign ตัวยาว
        token_patterns = [
            r'wmsAuthSign\s*=\s*[\'"]?([^\s"\'&;]+)',
            r'wmsAuthSign[\'"]?\s*[:=]\s*[\'"]?([^\s"\'&;}]+)'
        ]
        for pattern in token_patterns:
            token_match = re.search(pattern, source_code, re.IGNORECASE)
            if token_match:
                extracted_token = token_match.group(1).replace('{', '').replace('}', '')
                if len(extracted_token) > 20 and "TOKEN" not in extracted_token:
                    return extracted_token
    except:
        pass
        
    return default_token

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 📌 ฉกเอาเฉพาะโทเคนหลักสด ๆ วินาทีนั้นรอบเดียว แล้วกระจายฉีดใส่ทุกช่องทันที
        live_token = get_clean_wms_token()
        
        # 📌 จัดทำโครงสร้างลิงก์แบบตัดพารามิเตอร์ nimblesessionid ออกไป เพื่อไม่ให้ช่องโดนบล็อกและหมดอายุไว
        w3u_content = f"""{{
  "name": "SPORT LIVE",
  "author": "🍺 BEER-iPTV 🍺",
  "image": "https://googleusercontent.com",
  "stations": [
    {{
      "name": "HBO HD",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo/chunks.m3u8?{live_token}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "HBO Hits",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo-hits/chunks.m3u8?{live_token}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "Cinemax",
      "image": "https://githubusercontent.com",
      "url": "https://dov.streaming-api.xyz/kicksballcom/cinemax/chunks.m3u8?{live_token}",
      "referer": "https://kicksball.com",
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

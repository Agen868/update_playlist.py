from http.server import BaseHTTPRequestHandler
import requests
import re
import html

# 📌 ปรับปรุงฟังก์ชันให้รองรับการดึงแยกทีละช่องอย่างแม่นยำ
def get_channel_params(channel_slug):
    session = requests.Session()
    # หากเป็นช่อง hbo ปกติให้ไปหน้าทีวีหลัก หากเป็นช่องย่อยให้ไปตาม slug ตรงรุ่น
    if channel_slug == "hbo":
        player_url = "https://kicksball.com"
    else:
        player_url = f"https://kicksball.com?id={channel_slug}"
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://kicksball.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # ค่าตั๋วสำรองรายช่องแยกกลุ่ม ป้องกันรหัสซ้ำข้ามช่อง
    fallback_seeds = {
        "hbo": ("241169", "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"),
        "hbo-hits": ("242200", "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDU6MDA6MDUgQU0maGFzaF92YWx1ZT14WVpB..."),
        "cinemax": ("243300", "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDU6MTU6MDUgQU0maGFzaF92YWx1ZT1hQkNE...")
    }
    session_id, token_str = fallback_seeds.get(channel_slug, ("241169", ""))
    
    try:
        response = session.get(player_url, headers=headers, timeout=5)
        response.encoding = 'utf-8'
        source_code = html.unescape(response.text)
        
        # ค้นหาเลขเซสชันประจำช่อง
        session_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', source_code)
        if session_match:
            session_id = session_match.group(1)
            
        # ค้นหาโทเคนประจำช่อง
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
        
    return f"nimblesessionid={session_id}&wmsAuthSign={token_str}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 📌 สั่งระบบแยกยิงไปกระชากรหัสสด ๆ แยกเป็นรายช่องเด็ดขาด ไม่ใช้เลขแชร์ร่วมกันแล้ว
        hbo_params = get_channel_params("hbo")
        hbo_hits_params = get_channel_params("hbo-hits")
        cinemax_params = get_channel_params("cinemax")
        
        # ประกอบโครงสร้างข้อมูลพ่น W3U ป้อนเลขพารามิเตอร์แยกจากกันรายบรรทัด
        w3u_content = f"""{{
  "name": "SPORT LIVE",
  "author": "🍺 BEER-iPTV 🍺",
  "image": "https://googleusercontent.com",
  "stations": [
    {{
      "name": "HBO HD",
      "image": "https://githubusercontent.com",
      "url": "https://streaming-api.xyz?{hbo_params}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "HBO Hits",
      "image": "https://githubusercontent.com",
      "url": "https://streaming-api.xyz?{hbo_hits_params}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "Cinemax",
      "image": "https://githubusercontent.com",
      "url": "https://streaming-api.xyz?{cinemax_params}",
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

from http.server import BaseHTTPRequestHandler
import requests
import re
import html

def get_live_stream_params():
    session = requests.Session()
    player_url = "https://kicksball.com"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://kicksball.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "th-TH,th;q=0.9,en;q=0.8"
    }
    
    session_id = "241169"
    token_str = "c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"
    
    try:
        response = session.get(player_url, headers=headers, timeout=5)
        response.encoding = 'utf-8'
        source_code = html.unescape(response.text)
        
        session_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', source_code)
        if session_match:
            session_id = session_match.group(1)
            
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
        current_params = get_live_stream_params()
        
        w3u_content = f"""{{
  "name": "SPORT LIVE",
  "author": "🍺 BEER-iPTV 🍺",
  "image": "https://googleusercontent.com",
  "stations": [
    {{
      "name": "HBO HD",
      "image": "",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo/chunks.m3u8?{current_params}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "HBO Hits",
      "image": "",
      "url": "https://dov.streaming-api.xyz/kicksballcom/hbo-hits/chunks.m3u8?{current_params}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }},
    {{
      "name": "Cinemax",
      "image": "",
      "url": "https://dov.streaming-api.xyz/kicksballcom/cinemax/chunks.m3u8?{current_params}",
      "referer": "https://kicksball.com",
      "info": "kicksball🍺",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
      "playInNatPlayer": "true"
    }}
  ]
}}"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(w3u_content.encode('utf-8'))
        return


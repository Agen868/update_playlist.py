import requests
import re
import html

def get_channel_params_from_web(channel_slug):
    session = requests.Session()
    # ดึงค่าผ่านหน้า URL รับชมจริงของแต่ละช่องเพื่อหลบระบบ Cloudflare
    page_url = f"https://kicksball.com{channel_slug}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://kicksball.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = session.get(page_url, headers=headers, timeout=10)
        source_code = html.unescape(response.text)
        
        # แกะรหัสเซสชันแท้
        session_id = ""
        session_match = re.search(r'nimblesessionid\s*=\s*[\'"]?([0-9]+)', source_code)
        if session_match:
            session_id = session_match.group(1)
            
        # แกะโทเคนแท้ชุดยาว
        token_str = ""
        token_patterns = [
            r'wmsAuthSign\s*=\s*[\'"]?([^\s"\'&;]+)',
            r'wmsAuthSign[\'"]?\s*[:=]\s*[\'"]?([^\s"\'&;}]+)'
        ]
        for pattern in token_patterns:
            token_match = re.search(pattern, source_code, re.IGNORECASE)
            if token_match:
                token_str = token_match.group(1).replace('{', '').replace('}', '')
                break
                
        if session_id and token_str:
            return f"nimblesessionid={session_id}&wmsAuthSign={token_str}"
    except:
        pass
        
    return None

def main():
    print("🤖 บอท GitHub เริ่มปฏิบัติการดึงรหัสแยกช่องสกัดลิงก์ดับ...")
    
    # สั่งเจาะดึงรหัสตรงรุ่นแยกรายช่องจากหน้าเว็บหลักของแต่ละสถานี
    hbo_res = get_channel_params_from_web("hbo-276")
    hbo_hits_res = get_channel_params_from_web("hbo-hits-277")
    cinemax_res = get_channel_params_from_web("cinemax-278")

    # แผนสองสำรองระบบ: หากช่องย่อยดึงไม่ติด ให้ดึงจากสายแชร์และล็อกค่าตั๋วชุดล่าสุดของพี่แช่ไว้แก้ขัด
    shared_fallback = "nimblesessionid=244733&wmsAuthSign=c2VydmVyX3RpbWU9OC8xNi8yMDI2IDQ6NDc6MDUgQU0maGFzaF92YWx1ZT1iUUFDRloraW45bGxkTjV5WkRMYkJ3PT0mdmFsaWRtaW51dGVzPTIw"
    if not hbo_res: hbo_res = shared_fallback
    if not hbo_hits_res: hbo_hits_res = shared_fallback
    if not cinemax_res: cinemax_res = shared_fallback

    # เปิดอ่านไฟล์เทมเพลตต้นแบบ
    try:
        with open("template.w3u", "r", encoding="utf-8") as f:
            w3u_text = f.read()
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ template.w3u")
        return

    # เสียบพารามิเตอร์แบบคู่แยกช่องใครช่องมันอย่างเด็ดขาด ตัวเลขจะไม่ซ้ำกันเลย
    w3u_text = w3u_text.replace("{{HBO_PARAMS}}", hbo_res)
    w3u_text = w3u_text.replace("{{HBO_HITS_PARAMS}}", hbo_hits_res)
    w3u_text = w3u_text.replace("{{CINEMAX_PARAMS}}", cinemax_res)

    # บันทึกไฟล์ผลลัพธ์
    with open("playlist.w3u", "w", encoding="utf-8") as f:
        f.write(w3u_text)
    print("🎉 ผลิตไฟล์ playlist.w3u นามสกุลใหม่เวอร์ชันแยกท่อสำเร็จแล้ว!")

if __name__ == "__main__":
    main()

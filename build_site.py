import os
import requests
import sys

try:
    # 1. Ortam Değişkenlerini Kontrol Et
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("\n[HATA] GitHub Secrets eksik!")
        print(f"SUPABASE_URL var mı?: {'EVET' if SUPABASE_URL else 'HAYIR'}")
        print(f"SUPABASE_KEY var mı?: {'EVET' if SUPABASE_KEY else 'HAYIR'}")
        sys.exit(1)

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    # 2. Supabase'e İstek At
    print("[BİLGİ] Supabase'e bağlanılıyor...")
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/apks?order=id.desc"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"\n[HATA] Supabase API Hata Verdi! Durum Kodu: {response.status_code}")
        print("Hata İçeriği:", response.text)
        sys.exit(1)

    apk_list = response.json()
    print(f"[BİLGİ] Veritabanından {len(apk_list)} adet APK kaydı çekildi.")

    # 3. HTML Şablonunu Oluştur
    categories = {"social": "", "system": "", "game": ""}
    kategori_isimleri = {"social": "İnternet & Sosyal Medya", "system": "Sistem Araçları", "game": "Klasik Oyunlar"}
    kategori_ikonlari = {"social": "Op", "system": "ES", "game": "FB"}
    kategori_renkleri = {"social": "icon-social", "system": "icon-system", "game": "icon-game"}

    for apk in apk_list:
        cat = apk.get("category", "system")
        html_row = f"""
        <tr>
            <td style="width: 35px;" align="center"><div class="app-icon {kategori_renkleri.get(cat, 'icon-system')}">{kategori_ikonlari.get(cat, 'APK')}</div></td>
            <td>
                <div class="app-title">{apk.get('app_name', 'Bilinmeyen Uygulama')}</div>
                <div class="app-meta">{apk.get('file_size', '0 MB')} | Android 2.3+</div>
            </td>
            <td align="right" style="width: 65px;">
                <a href="{apk.get('file_url', '#')}" class="btn-download">İNDİR</a>
            </td>
        </tr>"""
        if cat in categories:
            categories[cat] += html_row

    dinamik_icerik = ""
    for key, rows in categories.items():
        if rows:
            dinamik_icerik += f'\n    <div class="category-title">{kategori_isimleri[key]}</div>\n    <table class="app-table">{rows}\n    </table>'

    mobil_html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://w3.org">
<html xmlns="http://w3.org" lang="tr">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>RetroAPK - Android 2.3 Arşivi</title>
    <style type="text/css">
        body {{ font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 5px; font-size: 14px; }}
        a {{ color: #4caf50; text-decoration: none; }}
        .header {{ background-color: #1f1f1f; border-bottom: 2px solid #4caf50; padding: 10px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 18px; color: #4caf50; }}
        .category-title {{ background-color: #2e2e2e; padding: 5px 8px; font-weight: bold; font-size: 12px; border-left: 3px solid #4caf50; margin: 10px 0 5px 0; }}
        .app-table {{ width: 100%; border-collapse: collapse; background-color: #1a1a1a; }}
        .app-table td {{ padding: 8px; border-bottom: 1px solid #2d2d2d; vertical-align: middle; }}
        .app-title {{ font-weight: bold; font-size: 13px; color: #ffffff; }}
        .app-meta {{ font-size: 11px; color: #888888; margin-top: 1px; }}
        .btn-download {{ background-color: #4caf50; color: #ffffff !important; padding: 4px 8px; display: inline-block; font-size: 11px; font-weight: bold; border-radius: 2px; }}
        .app-icon {{ width: 28px; height: 28px; border-radius: 3px; display: inline-block; text-align: center; line-height: 28px; font-weight: bold; color: #ffffff; font-size: 12px; }}
        .icon-social {{ background-color: #3b5998; }}
        .icon-system {{ background-color: #ff9800; }}
        .icon-game {{ background-color: #e91e63; }}
        .footer {{ text-align: center; padding: 15px; font-size: 11px; color: #666666; border-top: 1px solid #2d2d2d; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="header"><h1>RetroAPK - Mobil Sürüm</h1></div>
    {dinamik_icerik}
    <div class="footer">RetroAPK © 2026<br />Ekstrem Veri Tasarrufu Aktif</div>
</body>
</html>"""

    os.makedirs("mobil", exist_ok=True)
    with open("mobil/index.html", "w", encoding="utf-8") as f:
        f.write(mobil_html)

    print("✔ [BAŞARILI] Mobil site başarıyla üretildi!")

except Exception as e:
    print(f"\n[KRİTİK HATA] Kod çalışırken çöktü! Hata mesajı: {str(e)}")
    sys.exit(1)

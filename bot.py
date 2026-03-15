import requests
import re
import json

def get_mansetler():
    url = "https://www.haber7.com/gazete-mansetleri"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        # Haber7 resim desenini yakala
        pattern = r'https://image8x\.haber7\.net/haber/haber7/manset/[^\s"\']+\.jpg'
        urls = re.findall(pattern, response.text)
        
        # Tekrar edenleri temizle ve listeyi döndür
        return list(dict.fromkeys(urls))
    except Exception as e:
        print(f"Hata: {e}")
        return []

manset_listesi = get_mansetler()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump({"success": True, "count": len(manset_listesi), "mansetler": manset_listesi}, f)

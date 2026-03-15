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
        html_content = response.text
        
        # 1. Yöntem: Spesifik Haber7 manşet yapısını yakala
        # Genellikle manset-item içindeki img etiketlerini hedefler
        urls = re.findall(r'https://image8x\.haber7\.net/haber/haber7/manset/[^\s"\']+\.jpg', html_content)
        
        # 2. Yöntem (Yedek): Eğer ilk yöntem boş dönerse daha geniş bir tarama yap
        if not urls:
            # Sayfa içindeki tüm büyük jpg resimlerini bulmaya çalış
            urls = re.findall(r'https://[^\s"\']+/manset/[^\s"\']+\.jpg', html_content)

        # Tekrar edenleri temizle ve temiz bir liste oluştur
        clean_urls = list(dict.fromkeys(urls))
        
        # Sadece gerçek manşetleri (küçük ikon olmayanları) filtrele
        final_list = [u for u in clean_urls if "logo" not in u.lower()]
        
        return final_list
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

manset_listesi = get_mansetler()

# JSON dosyasını oluştur
data = {
    "success": len(manset_listesi) > 0,
    "count": len(manset_listesi),
    "mansetler": manset_listesi
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

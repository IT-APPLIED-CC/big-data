from pygooglenews import GoogleNews
import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse

# Google News Crawling
gn = GoogleNews(country='ID')

def generate_fallback_summary(title, link):
    """
    Membuat ringkasan fallback berdasarkan title dan bagian domain dari link.
    """
    parsed_url = urlparse(link)
    domain = parsed_url.netloc  # Ambil domain dari URL
    return f"{title[:50]}... (Sumber: {domain})"

def get_news_data(search, max_results=50):
    stories = []
    search_results = gn.search(search)
    news_items = search_results['entries'][:max_results]  # Batasi hasil

    for item in news_items:
        # Collect basic data
        story = {
            'Title': item.title,
            'Sumber': getattr(item, 'source', 'N/A'),  # Publisher/Source
            'Tanggal': getattr(item, 'published', 'N/A'),  # Publish date
            'Link': item.link,
            'Ringkasan': 'N/A'  # Default value for summary
        }
        
        # Mengambil hasil singkat pembahasan (paragraf pertama dari link)
        try:
            response = requests.get(item.link, timeout=5)  # Fetch the article page
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Ambil paragraf pertama
                paragraph = soup.find('p')
                if paragraph and paragraph.get_text(strip=True):
                    story['Ringkasan'] = paragraph.get_text(strip=True)[:150]  # Ambil 150 karakter pertama
                else:
                    # Jika tidak ada paragraf, gunakan fallback ringkasan
                    story['Ringkasan'] = generate_fallback_summary(item.title, item.link)
            else:
                # Jika gagal request, gunakan fallback
                story['Ringkasan'] = generate_fallback_summary(item.title, item.link)
        except Exception as e:
            # Jika terjadi error, gunakan fallback
            print(f"Gagal mengambil ringkasan untuk {item.link}: {e}")
            story['Ringkasan'] = generate_fallback_summary(item.title, item.link)
        
        stories.append(story)
    return stories

# Simpan Data ke CSV
def save_to_csv(stories, filename):
    output_dir = "crawl-output"
    os.makedirs(output_dir, exist_ok=True)  # Buat direktori jika belum ada
    
    file_path = os.path.join(output_dir, filename)
    header = ['Title', 'Sumber', 'Tanggal', 'Ringkasan', 'Link']
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()  # Tulis header
        for story in stories:
            writer.writerow({
                'Title': story['Title'],
                'Sumber': story['Sumber'],
                'Tanggal': story['Tanggal'],
                'Ringkasan': story['Ringkasan'],
                'Link': story['Link']
            })
    print(f"Data berhasil disimpan di {file_path}")

# Main Program
if __name__ == "__main__":
    search_query = 'ChatGPT'  # Kata kunci pencarian berita
    max_news = 100  # Jumlah berita maksimum yang akan diambil
    
    # Mengambil data berita
    print("Mengambil data berita, mohon tunggu...")
    stories = get_news_data(search_query, max_results=max_news)
    
    # Menyimpan ke CSV
    csv_filename = f'{search_query}_news.csv'
    save_to_csv(stories, csv_filename)

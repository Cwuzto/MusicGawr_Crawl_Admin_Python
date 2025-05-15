import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_nhaccuatui_top100():
    """
    Scrape top 100 songs from NhacCuaTui
    """
    url = "https://www.nhaccuatui.com/top100/top-100-nhac-tre.m3liaiy6vVsF.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract songs from the list
        songs = []
        li_tags = soup.select('.list_show_chart li')
        
        for li in li_tags:
            try:
                # Extract song information
                rank = li.select_one('.chart_tw').text.strip()
                title = li.select_one('.name_song').text.strip()
                
                # Extract singers
                singers_elements = li.select('.list_name_singer .name_singer')
                singers = [singer.text.strip() for singer in singers_elements]
                artists = ', '.join(singers)
                
                # Extract image URL
                img_element = li.select_one('.box_info_field img')
                img_url = ""
                if img_element:
                    # Try different attributes for image URL
                    if img_element.get('data-src'):
                        img_url = img_element['data-src']
                    elif img_element.get('src') and not img_element['src'].endswith('avatar_default.jpg'):
                        img_url = img_element['src']
                
                # Extract song URL
                song_url = li.select_one('.name_song')['href'] if li.select_one('.name_song') else ""
                
                songs.append({
                    'rank': rank,
                    'title': title,
                    'artists': artists,
                    'img_url': img_url,
                    'song_url': song_url,
                    'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
            except Exception as e:
                print(f"Error processing a song: {e}")
                continue
        
        return songs
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def save_to_csv(songs, filename="nhaccuatui_top100.csv"):
    """
    Save the scraped songs to a CSV file
    """
    fieldnames = ['rank', 'title', 'artists', 'img_url', 'song_url', 'date_scraped']
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(songs)
    
    return filename

if __name__ == "__main__":
    print("Starting to scrape NhacCuaTui Top 100...")
    songs = scrape_nhaccuatui_top100()
    
    if songs:
        csv_file = save_to_csv(songs)
        print(f"Successfully scraped {len(songs)} songs and saved to {csv_file}")
    else:
        print("No songs were scraped.")
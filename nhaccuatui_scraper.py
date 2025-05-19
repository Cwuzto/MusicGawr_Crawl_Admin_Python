import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from datetime import datetime
import time
import sys

def scrape_nhaccuatui(type, category, subcategory):
    """
    Scrape data from NhacCuaTui based on type, category, and subcategory.
    """
    # Mapping of menu selections to URLs and CSS selectors
    page_config = {
        'playlist': {
            'vietnam': {
                'nhactre': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-tre-moi.html',
                    'selector': '.list_album ul li'
                },
                'trutinh': {
                    'url': 'https://www.nhaccuatui.com/playlist/tru-tinh-moi.html',
                    'selector': '.list_album ul li'
                },
                'remixviet': {
                    'url': 'https://www.nhaccuatui.com/playlist/remix-viet-moi.html',
                    'selector': '.list_album ul li'
                },
                'rapviet': {
                    'url': 'https://www.nhaccuatui.com/playlist/rap-viet-moi.html',
                    'selector': '.list_album ul li'
                },
                'tienchien': {
                    'url': 'https://www.nhaccuatui.com/playlist/tien-chien-moi.html',
                    'selector': '.list_album ul li'
                },
                'nhactrinh': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-trinh-moi.html',
                    'selector': '.list_album ul li'
                },
                'rockviet': {
                    'url': 'https://www.nhaccuatui.com/playlist/rock-viet-moi.html',
                    'selector': '.list_album ul li'
                },
                'cachmang': {
                    'url': 'https://www.nhaccuatui.com/playlist/cach-mang-moi.html',
                    'selector': '.list_album ul li'
                }
            },
            'usuk': {
                'pop': {
                    'url': 'https://www.nhaccuatui.com/playlist/pop-moi.html',
                    'selector': '.list_album ul li'
                },
                'rock': {
                    'url': 'https://www.nhaccuatui.com/playlist/rock-moi.html',
                    'selector': '.list_album ul li'
                },
                'electronicadance': {
                    'url': 'https://www.nhaccuatui.com/playlist/electronicadance-moi.html',
                    'selector': '.list_album ul li'
                },
                'rbhiphoprap': {
                    'url': 'https://www.nhaccuatui.com/playlist/rbhip-hoprap-moi.html',
                    'selector': '.list_album ul li'
                },
                'bluesjazz': {
                    'url': 'https://www.nhaccuatui.com/playlist/bluesjazz-moi.html',
                    'selector': '.list_album ul li'
                },
                'country': {
                    'url': 'https://www.nhaccuatui.com/playlist/country-moi.html',
                    'selector': '.list_album ul li'
                },
                'latin': {
                    'url': 'https://www.nhaccuatui.com/playlist/latin-moi.html',
                    'selector': '.list_album ul li'
                },
                'indie': {
                    'url': 'https://www.nhaccuatui.com/playlist/indie-moi.html',
                    'selector': '.list_album ul li'
                },
                'aumy-khac': {
                    'url': 'https://www.nhaccuatui.com/playlist/au-my-khac-moi.html',
                    'selector': '.list_album ul li'
                }
            },
            'asia': {
                'nhachan': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-han-moi.html',
                    'selector': '.list_album ul li'
                },
                'nhachoa': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-hoa-moi.html',
                    'selector': '.list_album ul li'
                },
                'nhacnhat': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-nhat-moi.html',
                    'selector': '.list_album ul li'
                },
                'nhacthai': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-thai-moi.html',
                    'selector': '.list_album ul li'
                }
            },
            'other': {
                'thieunhi': {
                    'url': 'https://www.nhaccuatui.com/playlist/thieu-nhi-moi.html',
                    'selector': '.list_album ul li'
                },
                'khongloi': {
                    'url': 'https://www.nhaccuatui.com/playlist/khong-loi-moi.html',
                    'selector': '.list_album ul li'
                },
                'nhacphim': {
                    'url': 'https://www.nhaccuatui.com/playlist/nhac-phim-moi.html',
                    'selector': '.list_album ul li'
                },
                'theloaikhac': {
                    'url': 'https://www.nhaccuatui.com/playlist/the-loai-khac-moi.html',
                    'selector': '.list_album ul li'
                }
            }
        },
        'top100': {
            'vietnam': {
                'nhactre': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-nhac-tre.m3liaiy6vVsF.html',
                    'selector': '.list_show_chart li' 
                },
                'trutinh': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-tru-tinh.RKuTtHiGC8US.html',
                    'selector': '.list_show_chart li'
                },
                'remixviet': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-remix-viet.aY3KIEnpCywU.html',
                    'selector': '.list_show_chart li'
                },
                'rapviet': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-rap-viet.iY1AnIsXedqE.html',
                    'selector': '.list_show_chart li'
                },
                'tienchien': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-tien-chien.TDSMAL1lI8F6.html',
                    'selector': '.list_show_chart li'
                },
                'nhactrinh': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-nhac-trinh.v0AGjIhhCegh.html',
                    'selector': '.list_show_chart li'
                }
            },
            'usuk': {
                'pop': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-pop.zE23R7bc8e9X.html',
                    'selector': '.list_show_chart li'
                },
                'electronicadance': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-electronica-dance.ippIsiqacmnE.html',
                    'selector': '.list_show_chart li'
                },
                'rbhiphoprap': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-rb-hip-hop-rap.bxkenI7MAoFv.html',
                    'selector': '.list_show_chart li'
                },
                'bluesjazz': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-blues-jazz.BjTXbslQAOYD.html',
                    'selector': '.list_show_chart li'
                },
                'country': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-country.EpHtSo41Zstq.html',
                    'selector': '.list_show_chart li'
                },
                'latin': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-latin.cv4YefsXF887.html',
                    'selector': '.list_show_chart li'
                }
            },
            'asia': {
                'nhachan': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-nhac-han.iciV0mD8L9Ed.html',
                    'selector': '.list_show_chart li'
                },
                'nhachoa': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-nhac-hoa.g4Y7NTPP9exf.html',
                    'selector': '.list_show_chart li'
                },
                'nhacnhat': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-nhac-nhat.aOokfjySrloy.html',
                    'selector': '.list_show_chart li'
                }
            },
            'other': {
                'khongloi': {
                    'url': 'https://www.nhaccuatui.com/top100/top-100-khong-loi.kr9KYNtkzmnA.html',
                    'selector': '.list_show_chart li'
                }
            }
        },
        'song': {
            'vietnam': {
                'nhactre': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-tre-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'trutinh': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/tru-tinh-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'remixviet': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/remix-viet-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'rapviet': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/rap-viet-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'tienchien': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/tien-chien-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'nhactrinh': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-trinh-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'rockviet': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/rock-viet-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'cachmang': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/cach-mang-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                }
            },
            'usuk': {
                'pop': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/pop-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'rock': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/rock-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'electronicadance': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/electronicadance-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'rbhiphoprap': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/rbhip-hoprap-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'bluesjazz': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/bluesjazz-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'country': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/country-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'latin': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/latin-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'indie': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/indie-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'aumy-khac': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/au-my-khac-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                }
            },
            'asia': {
                'nhachan': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-han-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'nhachoa': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-hoa-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'nhacnhat': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-nhat-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'nhacthai': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/nhac-thai-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                }
            },
            'other': {
                'thieunhi': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/thieu-nhi-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'khongloi': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/khong-loi-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'beat': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/beat-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                },
                'theloaikhac': {
                    'url': 'https://www.nhaccuatui.com/bai-hat/the-loai-khac-moi.html',
                    'selector': '.list_music.listGenre .fram_select .listGenre li'
                }
            }
        },
        'collection': {
            'genre': {
                'nhactre': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/nhac-tre',
                    'selector': 'div.list_album.tag ul li'
                },
                'trutinh': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/tru-tinh',
                    'selector': 'div.list_album.tag ul li'
                },
                'pop': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/pop',
                    'selector': 'div.list_album.tag ul li'
                },
                'nhachan': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/nhac-han',
                    'selector': 'div.list_album.tag ul li'
                },
                'nhachoa': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/nhac-hoa',
                    'selector': 'div.list_album.tag ul li'
                },
                'soundtrack': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/soundtrack',
                    'selector': 'div.list_album.tag ul li'
                },
                'khongloi': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/khong-loi',
                    'selector': 'div.list_album.tag ul li'
                }
            },
            'mood': {
                'buon': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/buon',
                    'selector': 'div.list_album.tag ul li'
                },
                'hungphan': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/hung-phan',
                    'selector': 'div.list_album.tag ul li'
                },
                'nhonhung': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/nho-nhung',
                    'selector': 'div.list_album.tag ul li'
                },
                'thattinh': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/that-tinh',
                    'selector': 'div.list_album.tag ul li'
                },
                'thugian': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/thu-gian',
                    'selector': 'div.list_album.tag ul li'
                },
                'vuive': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/vui-ve',
                    'selector': 'div.list_album.tag ul li'
                }
            },
            'scene': {
                'cafe': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/cafe',
                    'selector': 'div.list_album.tag ul li'
                },
                'barclub': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/bar-club',
                    'selector': 'div.list_album.tag ul li'
                },
                'phongtra': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/phong-tra',
                    'selector': 'div.list_album.tag ul li'
                },
                'tamboiloi': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/tam-boi-loi',
                    'selector': 'div.list_album.tag ul li'
                },
                'tapgym': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/tap-gym',
                    'selector': 'div.list_album.tag ul li'
                },
                'langman': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/lang-man',
                    'selector': 'div.list_album.tag ul li'
                },
                'mua': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/mua',
                    'selector': 'div.list_album.tag ul li'
                }
            },
            'topic': {
                'tinhyeu': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/tinh-yeu',
                    'selector': 'div.list_album.tag ul li'
                },
                'top100': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/top-100',
                    'selector': 'div.list_album.tag ul li'
                },
                'weekend': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/weekend',
                    'selector': 'div.list_album.tag ul li'
                },
                'chillout': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/chill-out',
                    'selector': 'div.list_album.tag ul li'
                },
                'bathu': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/bat-hu',
                    'selector': 'div.list_album.tag ul li'
                },
                'songca': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/song-ca',
                    'selector': 'div.list_album.tag ul li'
                },
                'mashup': {
                    'url': 'https://www.nhaccuatui.com/playlist/tags/mashup',
                    'selector': 'div.list_album.tag ul li'
                }
            }
        }
    }

    # Get URL and selector based on parameters
    try:
        config = page_config.get(type, {}).get(category, {}).get(subcategory, {})
        url = config.get('url')
        selector = config.get('selector')
    except Exception as e:
        print(f"Configuration error: No config for type={type}, category={category}, subcategory={subcategory}. Error: {e}")
        return []

    if not url or not selector:
        print(f"Invalid configuration: url={url}, selector={selector}")
        return []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print(f"Fetching URL: {url}")
        time.sleep(1)  # Add 1-second delay
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Response status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        li_tags = soup.select(selector)
        print(f"Found {len(li_tags)} elements for {subcategory}")

        items = []
        for li in li_tags:
            try:
                if type == 'top100':
                    rank_element = li.select_one('.chart_tw')
                    rank = rank_element.text.strip() if rank_element else ''
                    title_element = li.select_one('.name_song')
                    title = title_element.text.strip() if title_element else 'Unknown Title'
                    singers_elements = li.select('.list_name_singer .name_singer')
                    artists = ', '.join([singer.text.strip() for singer in singers_elements]) if singers_elements else 'Unknown Artist'
                    img_element = li.select_one('.box_info_field img')
                    img_url = img_element.get('data-src') or img_element.get('src') or 'https://stc-id.nixcdn.com/v11/images/avatar_default.jpg'
                    song_url = title_element.get('href') if title_element else ''
                    
                    # Check for copyright block
                    if song_url:
                        song_response = requests.get(song_url, headers=headers)
                        song_response.raise_for_status()
                        song_soup = BeautifulSoup(song_response.text, 'html.parser')
                        if song_soup.find(string="Nội dung bị đóng theo yêu cầu của đơn vị chủ sở hữu bản quyền."):
                            print(f"Bỏ qua bài hát bị bản quyền: {title} - {song_url}")
                            continue
                    
                    items.append({
                        'rank': rank,
                        'title': title,
                        'artists': artists,
                        'img_url': img_url,
                        'song_url': song_url,
                        'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                elif type == 'song':
                    title_element = li.select_one('.name_song')
                    title = title_element.text.strip() if title_element else 'Unknown Title'
                    singers_elements = li.select('.name_sing_under .name_singer')
                    artists = ', '.join([singer.text.strip() for singer in singers_elements]) if singers_elements else 'Unknown Artist'
                    img_element = li.select_one('.avatar_song img')
                    img_url = img_element.get('data-src') or img_element.get('src') or 'https://stc-id.nixcdn.com/v11/images/avatar_default.jpg'
                    song_url = title_element.get('href') if title_element else ''
                    
                    # Check for copyright block
                    if song_url:
                        song_response = requests.get(song_url, headers=headers)
                        song_response.raise_for_status()
                        song_soup = BeautifulSoup(song_response.text, 'html.parser')
                        if song_soup.find(string="Nội dung bị đóng theo yêu cầu của đơn vị chủ sở hữu bản quyền."):
                            print(f"Bỏ qua bài hát bị bản quyền: {title} - {song_url}")
                            continue
                    
                    items.append({
                        'rank': '',
                        'title': title,
                        'artists': artists,
                        'img_url': img_url,
                        'song_url': song_url,
                        'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                elif type in ['collection', 'playlist']:
                    title_element = li.select_one('.info_album h2 a') or li.select_one('.info_album h3 a')
                    title = title_element.text.strip() if title_element else 'Unknown Playlist'
                    artist_element = li.select_one('.info_album p a.name_singer')
                    artists = artist_element.text.strip() if artist_element else 'Various Artists'
                    img_element = li.select_one('.box-left-album img')
                    img_url = img_element.get('data-src') or img_element.get('src') or 'https://stc-id.nixcdn.com/v11/images/img-plist-full.jpg'
                    playlist_url = title_element.get('href') if title_element else ''
                    
                    # Extract playlist_id from URL
                    playlist_id = ''
                    if playlist_url:
                        match = re.search(r'\.([A-Za-z0-9]+)\.html$', playlist_url)
                        if match:
                            playlist_id = match.group(1)
                        else:
                            print(f"Không thể lấy playlist_id từ URL: {playlist_url}")
                            continue
                    
                    # Scrape songs in the playlist/collection
                    songs = []
                    if playlist_url and playlist_id:
                        songs = scrape_playlist_songs(playlist_url)
                        if songs:
                            if type == 'collection':
                                save_collection_songs_to_csv(songs, playlist_id, category, subcategory)
                            else:
                                save_playlist_songs_to_csv(songs, playlist_id, category, subcategory)
                    
                    items.append({
                        'title': title,
                        'artists': artists,
                        'img_url': img_url,
                        'playlist_url': playlist_url,
                        'playlist_id': playlist_id,
                        'song_count': len(songs),
                        'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    print(f"Scraped item: {title} (ID: {playlist_id})")
            except Exception as e:
                print(f"Error processing an item: {e}")
                continue

        if not items:
            print(f"No items scraped for {subcategory}. Check HTML structure or selectors.")
        return items

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    
def scrape_playlist_songs(playlist_url):
    """
    Scrape songs from a specific playlist URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print(f"Fetching playlist URL: {playlist_url}")
        time.sleep(1)  # Add 1-second delay
        response = requests.get(playlist_url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Response status: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        song_items = soup.select('ul.list_song_in_album li')

        if not song_items:
            print(f"No songs found with selector 'ul.list_song_in_album li'. Trying alternative selector.")
            song_items = soup.select('li.alternate')

        print(f"Found {len(song_items)} songs in playlist")

        songs = []
        for index, item in enumerate(song_items, 1):
            try:
                title_meta = item.find('meta', itemprop='name')
                link_meta = item.find('meta', itemprop='url')
                if title_meta and link_meta:
                    title = title_meta['content'].strip()
                    song_url = link_meta['content'].strip()
                else:
                    title_element = item.select_one('.name_song')
                    if not title_element:
                        print(f"Skipping item {index}: No title found")
                        continue
                    title = title_element.text.strip() or 'Unknown Title'
                    song_url = title_element.get('href', '')

                if not song_url:
                    print(f"Skipping item {index}: No song URL found for {title}")
                    continue

                singers_elements = item.select('.name_singer')
                artists = ', '.join([singer.text.strip() for singer in singers_elements]) if singers_elements else 'Unknown Artist'

                img_url = 'https://stc-id.nixcdn.com/v11/images/avatar_default.jpg'

                try:
                    song_response = requests.get(song_url, headers=headers, timeout=10)
                    song_response.raise_for_status()
                    song_soup = BeautifulSoup(song_response.text, 'html.parser')

                    if song_soup.find(string="Nội dung bị đóng theo yêu cầu của đơn vị chủ sở hữu bản quyền."):
                        print(f"Skipping copyrighted song: {title} - {song_url}")
                        continue

                    img_element = song_soup.select_one('.box_info_field img')
                    if img_element:
                        img_url = img_element.get('data-src') or img_element.get('src') or img_url

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching song page {song_url}: {e}")
                    continue

                songs.append({
                    'rank': str(index),
                    'title': title,
                    'artists': artists,
                    'img_url': img_url,
                    'song_url': song_url,
                    'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f"Scraped song: {title} - {artists}")
            except Exception as e:
                print(f"Error processing song {index}: {e}")
                continue

        if not songs:
            print(f"No songs scraped for playlist {playlist_url}. Check HTML structure or selectors.")
        return songs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {playlist_url}: {e}")
        return []

def save_playlist_songs_to_csv(songs, playlist_id, category, subcategory):
    """
    Save the scraped playlist songs to a CSV file in the appropriate subdirectory.
    """
    directory = os.path.join('data', 'playlist', category, subcategory)
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, f"songs_playlist_{playlist_id}.csv")
    
    fieldnames = ['rank', 'title', 'artists', 'img_url', 'song_url', 'date_scraped']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for song in songs:
            writer.writerow({field: str(song.get(field, '')) for field in fieldnames})

    print(f"Saved {len(songs)} songs to {filename}")
    return filename

def save_collection_songs_to_csv(songs, playlist_id, category, subcategory):
    """
    Save the scraped collection songs to a CSV file in the appropriate subdirectory.
    """
    directory = os.path.join('data', 'collection', category, subcategory)
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, f"songs_collection_{playlist_id}.csv")
    
    fieldnames = ['rank', 'title', 'artists', 'img_url', 'song_url', 'date_scraped']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for song in songs:
            writer.writerow({field: str(song.get(field, '')) for field in fieldnames})

    print(f"Saved {len(songs)} songs to {filename}")
    return filename

def save_to_csv(items, type, category, subcategory):
    directory = os.path.join('data', type, category)
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, f"items_{type}_{category}_{subcategory}.csv")
    
    if type == 'collection':
        fieldnames = ['title', 'artists', 'img_url', 'playlist_url', 'playlist_id', 'song_count', 'date_scraped']
    elif type == 'playlist':
        fieldnames = ['title', 'artists', 'img_url', 'playlist_url', 'playlist_id', 'song_count', 'date_scraped']
    else:
        fieldnames = ['rank', 'title', 'artists', 'img_url', 'song_url', 'date_scraped']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow({field: str(item.get(field, '')) for field in fieldnames})

    print(f"Saved {len(items)} items to {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) == 4:
        type, category, subcategory = sys.argv[1], sys.argv[2], sys.argv[3]
        print(f"Scraping {type} - {category} - {subcategory}...")
        items = scrape_nhaccuatui(type, category, subcategory)
        if items:
            csv_file = save_to_csv(items, type, category, subcategory)
            print(f"Successfully scraped {len(items)} items and saved to {csv_file}")
        else:
            print(f"No items were scraped for {subcategory}.")
    else:
        print("No specific arguments provided. Please provide type, category, and subcategory.")
        print("Usage: python nhaccuatui_scraper.py <type> <category> <subcategory>")
        sys.exit(1)
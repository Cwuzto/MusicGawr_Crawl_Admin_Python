import requests
import xml.etree.ElementTree as ET
import re

def extract_mp3_url_from_html(song_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": song_url,
        "Accept": "audio/mpeg, audio/*; q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    try:
        session = requests.Session()
        html_response = session.get(song_url, headers=headers)
        html = html_response.text

        match = re.search(r'player\.peConfig\.xmlURL\s*=\s*"([^"]+)"', html)
        if not match:
            print("Không tìm thấy XML URL trong HTML.")
            return None, "Không tìm thấy XML URL"

        xml_url = match.group(1)
        print(f"🔗 XML URL: {xml_url}")

        xml_response = session.get(xml_url, headers=headers)
        if xml_response.status_code != 200:
            print(f"Lỗi khi tải XML ({xml_response.status_code})")
            return None, f"Lỗi khi tải XML ({xml_response.status_code})"

        xml_data = xml_response.text
        root = ET.fromstring(xml_data)
        location = root.find(".//location")
        if location is not None:
            mp3_url = location.text
            print(f"Link MP3: {mp3_url}")
            mp3_response = session.get(mp3_url, headers=headers, stream=True)
            if mp3_response.status_code == 200:
                content_type = mp3_response.headers.get("Content-Type", "")
                if "audio/mpeg" in content_type:
                    return mp3_url, None
                else:
                    return None, f"MIME type không hợp lệ: {content_type}"
            else:
                return None, f"Không thể truy cập MP3: {mp3_response.status_code}"
        else:
            return None, "Không tìm thấy link MP3 trong XML"

    except requests.RequestException as e:
        return None, f"Lỗi khi gửi yêu cầu HTTP: {str(e)}"
    except Exception as e:
        return None, f"Lỗi không xác định: {str(e)}"
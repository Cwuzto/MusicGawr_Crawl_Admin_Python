from flask import Flask, Response, jsonify, render_template, request, send_file
import subprocess
import os
import time
import pandas as pd
import numpy as np
import requests
from mp3_extractor import extract_mp3_url_from_html

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    """Hiển thị trang admin"""
    return render_template('/templates/admin_page.html')

@app.route('/api/songs')
def get_songs():
    """API để lấy danh sách bài hát hoặc playlist từ file CSV"""
    try:
        type = request.args.get('type')
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        csv_file = os.path.join('data', type, category, f"items_{type}_{category}_{subcategory}.csv")

        if not os.path.exists(csv_file):
            return jsonify({"error": "Không tìm thấy file CSV", "data": []})

        df = pd.read_csv(csv_file)
        df = df.replace({np.nan: ''})
        if type == 'collection' and 'playlist_url' in df.columns:
            df['song_url'] = df['playlist_url']
            df['artists'] = df.get('artists', '')
        return jsonify({"data": df.to_dict('records')})
    except Exception as e:
        return jsonify({"error": str(e), "data": []})
    
@app.route('/api/playlist-songs')
def get_playlist_songs():
    """API để lấy danh sách bài hát từ một playlist"""
    try:
        playlist_id = request.args.get('playlist_id')
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        csv_file = os.path.join('data', 'playlist', category, subcategory, f"songs_playlist_{playlist_id}.csv")

        if not os.path.exists(csv_file):
            return jsonify({"error": "Không tìm thấy file CSV cho playlist này", "data": []})

        df = pd.read_csv(csv_file)
        df = df.replace({np.nan: ''})
        return jsonify({"data": df.to_dict('records')})
    except Exception as e:
        return jsonify({"error": str(e), "data": []})

@app.route('/api/collection-songs')
def get_collection_songs():
    """API để lấy danh sách bài hát từ một collection"""
    try:
        playlist_id = request.args.get('playlist_id')
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        csv_file = os.path.join('data', 'collection', category, subcategory, f"songs_collection_{playlist_id}.csv")

        if not os.path.exists(csv_file):
            return jsonify({"error": "Không tìm thấy file CSV cho collection này", "data": []})

        df = pd.read_csv(csv_file)
        df = df.replace({np.nan: ''})
        return jsonify({"data": df.to_dict('records')})
    except Exception as e:
        return jsonify({"error": str(e), "data": []})

@app.route('/api/scrape', methods=['POST'])
def scrape_data():
    """API để chạy script scraper"""
    try:
        data = request.get_json()
        type = data.get('type')
        category = data.get('category')
        subcategory = data.get('subcategory')

        result = subprocess.run(
            ['python', 'nhaccuatui_scraper.py', type, category, subcategory],
            capture_output=True,
            text=True,
            check=True
        )

        if "Successfully scraped" in result.stdout:
            return jsonify({"success": True, "message": result.stdout})
        else:
            return jsonify({"success": False, "message": "Cào dữ liệu không thành công", "details": result.stdout})

    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "message": "Lỗi khi chạy script", "details": e.stderr})
    except Exception as e:
        return jsonify({"success": False, "message": "Lỗi: " + str(e)})

@app.route('/api/export-csv')
def export_csv():
    """API để tải xuống file CSV"""
    try:
        type = request.args.get('type')
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        playlist_id = request.args.get('playlist_id')

        if type == 'playlist_songs' and playlist_id and category and subcategory:
            csv_file = os.path.join('data', 'playlist', category, subcategory, f"songs_playlist_{playlist_id}.csv")
        elif type == 'collection_songs' and playlist_id and category and subcategory:
            csv_file = os.path.join('data', 'collection', category, subcategory, f"songs_collection_{playlist_id}.csv")
        else:
            csv_file = os.path.join('data', type, category, f"items_{type}_{category}_{subcategory}.csv")

        if not os.path.exists(csv_file):
            return jsonify({"error": "Không tìm thấy file CSV"}), 404

        download_name = f'nhaccuatui_{type}_{category}_{subcategory}_{int(time.time())}.csv'
        if type == 'playlist_songs':
            download_name = f'nhaccuatui_playlist_songs_{playlist_id}_{int(time.time())}.csv'
        elif type == 'collection_songs':
            download_name = f'nhaccuatui_collection_songs_{playlist_id}_{int(time.time())}.csv'

        return send_file(
            csv_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name=download_name
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get-mp3")
def get_mp3_api():
    song_url = request.args.get("song_url")
    print(f"Received song_url: {song_url}")
    if not song_url:
        return jsonify({"error": "Vui lòng cung cấp song_url"}), 400

    mp3_url, error = extract_mp3_url_from_html(song_url)
    print(f"MP3 URL: {mp3_url}")
    print(f"Error: {error}")

    if mp3_url:
        return jsonify({"mp3_url": mp3_url})
    else:
        return jsonify({"error": error or "Không thể lấy link MP3"}), 404

@app.route("/proxy-mp3")
def proxy_mp3():
    mp3_url = request.args.get("mp3_url")
    if not mp3_url:
        return jsonify({"error": "Vui lòng cung cấp mp3_url"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": "https://www.nhaccuatui.com/",
        "Accept": "audio/mpeg, audio/*; q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    try:
        session = requests.Session()
        mp3_response = session.get(mp3_url, headers=headers, stream=True)
        
        if mp3_response.status_code == 200:
            def generate():
                for chunk in mp3_response.iter_content(chunk_size=8192):
                    yield chunk
            return Response(generate(), content_type=mp3_response.headers.get("Content-Type", "audio/mpeg"))
        else:
            return jsonify({"error": f"Không thể truy cập MP3: {mp3_response.status_code}"}), mp3_response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Lỗi khi gửi yêu cầu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
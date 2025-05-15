from flask import Flask, jsonify, render_template, request, send_file
import subprocess
import os
import time
import pandas as pd

app = Flask(__name__, template_folder='.')

# Đường dẫn đến tệp CSV
CSV_FILE = 'nhaccuatui_top100.csv'
SCRAPER_FILE = 'nhaccuatui_scraper.py'

@app.route('/')
def index():
    """Hiển thị trang admin"""
    return render_template('admin_page.html')

@app.route('/api/songs')
def get_songs():
    """API để lấy danh sách bài hát từ file CSV"""
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({"error": "Không tìm thấy file CSV", "data": []})
        
        df = pd.read_csv(CSV_FILE)
        return jsonify({"data": df.to_dict('records')})
    except Exception as e:
        return jsonify({"error": str(e), "data": []})

@app.route('/api/scrape', methods=['POST'])
def scrape_data():
    """API để chạy script scraper"""
    try:
        # Chạy script scraper bằng subprocess
        result = subprocess.run(['python', SCRAPER_FILE], 
                               capture_output=True, 
                               text=True, 
                               check=True)
        
        # Kiểm tra kết quả
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
        if not os.path.exists(CSV_FILE):
            return jsonify({"error": "Không tìm thấy file CSV"}), 404
        
        # Trả về file CSV để tải xuống
        return send_file(CSV_FILE, 
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'nhaccuatui_top100_{int(time.time())}.csv')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, render_template, request, send_file, jsonify
from flask_bootstrap import Bootstrap
import pandas as pd
import uuid
import os
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

def generate_sample_data(uuid_str):
    """生成與 UUID 相關的示例數據"""
    data1 = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 5,
        'value': [uuid.uuid4().int % 1000 for _ in range(5)],
        'category': ['A', 'B', 'C', 'D', 'E']
    }
    
    data2 = {
        'id': [uuid.uuid4().hex[:8] for _ in range(3)],
        'status': ['active', 'pending', 'completed'],
        'score': [85, 92, 78]
    }
    
    data3 = {
        'date': [datetime.now().strftime('%Y-%m-%d')] * 4,
        'amount': [1000, 2000, 3000, 4000],
        'type': ['income', 'expense', 'income', 'expense']
    }
    
    return data1, data2, data3

def create_csv_files(uuid_str):
    """創建 CSV 檔案並返回檔案路徑"""
    # 創建下載目錄
    download_dir = 'downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # 生成示例數據
    data1, data2, data3 = generate_sample_data(uuid_str)
    
    # 創建 DataFrame 並保存為 CSV
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    
    # 生成檔案名稱
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename1 = f'data1_{uuid_str[:8]}_{timestamp}.csv'
    filename2 = f'data2_{uuid_str[:8]}_{timestamp}.csv'
    filename3 = f'data3_{uuid_str[:8]}_{timestamp}.csv'
    
    # 保存 CSV 檔案
    df1.to_csv(os.path.join(download_dir, filename1), index=False)
    df2.to_csv(os.path.join(download_dir, filename2), index=False)
    df3.to_csv(os.path.join(download_dir, filename3), index=False)
    
    return filename1, filename2, filename3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        uuid_str = request.form['uuid']
        # 驗證 UUID 格式
        uuid_obj = uuid.UUID(uuid_str)
        
        # 創建 CSV 檔案
        file1, file2, file3 = create_csv_files(uuid_str)
        
        return jsonify({
            'success': True,
            'files': [file1, file2, file3],
            'message': '檔案生成成功！'
        })
    except ValueError:
        return jsonify({
            'success': False,
            'message': '無效的 UUID 格式'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'發生錯誤：{str(e)}'
        })

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join('downloads', filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'下載失敗：{str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 
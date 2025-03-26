import uuid
import pandas as pd
import os
from datetime import datetime

def generate_sample_data(uuid_str):
    """生成與 UUID 相關的示例數據"""
    # 生成一些隨機數據
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

def download_csv_files(uuid_str):
    """根據 UUID 生成並下載三個相關的 CSV 檔案"""
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
    filename1 = f'{download_dir}/data1_{uuid_str[:8]}_{timestamp}.csv'
    filename2 = f'{download_dir}/data2_{uuid_str[:8]}_{timestamp}.csv'
    filename3 = f'{download_dir}/data3_{uuid_str[:8]}_{timestamp}.csv'
    
    # 保存 CSV 檔案
    df1.to_csv(filename1, index=False)
    df2.to_csv(filename2, index=False)
    df3.to_csv(filename3, index=False)
    
    return filename1, filename2, filename3

def main():
    print("歡迎使用 UUID CSV 檔案下載器！")
    while True:
        uuid_str = input("請輸入 UUID（或輸入 'q' 退出）: ")
        if uuid_str.lower() == 'q':
            break
            
        try:
            # 驗證 UUID 格式
            uuid_obj = uuid.UUID(uuid_str)
            print(f"\n正在處理 UUID: {uuid_str}")
            
            # 下載檔案
            file1, file2, file3 = download_csv_files(uuid_str)
            
            print("\n檔案已成功生成：")
            print(f"1. {file1}")
            print(f"2. {file2}")
            print(f"3. {file3}")
            print("\n檔案已保存在 'downloads' 目錄中")
            
        except ValueError:
            print("錯誤：無效的 UUID 格式，請重新輸入")
        except Exception as e:
            print(f"發生錯誤：{str(e)}")

if __name__ == "__main__":
    main() 
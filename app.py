from flask import Flask, render_template, request, send_file, jsonify
from flask_bootstrap import Bootstrap
import pandas as pd
import uuid
import os
from datetime import datetime
import re
import json

app = Flask(__name__)
Bootstrap(app)

def extract_uuid(text):
    """從文本中提取 UUID"""
    # UUID 的正則表達式模式
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    match = re.search(uuid_pattern, text, re.IGNORECASE)
    if match:
        try:
            # 驗證 UUID 格式
            uuid_obj = uuid.UUID(match.group(0))
            return str(uuid_obj)
        except ValueError:
            return None
    return None

def clean_uuid(uuid_str):
    """清理並驗證 UUID 格式"""
    try:
        # 去除前後空格
        cleaned = uuid_str.strip()
        # 驗證 UUID 格式
        uuid_obj = uuid.UUID(cleaned)
        return str(uuid_obj)
    except ValueError:
        return None

def generate_sample_data(store_uuids, client_id):
    """生成與 Store UUID 和 Client ID 相關的示例數據"""
    # 從每行文本中提取 UUID
    valid_uuids = []
    for line in store_uuids:
        # 先嘗試直接清理
        cleaned = clean_uuid(line)
        if cleaned:
            valid_uuids.append(cleaned)
        else:
            # 如果直接清理失敗，嘗試提取
            extracted = extract_uuid(line)
            if extracted:
                valid_uuids.append(extracted)
    
    if not valid_uuids:
        raise ValueError("沒有找到有效的 UUID")
    
    # 第一個檔案：簡單的 storeUUID 和 clientID 對應
    data1 = {
        'storeUUID': valid_uuids,
        'clientID': [client_id] * len(valid_uuids)
    }
    
    # 第二個檔案：Remove Legacy Config 格式
    data2 = {
        'storeUUID': valid_uuids,
        'posTypes': ['UBER_API'] * len(valid_uuids),
        'removeDevUserWithOrderWebhook': ['TRUE'] * len(valid_uuids)
    }
    
    # 第三個檔案：Update store tag 格式
    data3 = {
        'storeUUID': valid_uuids,
        'actionType': ['remove'] * len(valid_uuids),
        'tagNames': ['menu_editor_blacklist'] * len(valid_uuids)
    }
    
    return data1, data2, data3

def create_csv_files(store_uuids, client_id):
    """創建 CSV 檔案並返回檔案路徑"""
    # 創建下載目錄
    download_dir = 'downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # 生成示例數據
    data1, data2, data3 = generate_sample_data(store_uuids, client_id)
    
    # 創建 DataFrame 並保存為 CSV
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    
    # 生成檔案名稱
    timestamp = datetime.now().strftime('%Y%m%d')
    filename1 = f'Remove_vnext_{timestamp}.csv'
    filename2 = f'Remove_Legacy_Config_{timestamp}.csv'
    filename3 = f'Update_store_tag(menu_blacklist_removed)_{timestamp}.csv'
    
    # 保存 CSV 檔案，使用 lineterminator='\n' 來避免最後的空行
    df1.to_csv(os.path.join(download_dir, filename1), index=False, lineterminator='\n')
    df2.to_csv(os.path.join(download_dir, filename2), index=False, lineterminator='\n')
    df3.to_csv(os.path.join(download_dir, filename3), index=False, lineterminator='\n')
    
    return filename1, filename2, filename3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_vnext')
def remove_vnext():
    return render_template('remove_vnext.html')

@app.route('/subway_staging')
def subway_staging():
    return render_template('subway_staging.html')

@app.route('/mcd_staging')
def mcd_staging():
    return render_template('mcd_staging.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        store_uuids = data.get('storeUUIDs', [])
        client_id = data.get('clientID', '').strip()
        
        if not store_uuids:
            return jsonify({
                'success': False,
                'message': '請至少輸入一個 Store UUID'
            })
            
        if not client_id:
            return jsonify({
                'success': False,
                'message': '請輸入 Client ID'
            })
        
        # 創建 CSV 檔案
        file1, file2, file3 = create_csv_files(store_uuids, client_id)
        
        return jsonify({
            'success': True,
            'files': [file1, file2, file3],
            'message': '檔案生成成功！'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'發生錯誤：{str(e)}'
        })

@app.route('/generate_subway', methods=['POST'])
def generate_subway():
    try:
        data = request.get_json()
        country = data.get('country')
        store_pairs = data.get('storePairs', [])
        
        if not country:
            return jsonify({
                'success': False,
                'message': '請選擇國家'
            })
            
        if not store_pairs:
            return jsonify({
                'success': False,
                'message': '請至少輸入一組 Store UUID'
            })
        
        # 驗證 Store UUID 格式
        valid_store_pairs = []
        for pair in store_pairs:
            store_uuid = pair.get('storeUUID', '').strip()
            partner_id = pair.get('partnerID', '')  # 先獲取原始值
            
            # 驗證 UUID 格式
            try:
                uuid_obj = uuid.UUID(store_uuid)
                store_uuid = str(uuid_obj)
            except ValueError:
                continue
            
            # 處理 partnerID
            partner_id = partner_id.strip() if partner_id else ''
            
            valid_store_pairs.append({
                'storeUUID': store_uuid,
                'partnerID': partner_id if partner_id else None
            })
        
        if not valid_store_pairs:
            return jsonify({
                'success': False,
                'message': '沒有有效的 Store UUID'
            })
        
        # 創建下載目錄
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d')
        filenames = []
        
        # 1. vNEXT config CSV
        vnext_data = []
        for pair in valid_store_pairs:
            store_uuid = pair['storeUUID']
            partner_id = pair['partnerID']
            
            # 處理 Partner ID
            merchant_store_id = ''
            if partner_id:
                # 檢查是否為五位數字或五位數字加上 -0
                if (partner_id.isdigit() and len(partner_id) == 5) or \
                   (partner_id.endswith('-0') and len(partner_id) == 7 and partner_id[:-2].isdigit()):
                    merchant_store_id = partner_id if partner_id.endswith('-0') else f"{partner_id}-0"
            
            # 根據國家選擇 clientID
            client_id = 'Dk2OuDDnZYTJsfITCdYVKx_Vd_EhPD2X' if country == 'NZ' else 'hhPwU9UicO1rnSutuaj9VJtEWMdIl_3C'
            
            # 創建一行數據
            row = {
                'storeUUID': store_uuid,
                'isOrderManager': 'TRUE',
                'clientID': client_id,
                'storeConfigurationData': '',
                'externalIntegratorID': '',
                'externalBrandID': '',
                'merchantStoreID': merchant_store_id,
                'overrideReason': '',
                'enableIntegration': 'TRUE',
                'enableOrderRelease': 'FALSE',
                'enablePOSDenyCancellations': 'TRUE',
                'enableAutoAccept': '',
                'enableRDAcceptBeforePosInjection': '',
                'enableRDOptional': '',
                'forceOrderReleaseInSeconds': '',
                'internalTags': '',
                'storeTags': '"pos_api_order,pos_api_menu,pos_provider_subway_anz"',
                'isVisible': 'TRUE',
                'allowSingleUseItemOptOut': 'FALSE',
                'isAllergenFriendlinessEligible': '',
                'requireSyncedMenu': '',
                'preserveCurrentOrderConfig': '',
                'apiVersion': '',
                'acceptScheduledOrderEnabled': '',
                'enableDeliveryStatusTracking': '',
                'skipProvisioningWebhook': ''
            }
            vnext_data.append(row)
        
        # 2. Item and Order Instruction CSV
        instruction_data = []
        for pair in valid_store_pairs:
            instruction_data.append({
                'storeUUID': pair['storeUUID'],
                'disableOrderInstructions': 'FALSE',
                'disableItemInstructions': 'TRUE'
            })
        
        # 3. Operating Hours CSV
        operating_hours_data = []
        for pair in valid_store_pairs:
            operating_hours_data.append({
                'storeUUID': pair['storeUUID'],
                'overrideType': 'LAST_ORDER_BUFFER',
                'overrideValue': '30',
                'days': ''
            })
        
        # 4. Subway Store Tags CSV
        store_tags_data = []
        for pair in valid_store_pairs:
            store_tags_data.append({
                'storeUUID': pair['storeUUID'],
                'actionType': 'add',
                'tagNames': '"rd_hide_menu_availability,rd_price_hide_adjust,ue_rx_rd_suppress_order_chimes"'
            })
        
        # 生成檔案名稱
        filename1 = f'vNEXT_config_{country}_{timestamp}.csv'
        filename2 = f'item_and_order_instruction_{country}_{timestamp}.csv'
        filename3 = f'operating_hours_{country}_{timestamp}.csv'
        filename4 = f'subway_store_tags_{country}_{timestamp}.csv'
        
        # 保存所有 CSV 檔案
        pd.DataFrame(vnext_data).to_csv(os.path.join(download_dir, filename1), index=False, lineterminator='\n')
        pd.DataFrame(instruction_data).to_csv(os.path.join(download_dir, filename2), index=False, lineterminator='\n')
        pd.DataFrame(operating_hours_data).to_csv(os.path.join(download_dir, filename3), index=False, lineterminator='\n')
        pd.DataFrame(store_tags_data).to_csv(os.path.join(download_dir, filename4), index=False, lineterminator='\n')
        
        return jsonify({
            'success': True,
            'files': [filename1, filename2, filename3, filename4],
            'message': '檔案生成成功！'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'發生錯誤：{str(e)}'
        })

@app.route('/generate_mcd', methods=['POST'])
def generate_mcd():
    try:
        data = request.get_json()
        country = data.get('country')
        store_uuids = data.get('storeUUIDs', [])
        
        if not country:
            return jsonify({
                'success': False,
                'message': '請選擇國家'
            })
            
        if not store_uuids:
            return jsonify({
                'success': False,
                'message': '請至少輸入一個 Store UUID'
            })
        
        # 驗證 Store UUID 格式
        valid_uuids = []
        for uuid_str in store_uuids:
            try:
                # 清理並驗證 UUID
                cleaned = clean_uuid(uuid_str)
                if cleaned:
                    valid_uuids.append(cleaned)
            except ValueError:
                continue
        
        if not valid_uuids:
            return jsonify({
                'success': False,
                'message': '沒有有效的 Store UUID'
            })
        
        # 創建下載目錄
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d')
        
        # 生成檔案名稱
        filename1 = f'vNext_MCD_MENU_{timestamp}.csv'
        filename2 = f'vNext_MCD_{country}_{timestamp}.csv'
        
        # 準備第一個 CSV 數據
        menu_data = []
        for store_uuid in valid_uuids:
            row = {
                'storeUUID': store_uuid,
                'isOrderManager': 'FALSE',
                'clientID': 'fPfDEQxws8cheEUBASpMnuBLcI1f_5iZ',
                'storeConfigurationData': '',
                'externalIntegratorID': '',
                'externalBrandID': '',
                'merchantStoreID': '',
                'overrideReason': 'stage to have menu user',
                'enableIntegration': 'FALSE',
                'enableOrderRelease': 'FALSE',
                'enablePOSDenyCancellations': 'FALSE',
                'enableAutoAccept': 'FALSE',
                'enableRDAcceptBeforePosInjection': 'FALSE',
                'enableRDOptional': 'FALSE',
                'forceOrderReleaseInSeconds': '',
                'internalTags': '',
                'storeTags': '',
                'isVisible': '',
                'allowSingleUseItemOptOut': '',
                'isAllergenFriendlinessEligible': '',
                'requireSyncedMenu': '',
                'preserveCurrentOrderConfig': '',
                'apiVersion': '',
                'acceptScheduledOrderEnabled': '',
                'enableDeliveryStatusTracking': '',
                'skipProvisioningWebhook': ''
            }
            menu_data.append(row)
        
        # 準備第二個 CSV 數據
        config_data = []
        for store_uuid in valid_uuids:
            # 根據國家設置不同的配置
            config = {
                'client_id': 'auubereatshahajhdsfusbdau',
                'isMenuV2': 'TRUE',
                'market_id': country,
                'posType': 'MCD',
                'timeZone': '',
                'urlprefix': 'https://ap-vendor.api.mcd.com',
                'organization': 'mcd-apac',
                'posStoreId': store_uuid
            }
            
            row = {
                'storeUUID': store_uuid,
                'isOrderManager': 'TRUE',
                'clientID': 'sq2EuRvkQUBpmh6QkAH-sfktPCdFyupP',
                'storeConfigurationData': json.dumps(config),
                'externalIntegratorID': '',
                'externalBrandID': '',
                'merchantStoreID': '',
                'overrideReason': 're-stage to have vNEXT',
                'enableIntegration': 'TRUE',
                'enableOrderRelease': 'TRUE',
                'enablePOSDenyCancellations': 'FALSE',
                'enableAutoAccept': 'FALSE',
                'enableRDAcceptBeforePosInjection': 'FALSE',
                'enableRDOptional': 'TRUE',
                'forceOrderReleaseInSeconds': '',
                'internalTags': '',
                'storeTags': '',
                'isVisible': 'TRUE',
                'allowSingleUseItemOptOut': '',
                'isAllergenFriendlinessEligible': '',
                'requireSyncedMenu': '',
                'preserveCurrentOrderConfig': '',
                'apiVersion': '',
                'acceptScheduledOrderEnabled': '',
                'enableDeliveryStatusTracking': '',
                'skipProvisioningWebhook': ''
            }
            config_data.append(row)
        
        # 保存 CSV 檔案
        pd.DataFrame(menu_data).to_csv(os.path.join(download_dir, filename1), index=False, lineterminator='\n')
        pd.DataFrame(config_data).to_csv(os.path.join(download_dir, filename2), index=False, lineterminator='\n')
        
        return jsonify({
            'success': True,
            'files': [filename1, filename2],
            'message': '檔案生成成功！'
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
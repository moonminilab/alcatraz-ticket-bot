import urllib.request
import urllib.parse
import json
import time
import os
from datetime import datetime

# 從環境變數讀取設定
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
CHECK_DATE = '2025-08-01'  # 要監控的日期

def send_telegram(message):
    """發送Telegram訊息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data_encoded, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("✅ Telegram訊息發送成功")
                return True
            else:
                print(f"❌ Telegram API回傳狀態: {response.status}")
                return False
                
    except Exception as e:
        print(f"❌ 發送Telegram訊息失敗: {e}")
        return False

def check_alcatraz_tickets():
    """檢查Alcatraz票券是否有空位"""
    try:
        print("🌐 正在檢查Alcatraz網站...")
        
        # 要檢查的網址
        urls_to_check = [
            'https://www.alcatrazcruises.com/tickets/',
            'https://www.alcatrazcruises.com/',
        ]
        
        # 模擬iPhone瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        
        for url in urls_to_check:
            try:
                print(f"🔍 檢查中: {url}")
                
                req = urllib.request.Request(url)
                for key, value in headers.items():
                    req.add_header(key, value)
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status == 200:
                        content = response.read().decode('utf-8', errors='ignore').lower()
                        
                        # 日期關鍵字
                        date_indicators = [
                            CHECK_DATE, "august 1", "aug 1", "8/1/2025", "08/01/2025", "2025-08-01"
                        ]
                        
                        # 有票關鍵字
                        availability_indicators = [
                            "available", "book now", "select time", "choose departure", "purchase", "buy tickets"
                        ]
                        
                        # 售完關鍵字
                        sold_out_indicators = [
                            "sold out", "no tickets available", "fully booked", "unavailable", "no availability"
                        ]
                        
                        date_found = any(indicator in content for indicator in date_indicators)
                        availability_found = any(indicator in content for indicator in availability_indicators)
                        sold_out = any(indicator in content for indicator in sold_out_indicators)
                        
                        print(f"📊 分析結果: 日期={date_found}, 有票={availability_found}, 售完={sold_out}")
                        
                        if date_found and availability_found and not sold_out:
                            message = f"🎟️ Alcatraz {CHECK_DATE} 有票了！\n\n📅 日期: 2025年8月1日\n🔗 訂票網址: {url}\n\n⏰ 發現時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n請盡快到網站確認並訂票！"
                            print("✅ 發現有票！")
                            send_telegram(message)
                            return True
                        
            except Exception as e:
                print(f"⚠️ 檢查 {url} 時發生錯誤: {e}")
                continue
        
        print("❌ 目前沒有票券")
        return False
        
    except Exception as e:
        error_msg = f"⚠️ 錯誤: {str(e)}"
        print(error_msg)
        send_telegram(f"🚨 機器人錯誤: {error_msg}")
        return False

def main():
    """主程式迴圈"""
    print(f"🤖 開始監控 {CHECK_DATE} 的Alcatraz票券")
    send_telegram(f"🤖 iPhone Alcatraz監控機器人已啟動！\n📅 監控日期: {CHECK_DATE}\n⏰ 檢查間隔: 1小時\n\n機器人會24小時自動監控，一有票就通知你！")
    
    while True:
        try:
            print(f"🔍 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 開始檢查")
            
            success = check_alcatraz_tickets()
            
            if success:
                print("🎉 發現票券！繼續監控...")
                
        except KeyboardInterrupt:
            print("🛑 機器人停止")
            send_telegram("🛑 監控機器人已停止")
            break
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        print("😴 休息1小時後繼續檢查...")
        time.sleep(3600)  # 3600秒 = 1小時

if __name__ == "__main__":
    main()

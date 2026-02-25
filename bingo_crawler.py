import os, json, time, requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def send_tg(msg):
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    if not token or not chat_id: return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try: requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=15)
    except: pass

def run_crawler():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_history = {}
    try:
        for i in range(5):
            d = datetime.now() - timedelta(days=i)
            date_str, date_key = d.strftime('%Y-%m-%d'), d.strftime('%Y%m%d')
            driver.get(f"https://winwin.tw/Bingo?date={date_str}")
            time.sleep(10)
            rows = driver.find_elements(By.TAG_NAME, "tr")
            day_data = []
            for row in rows:
                txt = row.text
                if ":" in txt and len(txt) > 40:
                    parts = txt.split()
                    if len(parts) >= 22:
                        day_data.append({"issue": parts[0], "time": parts[1], "h": int(parts[1].split(':')[0]), "nums": parts[2:22]})
            all_history[date_key] = day_data
        with open('bingo_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_history, f, ensure_ascii=False, indent=4)
        send_tg(f"✅ <b>BINGO 雲端 5 日備份完成</b>\n更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    finally: driver.quit()

if __name__ == "__main__":
    run_crawler()

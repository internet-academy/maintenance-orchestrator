
import os
import requests
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

TRANSLATIONS = {
    "MD_SD-1249": {
        "en": "Request to change the first session date for Riho Kano.
- Before: 20250201 12:00
- After: 20260201 12:00

Kikuichi URL: https://www.internetacademy.jp/mem/admins/contract/241731?list=1",
        "jp": "加納梨穂さまの初回日の変更をお願いできませんでしょうか。
変更前：20250201 1200
変更後：20260201 1200

▼菊一URL：https://www.internetacademy.jp/mem/admins/contract/241731?list=1"
    },
    "MD_SD-1250": {
        "en": "Possible issue with exam time limits in Corporate LMS. Even if set to 30 mins, some students (e.g., Yuya Imasu) are seeing longer times (37m 59s) or actual test time differs from displayed time. 
Admin Account ID: b3724u0126
Imasu's Personal Account ID: b3724u0129",
        "jp": "法人LMSの本試験の制限時間を30分に設定していても、30分以上かけてテストを実施できている可能性がある。もしくは、実際に受験した時間とLMSに表示される回答時間が違う可能性がある。ご確認お願いいたします。
管理者アカウント　ID ：b3724u0126
井桝様ご本人のアカウント　ID ：b3724u0129"
    },
    "MD_SD-1251": {
        "en": "Request regarding daily report line breaks in LMS for Mitsubishi Motors training. Currently, line breaks entered by students are lost and displayed as a single paragraph. Please ensure formatting is preserved in the confirmation screen.",
        "jp": "受講生の入力した改行が、確認画面でも同様に確認できるようにしてほしいというご要望でございます。現在は改行が無くなって１つのパラグラフで表示されています。"
    },
    "MD_SD-1252": {
        "en": "Web Creator Certification guide page is not displaying correctly, preventing students from applying. 
Target Page: https://www.internetacademy.jp/bohr/guide09",
        "jp": "【結論】Webクリエイター認定試験のご案内ページが正しく表示されない為、不具合の解消をお願いできますでしょうか。こちらが見れないとWebクリの申し込みができない為、早めのご対応を御願い致します。"
    },
    "MD_SD-1253": {
        "en": "Issue with feedback sheets being submitted with '0 0 0' ratings. Submissions should be blocked unless star ratings are provided. Example cases for Takahashi Mio and Asano Kaoru provided in original text.",
        "jp": "感想シートの評価が「0 0 0」の状態で投稿されております。本来、星マークの評価をつけないと投稿できないはずなので修正をお願いいたします。"
    },
    "MD_SD-1254": {
        "en": "Abnormal behavior in the lesson reservation form when 'Field of Interest' is not selected. 
1. Error claiming time slots are full even when available. 
2. 'Unexpected error' message displayed despite successful conversion. 
Target: https://www.internetacademy.jp/lesson/",
        "jp": "【報告・相談】「興味がある分野」未選択時のフォーム動作異常について。①予約時間帯エラー(空いているのに埋まっていると表示)、②予期せぬエラー(表示されるがCVは通る)の不具合が発生しています。"
    },
    "MD_SD-1255": {
        "en": "Incorrect course name displayed on Enrollment Certificates in Kikuichi. It should show 'SNS Marketing for Beginners (Campaign)' instead of just 'SNS Marketing for Beginners'. 
Verification page: https://www.internetacademy.jp/mem/admins/school/application_enroll/239895",
        "jp": "在学証明書の受講コース名の表示不具合。正しくは「ゼロから学ぶSNSマーケティング入門（キャンペーン）」と表示される必要があります。修正をお願いいたします。"
    },
    "MD_SD-1256": {
        "en": "Correction needed for duplicate data parsing in the legacy sync script. Task 9 was created with redundant info. Please consolidate.",
        "jp": "以前の同期スクリプトにおける重複データの修正。タスク9が冗長な情報で作成されました。統合をお願いします。"
    }
}

def run_fix():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')
    base_url = f"https://{space_id}.backlog.com/api/v2"
    
    for key, content in TRANSLATIONS.items():
        # Using ACTUAL newlines in the f-string template
        desc = f"## English Description

{content['en']}

## 原文 (Japanese)

{content['jp']}"
        
        url = f"{base_url}/issues/{key}"
        params = {"apiKey": api_key}
        payload = {"description": desc}
        
        try:
            print(f"Applying correct formatting fix to {key}...")
            r = requests.patch(url, params=params, data=payload)
            r.raise_for_status()
            print(f"SUCCESS: {key} is now correctly formatted.")
        except Exception as e:
            print(f"ERROR: Failed to fix {key}: {e}")

if __name__ == "__main__":
    run_fix()

import os
import requests
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

TASKS = {
    "MD_SD-1249": {
        "title": "Change first session date for student",
        "en": "Request to change the enrollment/start date for student Riho Kano from Feb 1, 2025 to Feb 1, 2026.",
        "jp": "加納梨穂さまの初回日の変更をお願いできませんでしょうか。\n変更前：20250201 1200\n変更後：20260201 1200",
        "req": "鈴木佳子", "id": "1"
    },
    "MD_SD-1250": {
        "title": "LMS Exam time limit discrepancy",
        "en": "Possible bug in LMS exam timing. Tests are showing completion times longer than the 30-minute limit (e.g., 37m 59s).",
        "jp": "法人LMSの本試験の制限時間を30分に設定していても、30分以上かけてテストを実施できている可能性がある。もしくは、実際に受験した時間とLMSに表示される回答時間が違う可能性がある。",
        "req": "稲葉由衣", "id": "2"
    },
    "MD_SD-1251": {
        "title": "Preserve line breaks in LMS reports",
        "en": "User-entered line breaks are being lost in the LMS report confirmation screen, resulting in a single continuous paragraph.",
        "jp": "受講生の入力した改行が、確認画面でも同様に確認できるようにしてほしいというご要望でございます。現在は改行が無くなって１つのパラグラフで表示されています。",
        "req": "谷川大虎", "id": "3"
    },
    "MD_SD-1252": {
        "title": "Web Creator page display error",
        "en": "The Web Creator Certification guide page is not loading or displaying correctly, preventing exam applications.",
        "jp": "【結論】Webクリエイター認定試験のご案内ページが正しく表示されない為、不具合の解消をお願いできますでしょうか。",
        "req": "中村駿吾", "id": "4"
    },
    "MD_SD-1253": {
        "title": "Block zero-rating feedback submissions",
        "en": "Feedback sheets are being submitted with all zeroes (0 0 0) for ratings. Validation should require star ratings before submission.",
        "jp": "感想シートの評価が「0 0 0」の状態で投稿されております。本来、星マークの評価をつけないと投稿できないはずなので修正をお願いいたします。",
        "req": "石井陽介", "id": "5"
    },
    "MD_SD-1254": {
        "title": "Lesson form errors when field unselected",
        "en": "Reservation form malfunctions when 'Field of Interest' is left blank, showing false 'slot full' or 'unexpected' errors.",
        "jp": "【報告・相談】「興味がある分野」未選択時のフォーム動作異常について。①予約時間帯エラー、②予期せぬエラーの不具合が発生しています。",
        "req": "榎本智香", "id": "6"
    },
    "MD_SD-1255": {
        "title": "Incorrect course name on certificates",
        "en": "Enrollment certificates are showing the base course name instead of the required '(Campaign)' version.",
        "jp": "在学証明書の受講コース名の表示不具合。正しくは「ゼロから学ぶSNSマーケティング入門（キャンペーン）」と表示される必要があります。",
        "req": "眞尾由紀子", "id": "7"
    },
    "MD_SD-1256": {
        "title": "UI improvement for enrollment terms screen",
        "en": "Student feedback indicates the enrollment terms/agreement screens are difficult to use. Requesting a UI/UX review.",
        "jp": "入校時の約款確認などの画面が使いづらく、受講生からご意見をいただきました。UI設計の見直しをお願いします。",
        "req": "鈴木佳子", "id": "9"
    }
}

def run_surgical_fix():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')
    base_url = f"https://{space_id}.backlog.com/api/v2"
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    for key, data in TASKS.items():
        full_title = f"[ERROR] {data['title']} ({data['req']} - #{data['id']})"
        desc = f"## English Summary\n\n{data['en']}\n\n## Reference Links\n- **Google Sheets**: [View Sheet](https://docs.google.com/spreadsheets/d/{sheet_id}/edit)\n\n## 原文 (Japanese)\n\n{data['jp']}"
        url = f"{base_url}/issues/{key}"
        params = {"apiKey": api_key}
        payload = {"summary": full_title, "description": desc}
        try:
            r = requests.patch(url, params=params, data=payload)
            r.raise_for_status()
            print(f"SUCCESS: {key} updated.")
        except Exception as e:
            print(f"ERROR: {key} failed: {e}")

if __name__ == "__main__":
    run_surgical_fix()

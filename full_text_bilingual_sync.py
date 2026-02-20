import os
import requests
from dotenv import load_dotenv

load_dotenv('/home/min/projects/personal-agents/.env')

TASKS = {
    "MD_SD-1249": {
        "title": "Change first session date for student",
        "en": """Could you please change the first session date for Riho Kano?
Before: 20250201 12:00
After: 20260201 12:00

▼Kikuichi URL: https://www.internetacademy.jp/mem/admins/contract/241731?list=1""",
        "jp": """加納梨穂さまの初回日の変更をお願いできませんでしょうか。
変更前：20250201 1200
変更後：20260201 1200

▼菊一URL：https://www.internetacademy.jp/mem/admins/contract/241731?list=1""",
        "req": "鈴木佳子", "id": "1"
    },
    "MD_SD-1250": {
        "title": "LMS Exam time limit discrepancy",
        "en": """Even if the corporate LMS has a 30-minute time limit for the actual exam, it's possible that the test took longer than 30 minutes. Alternatively, the actual test time and the response time displayed on the LMS may differ. Please confirm this.
We received a call from a participant at the Information and Communications Equipment Association.
Dear Yuya Imasu,
Although the test should be completed within 30 minutes, after taking the test, the response time displayed was '37 minutes 59 seconds.' Furthermore, Imasu believes he responded within 30 minutes.
Yui Inaba checked Imasu's response time from her administrator account, and it displayed '37 minutes 59 seconds.'
Admin Account ID: b3724u0126 PW: Qtg4ZTFrc
Imasu's Personal Account ID: b3724u0129 PW: WVQ34PA7i""",
        "jp": """法人LMSの本試験の制限時間を30分に設定していても、30分以上かけてテストを実施できている可能性がある。
もしくは、実際に受験した時間とLMSに表示される回答時間が違う可能性がある。ご確認お願いいたします。
一般社団法人情報通信設備協会様の受講者様より、お電話いただきました。
井桝優矢さま
30分以内に受験しなければいけないはずだが、受験後、回答時間が「37分59秒」と表示された。また、井桝様としては30分以内に回答したはず。とのことです。
稲葉由衣が管理者アカウントから井桝様の回答時間を確認しましたが、「37分59秒」の表示でした。
管理者アカウント　ID ：b3724u0126　PW:　Qtg4ZTFrc
井桝様ご本人のアカウント　ID ：b3724u0129　PW:　WVQ34PA7i""",
        "req": "稲葉由衣", "id": "2"
    },
    "MD_SD-1251": {
        "title": "Preserve line breaks in LMS reports",
        "en": """We received a request from PI Murabayashi-sama regarding the daily report confirmation for the Mitsubishi Motors Corporation training that is currently being conducted. The request is to ensure that line breaks entered by students can be confirmed in the same way on the confirmation screen.
Since the daily report is necessary for training evaluation (reporting from the instructor to the person in charge on the other side) and is an important item, could you please confirm this?

Below is the message received from Murabayashi-sama:
Regarding line breaks in LMS
I advise students to manage their progress quantitatively. And I also recommend using bullet points for numerical parts to make them easier to read. However, as shown below, the line breaks have disappeared and are displayed as a single paragraph. Is it possible to display it so that line breaks are made in the same place where the student inserted them?""",
        "jp": """PI村林様より、現在ご登壇いただいている三菱自動車工業様の研修の日報確認についてご要望を頂きました。
受講生の入力した改行が、確認画面でも同様に確認できるようにしてほしいというご要望でございます。

日報報告が、研修評価(講師から先方担当者への報告)に必要で、重要な項目となっているため、
恐れ入りますが、ご確認をお願いできますでしょうか。

以下村林様よりいただいたメッセージです。

▼村林様よりいただいたメッセージ
LMSの改行について

受講生へは、定量的に進捗管理をするようにアドバイスしています。
そして、数値部分は見やすい様に箇条書きにする事も推奨しています。

しかし、以下のように改行が無くなって１つのパラグラフで表示されています。
受講生が改行を入れた場所で、同じように改行されるように表示して頂く事は可能でしょうか？""",
        "req": "谷川大虎", "id": "3"
    },
    "MD_SD-1252": {
        "title": "Web Creator page display error",
        "en": """[Conclusion] The Web Creator Certification guide page is not displaying correctly, so could you please resolve this issue? If this cannot be viewed, students cannot apply for Web Creator, so please respond as soon as possible.
Regarding the Web Creator Ability Certification guide page, we have confirmed that it is currently not being displayed normally. We have received an inquiry from a student via chat, and we have confirmed here that a similar display problem occurs when actually accessing the URL below.

▼Relevant page (Guide to the Web Creator Certification Exam)
https://www.internetacademy.jp/bohr/guide09
▼Previous page linked to the relevant page
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1

▼Student who asked the question
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1""",
        "jp": """【結論】Webクリエイター認定試験のご案内ページが正しく表示されない為、不具合の解消をお願いできますでしょうか。

こちらが見れないとWebクリの申し込みができない為、早めのご対応を御願い致します。
Webクリエイター能力認定試験のご案内ページにつきまして、
現在、正常に表示されない事象が発生していることを確認しております。
現在受講生様よりチャットにてお問い合わせをいただいており、
こちらでも実際に下記URLへアクセスし、同様の表示不具合が発生していることを確認しております。

▼該当ページ(Webクリエイター認定試験のご案内)
https://www.internetacademy.jp/bohr/guide09
▼該当のページへのリンク前ページ
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1

▼ご質問いただいた受講生様
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1""",
        "req": "中村駿吾", "id": "4"
    },
    "MD_SD-1253": {
        "title": "Block zero-rating feedback submissions",
        "en": """This month, two feedback sheets have been submitted with ratings of '0 0 0'. Originally, it should not be possible to submit without giving a star rating, so the fact that they are being submitted with '0 0 0' is likely strange in itself.
I apologize for the inconvenience while you are busy, but please check why this is happening and correct it so that submissions cannot be made with '0 0 0'.

Example:
2026-02-03(Tue) 11:16 Homepage C 3rd Session Homepage C3(1h 28m) 0 0 0 Mio Takahashi
2026-02-11(Wed) 22:00 2026-02-11(Wed) Yosuke Ishii PHP 0 0 0 Thank you for today's lesson as well. Today's lesson was easy to understand and helpful. However, as it progresses, the level of difficulty also increases, so it's still difficult. I thought I would review the on-demand content and practice coding in my spare time. Looking forward to tomorrow as well. Kaoru Asano""",
        "jp": """当月2件、感想シートの評価が「0 0 0」の状態で投稿されております。

本来、星マークの評価をつけないと投稿できないはずなので
「0 0 0」で投稿されていること自体がおかしいはずかと存じます。

お忙しい中お手数をおかけしますが、なぜそのような状態になっているかの
ご確認の上、「0 0 0」で投稿できないよう修正のほど、よろしくお願いいたします。

例
2026-02-03(火) 11:16         ホームページC         第3回         ホームページC3(1時間28分)         0         0         0                 
髙橋澪

2026-02-11(水) 22:00         2026-02-11(水)         石井陽介         PHP         0         0         0         本日の授業もありがとうございました。 今日の授業もわかりやすく教えて頂き助かりました。ですが進むにつれて難易度も増してくるので、やっぱり難しいですね。オンデマンドも見返して隙間時間にコード練習しようと思いました。
明日もよろしくお願いします。         
浅野薫""",
        "req": "石井陽介", "id": "5"
    },
    "MD_SD-1254": {
        "title": "Lesson form errors when field unselected",
        "en": """[Report/Consultation] Abnormal form behavior when 'Field of Interest' is not selected. When conducting a test CV without selecting 'Field of Interest', the following errors occur:

■Test Environment
Target Form: /lesson/
https://www.internetacademy.jp/lesson/

■Confirmed Phenomena (2 points)
1. Reservation Time Slot Error: Even when choosing a clearly available date, it displays 'The reservation time slot is already full. Please try another time slot.' and the CV does not go through.
2. Unexpected Error: While it displays 'An unexpected error occurred. Please try again.', the CV actually goes through normally (mismatch between screen and action).

The phenomenon of the reservation form not working correctly when 'Field of Interest' is not selected is continuing to occur. Since it affects user experience, I believe emergency measures can be taken by making it a 'required' item. I apologize for the inconvenience while you are busy, but I would appreciate your confirmation/response.""",
        "jp": """【報告・相談】「興味がある分野」未選択時のフォーム動作異常について

「興味がある分野」未選択の場合のテストCVを実施すると、以下のエラーが起こります。

■テスト環境
対象フォーム：/lesson/
https://www.internetacademy.jp/lesson/

■確認された事象（2点）
①予約時間帯エラー
明らかに空いている日程を選択しても、「予約時間帯はすでに埋まっています。別の時間帯でお試しください。」と表示され、CVが通らない。

②予期せぬエラー
「予期せぬエラーが発生しました。もう一度お試しください。」と表示される一方で、CVは正常に通る(画面と不一致)。

「興味がある分野」未選択時に、予約フォームで正常動作しない事象が引き続き発生しています。
ユーザー体験に影響するため、「必須」項目にすることで一旦応急処置はできると考えております。
ご多用のところ恐れ入りますが、ご確認/ご対応いただけますと幸いです。""",
        "req": "榎本智香", "id": "6"
    },
    "MD_SD-1255": {
        "title": "Incorrect course name on certificates",
        "en": """Problem with course name display on Enrollment Certificates. When printing an enrollment certificate in Kikuichi, the course name is displayed as 'Introduction to SNS Marketing from Scratch'. Since this course is a campaign course, it must be set to correctly display 'Introduction to SNS Marketing from Scratch (Campaign)'. Please correct this.

Please confirm on Hanako Narahira's enrollment certificate page.
Hanako Narahira
https://www.internetacademy.jp/mem/admins/school/application_enroll/239895""",
        "jp": """在学証明書の受講コース名の表示不具合
菊一で在学証明書を印刷すると、受講コース名に
「ゼロから学ぶSNSマーケティング入門」と表示されてしまいます。
本講座はキャンペーン講座のため、
正しくは「ゼロから学ぶSNSマーケティング入門（キャンペーン）」と
表示されるよう設定する必要があります。
修正をお願いいたします。

受講生様の奈良平華子様の在学証明書のページでご確認ください。
奈良平華子さま
https://www.internetacademy.jp/mem/admins/school/application_enroll/239895""",
        "req": "眞尾由紀子", "id": "7"
    },
    "MD_SD-1256": {
        "title": "UI improvement for enrollment terms screen",
        "en": """The screens for confirming terms and conditions at the time of enrollment are difficult to use, and we have received feedback from students. Please review the UI design.""",
        "jp": """入校時の約款確認などの画面が使いづらく、受講生からご意見をいただきました。
UI設計の見直しをお願いします。""",
        "req": "鈴木佳子", "id": "9"
    }
}

def run_fix():
    api_key = os.getenv('BACKLOG_API_KEY')
    space_id = os.getenv('BACKLOG_SPACE_ID')
    base_url = f"https://{space_id}.backlog.com/api/v2"
    
    for key, data in TASKS.items():
        full_title = f"[ERROR] {data['title']} ({data['req']} - #{data['id']})"
        desc = f"## English Translation\n\n{data['en']}\n\n## 原文 (Japanese)\n\n{data['jp']}"
        url = f"{base_url}/issues/{key}"
        params = {"apiKey": api_key}
        payload = {"summary": full_title, "description": desc}
        
        try:
            r = requests.patch(url, params=params, data=payload)
            r.raise_for_status()
            print(f"SUCCESS: {key} updated.")
        except Exception as e:
            print(f"ERROR: Failed to fix {key}: {e}")

if __name__ == "__main__":
    run_fix()

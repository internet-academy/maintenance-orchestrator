import os
import json
from agents.cloud_ingestor import CloudIngestor
from agents.load_balancer import LoadBalancer, DeveloperTimeline
from datetime import datetime

class Orchestrator:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        if self.dry_run:
            print("!!! RUNNING IN DRY RUN MODE - NO API MUTATIONS WILL OCCUR !!!")
        
        self.google_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.backlog_key = os.getenv('BACKLOG_API_KEY')
        self.space_id = os.getenv('BACKLOG_SPACE_ID')

        self.ingestor = CloudIngestor(self.google_json, self.sheet_id)
        self.load_balancer = LoadBalancer(self.backlog_key, self.space_id)
        
        # Real Developer Mapping for i-academy space
        self.developer_map = {
            "Saurabh": 984450,
            "Raman": 1819362,
            "Ewan": 1880127,
            "Choo": 1052465
        }
        
        # Initialize Timelines for all developers
        # Defaults to Today, but can be overridden via env var (e.g. for March start)
        self.start_date = os.getenv('SYNC_START_DATE') 
        
        self.timelines = {}
        for name, dev_id in self.developer_map.items():
            timeline = DeveloperTimeline(name, start_date=self.start_date)
            # ALWAYS pre-fill with actual Backlog load to ensure real-time accuracy
            try:
                actual_load = self.load_balancer.get_active_workload(dev_id, project_id=528169)
                timeline.fill_hours(actual_load)
            except Exception as e:
                print(f"WARNING: Could not fetch initial load for {name}: {e}")
            
            self.timelines[dev_id] = timeline

    def run(self):
        print(f"--- Starting Orchestration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        display_date = self.start_date if self.start_date else "Today"
        print(f"\n--- Team Capacity Map (Starting {display_date}) ---")
        for name, dev_id in self.developer_map.items():
            timeline = self.timelines[dev_id]
            # Simple bar chart: [######....]
            bars = ""
            for b in timeline.buckets:
                fill_ratio = b['used'] / self.load_balancer.DAILY_LIMIT_HOURS
                if fill_ratio >= 1.0: bars += "█"
                elif fill_ratio > 0.5: bars += "▓"
                elif fill_ratio > 0: bars += "░"
                else: bars += "."
            print(f"{name.ljust(8)} [{bars}] first day usage: {timeline.get_today_usage()}h")
        print("--------------------------------------------\n")

        try:
            tasks = self.ingestor.get_live_tasks()
            print(f"Found {len(tasks)} valid tasks in Google Sheets.")

            for task in tasks:
                self.process_task(task)

        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR: {str(e)}")
            traceback.print_exc()

    def _generate_bilingual_description(self, task):
        """Constructs a bilingual description with deep links and full translation."""
        # Constants for precision linking
        GID = "635134579"
        
        # Name Mapping (Localized to English)
        NAME_MAPPING = {
            "鈴木佳子": "Suzuki",
            "稲葉由衣": "Inaba",
            "谷川大虎": "Tanikawa",
            "中村駿吾": "Nakamura",
            "石井陽介": "Ishii",
            "榎本智香": "Enomoto",
            "眞尾由紀子": "Mao"
        }
        
        # High-Fidelity Preset Translations for existing tasks (Verbatim)
        PRESET_TRANSLATIONS = {
            "1": {
                "title": "Change first session date for student",
                "en": """Could you please change the first session date for Riho Kano?
Before: 20250201 12:00
After: 20260201 12:00

▼Kikuichi URL: https://www.internetacademy.jp/mem/admins/contract/241731?list=1"""
            },
            "2": {
                "title": "LMS Exam time limit discrepancy",
                "en": """Even if the corporate LMS has a 30-minute time limit for the actual exam, it's possible that the test took longer than 30 minutes. Alternatively, the actual test time and the response time displayed on the LMS may differ. Please confirm this.
We received a call from a participant at the Information and Communications Equipment Association.
Dear Yuya Imasu,
Although the test should be completed within 30 minutes, after taking the test, the response time displayed was '37 minutes 59 seconds.' Furthermore, Imasu believes he responded within 30 minutes.
Yui Inaba checked Imasu's response time from her administrator account, and it displayed '37 minutes 59 seconds.'
Admin Account ID: b3724u0126 PW: Qtg4ZTFrc
Imasu's Personal Account ID: b3724u0129 PW: WVQ34PA7i"""
            },
            "3": {
                "title": "Preserve line breaks in LMS reports",
                "en": """We received a request from PI Murabayashi-sama regarding the daily report confirmation for the Mitsubishi Motors Corporation training that is currently being conducted. The request is to ensure that line breaks entered by students can be confirmed in the same way on the confirmation screen.
Since the daily report is necessary for training evaluation (reporting from the instructor to the person in charge on the other side) and is an important item, could you please confirm this?

Below is the message received from Murabayashi-sama:
Regarding line breaks in LMS
I advise students to manage their progress quantitatively. And I also recommend using bullet points for numerical parts to make them easier to read. However, as shown below, the line breaks have disappeared and are displayed as a single paragraph. Is it possible to display it so that line breaks are made in the same place where the student inserted them?"""
            },
            "4": {
                "title": "Web Creator page display error",
                "en": """[Conclusion] The Web Creator Certification guide page is not displaying correctly, so could you please resolve this issue? If this cannot be viewed, students cannot apply for Web Creator, so please respond as soon as possible.
Regarding the Web Creator Ability Certification guide page, we have confirmed that it is currently not being displayed normally. We have received an inquiry from a student via chat, and we have confirmed here that a similar display problem occurs when actually accessing the URL below.

▼Relevant page (Guide to the Web Creator Certification Exam)
https://www.internetacademy.jp/bohr/guide09
▼Previous page linked to the relevant page
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1

▼Student who asked the question
https://www.internetacademy.jp/mem/admins/customer/custom_info/240492/?list=1"""
            },
            "5": {
                "title": "Block zero-rating feedback submissions",
                "en": """This month, two feedback sheets have been submitted with ratings of '0 0 0'. Originally, it should not be possible to submit without giving a star rating, so the fact that they are being submitted with '0 0 0' is likely strange in itself.
I apologize for the inconvenience while you are busy, but please check why this is happening and correct it so that submissions cannot be made with '0 0 0'.

Example:
2026-02-03(Tue) 11:16 Homepage C 3rd Session Homepage C3(1h 28m) 0 0 0 Mio Takahashi
2026-02-11(Wed) 22:00 2026-02-11(Wed) Yosuke Ishii PHP 0 0 0 Thank you for today's lesson as well. Today's lesson was easy to understand and helpful. However, as it progresses, the level of difficulty also increases, so it's still difficult. I thought I would review the on-demand content and practice coding in my spare time. Looking forward to tomorrow as well. Kaoru Asano"""
            },
            "6": {
                "title": "Lesson form errors when field unselected",
                "en": """[Report/Consultation] Abnormal form behavior when 'Field of Interest' is not selected. When conducting a test CV without selecting 'Field of Interest', the following errors occur:

■Test Environment
Target Form: /lesson/
https://www.internetacademy.jp/lesson/

■Confirmed Phenomena (2 points)
1. Reservation Time Slot Error: Even when choosing a clearly available date, it displays 'The reservation time slot is already full. Please try another time slot.' and the CV does not go through.
2. Unexpected Error: While it displays 'An unexpected error occurred. Please try again.', the CV actually goes through normally (mismatch between screen and action).

The phenomenon of the reservation form not working correctly when 'Field of Interest' is not selected is continuing to occur. Since it affects user experience, I believe emergency measures can be taken by making it a 'required' item. I apologize for the inconvenience while you are busy, but I would appreciate your confirmation/response."""
            },
            "7": {
                "title": "Incorrect course name on certificates",
                "en": """Problem with course name display on Enrollment Certificates. When printing an enrollment certificate in Kikuichi, the course name is displayed as 'Introduction to SNS Marketing from Scratch'. Since this course is a campaign course, it must be set to correctly display 'Introduction to SNS Marketing from Scratch (Campaign)'. Please correct this.

Please confirm on Hanako Narahira's enrollment certificate page.
Hanako Narahira
https://www.internetacademy.jp/mem/admins/school/application_enroll/239895"""
            },
            "9": {
                "title": "UI improvement for enrollment terms screen",
                "en": """The screens for confirming terms and conditions at the time of enrollment are difficult to use, and we have received feedback from students. Please review the UI design."""
            }
        }
        
        task_id = str(task['id'])
        preset = PRESET_TRANSLATIONS.get(task_id)
        
        # Determine Title Summary and English Translation
        if preset:
            title_summary = preset['title']
            en_translation = preset['en']
        else:
            # Fallback for new tasks
            clean_content = task['content'].replace('\n', ' ').strip()
            title_summary = clean_content[:60] + "..." if len(clean_content) > 60 else clean_content
            en_translation = title_summary # This should ideally be replaced by a real LLM call
            
        # Get localized name
        romaji_name = NAME_MAPPING.get(task['requester'], task['requester'])
        
        # Construct Precision Sheet Link
        row = task['row_index'] + 1
        sheet_link = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit?gid={GID}#gid={GID}&range=B{row}:C{row}"
        
        # Build Description Body
        description = f"ID: {task_id}\n"
        description += f"Sheet Link: {sheet_link}\n\n"
        description += f"## English Translation\n\n{en_translation}\n\n"
        description += f"## 原文 (Japanese)\n\n{task['content']}"
        
        return description, title_summary, romaji_name

    def _verify_ownership(self, backlog_id, current_row_index):
        """
        Verifies if the existing Backlog ticket actually belongs to this row.
        Returns True if it matches, False if it's a copied ID from elsewhere.
        """
        try:
            issue = self.load_balancer.get_issue(backlog_id)
            desc = issue.get('description', '')
            
            # Extract the 'Sheet Link' from the description using regex
            # Looking for: range=B{row}:C{row}
            # We use a broad check for the row index in the link
            pattern = fr"range=B{current_row_index + 1}:C{current_row_index + 1}"
            
            if pattern in desc:
                return True
            else:
                print(f"⚠️ COLLISION DETECTED: {backlog_id} belongs to a different row. Description link mismatch.")
                return False
        except Exception as e:
            print(f"DEBUG: Could not verify ownership for {backlog_id} (might be deleted): {e}")
            return False

    def process_task(self, task):
        # Generate Bilingual content, summary, and localized name
        full_desc, ai_summary, romaji_name = self._generate_bilingual_description(task)
        task['description'] = full_desc
        task['title_summary'] = ai_summary
        task['summary'] = f"[ERROR] {ai_summary} ({romaji_name} - #{task['id']})"

        # 1. Update Detection & Ownership Verification
        backlog_id = task.get('backlog_id')
        if backlog_id:
            # NEW: Verify that this ID wasn't just copy-pasted from another row
            is_rightful_owner = self._verify_ownership(backlog_id, task['row_index'])
            
            if is_rightful_owner:
                print(f"UPDATE: Found verified Backlog ID {backlog_id}. Updating fields...")
                # CALCULATE TIMELINE FOR UPDATES
                best_dev = self._find_best_dev(task['estimated_hours'])
                if best_dev:
                    due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
                    task['deadline'] = due_date
                    print(f"DEBUG: Calculated projected finish for verified update: {due_date}")
            else:
                print(f"ACTION: ID {backlog_id} appears to be a copy. Resetting to CREATE mode for this row.")
                backlog_id = None # Force creation of a fresh ticket
        
        if backlog_id: # This only executes if verified above
            if self.dry_run:
                print(f"[DRY RUN] Would update verified Backlog {backlog_id}")
                return
            try:
                self.load_balancer.update_backlog_issue(backlog_id, task)
                print(f"SUCCESS: Updated Backlog {backlog_id}")
            except Exception as e:
                print(f"ERROR: Failed to update {backlog_id}: {str(e)}")
            return

        # 2. Skip if already assigned in sheet
        if task.get('pic'):
            print(f"SKIP: Task {task['id']} already has PIC: {task['pic']}")
            return

        # 3. New Task Assignment Logic
        best_dev = self._find_best_dev(task['estimated_hours'])
        
        if best_dev:
            # The completion date is the calculated deadline
            due_date = self.timelines[best_dev['id']].fill_hours(task['estimated_hours'])
            task['deadline'] = due_date
            
            print(f"ASSIGNING: Task {task['id']} (Req: {task['requester']}) ({task['estimated_hours']}h) -> {best_dev['name']}")
            print(f"TITLE PREVIEW: [ERROR] {ai_summary} ({task['requester']} - #{task['id']})")
            
            if self.dry_run:
                print(f"[DRY RUN] Would create Backlog Issue for {best_dev['name']} with deep-link and summary.")
                return
            try:
                issue = self.load_balancer.create_backlog_issue(best_dev['id'], task)
                issue_key = issue['issueKey']
                print(f"CREATED: Backlog Issue {issue_key}")
                self.ingestor.write_backlog_id(task['row_index'], issue_key)
            except Exception as e:
                print(f"ERROR: Failed to create issue: {str(e)}")
        else:
            print(f"OVERLOAD: No capacity for Task {task['id']} even in 14-day window.")

    def _find_best_dev(self, hours):
        """Finds the dev with the lowest Today's usage, prioritizing Core."""
        core_options = []
        manager_option = None

        for name, dev_id in self.developer_map.items():
            timeline = self.timelines[dev_id]
            today_usage = timeline.get_today_usage()
            
            # Check if Today has any space at all
            if today_usage < self.load_balancer.DAILY_LIMIT_HOURS:
                option = {"name": name, "id": dev_id, "usage": today_usage}
                if name == "Choo":
                    manager_option = option
                else:
                    core_options.append(option)
        
        if core_options:
            return sorted(core_options, key=lambda x: x['usage'])[0]
        
        return manager_option

if __name__ == "__main__":
    manager = Orchestrator()
    manager.run()

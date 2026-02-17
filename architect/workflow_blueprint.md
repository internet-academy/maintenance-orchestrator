# Multi-Agent Workflow Architecture: The Nulab-GitHub Orchestrator

This document defines the specialized agents and their interaction protocol for automating the engineering management workflow.

## 1. The Ingestor (Data Specialist)
- **Primary Tool:** Google Sheets API.
- **Responsibility:** Monitor the sheet for new entries. Sanitize and validate the data.
- **Output:** `StandardizedTaskObject` { title, description, page_url, preferred_deadline, estimated_hours }.
- **Accuracy Logic:** Handles edge cases in user input (e.g., missing deadlines or vague descriptions).

## 2. The Load Balancer (Resource Specialist)
- **Primary Tool:** Backlog API.
- **Responsibility:** Query the current active tasks for all developers. 
- **Decision Logic:** 
  - `Total_Load = Sum(backlog_active_tasks.estimated_hours)`
  - `If (Total_Load + Task.estimated_hours) <= 6: Assign(Developer)`
  - `Else: Flag for Manual Review / Next Day Queue.`
- **Accuracy Logic:** Prevents developer burnout and ensures realistic scheduling.

## 3. The Communicator (Context Specialist)
- **Primary Tool:** Google Chat API.
- **Responsibility:** Format and deliver human-centric notifications.
- **Actions:**
  - DM Developer on assignment.
  - Post "Pending Approval" report to the Requestee.
- **Accuracy Logic:** Translates technical state changes into clear, actionable human messages.

## 4. The Sync Agent (Git Specialist)
- **Primary Tool:** GitHub Webhooks / Actions.
- **Responsibility:** Map GitHub events to Backlog status changes.
- **Triggers:**
  - `PR Created` -> Backlog: `Pending Release`
  - `PR Merged` -> Backlog: `Pending Report`
- **Accuracy Logic:** Uses regex to extract Backlog Issue Keys from PR titles/branches to ensure 1:1 mapping.

## 5. The Janitor (Compliance Specialist)
- **Primary Tool:** Persistence Layer (DB/Cron).
- **Responsibility:** Monitor "Pending Approval" states.
- **Logic:**
  - If `status == 'Pending Approval'` AND `age > 7 days` -> Backlog: `Closed`.
  - If `Requestee_Confirmation == True` -> Backlog: `Closed`.
- **Accuracy Logic:** Ensures the backlog doesn't clutter with stale tasks.

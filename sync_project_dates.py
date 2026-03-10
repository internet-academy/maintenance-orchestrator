import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def sync_projects():
    TOKEN = os.getenv('GITHUB_TOKEN')
    ORG = "internet-academy"
    HEADERS = {"Authorization": f"token {TOKEN}"}
    URL = "https://api.github.com/graphql"

    print("=== PROJECT SYNCHRONIZATION: P4 -> P3 ===\n")

    # 1. Fetch ALL items from Project 4 (Source)
    query_p4 = """
    query($org: String!) {
      organization(login: $org) {
        projectV2(number: 4) {
          items(first: 100) {
            nodes {
              content { ... on Issue { number title } }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
      }
    }
    """
    resp_p4 = requests.post(URL, headers=HEADERS, json={"query": query_p4, "variables": {"org": ORG}})
    p4_items = resp_p4.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])

    # 2. Fetch ALL items from Project 3 (Target)
    query_p3 = """
    query($org: String!) {
      organization(login: $org) {
        projectV2(number: 3) {
          items(first: 100) {
            nodes {
              id
              content { ... on Issue { number title } }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2Field { name } } }
                }
              }
            }
          }
        }
      }
    }
    """
    resp_p3 = requests.post(URL, headers=HEADERS, json={"query": query_p3, "variables": {"org": ORG}})
    p3_items = resp_p3.json().get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])

    # Map P3 items for quick lookup
    p3_map = {}
    for item in p3_items:
        content = item.get('content')
        if content:
            # Store by issue number
            p3_map[content['number']] = {
                'item_id': item['id'],
                'dates': {fv['field']['name']: fv.get('date') for fv in item['fieldValues']['nodes'] if fv.get('field')}
            }

    # 3. COMPARE AND UPDATE
    update_count = 0
    
    # IDs for Project 3 fields
    P3_START_FIELD = "PVTF_lADOA1jKuM4BQoorzg-xYWY"
    P3_END_FIELD = "PVTF_lADOA1jKuM4BQoorzg-xYWs"

    for p4_item in p4_items:
        content = p4_item.get('content')
        if not content: continue
        
        issue_num = content['number']
        p4_dates = {fv['field']['name']: fv.get('date') for fv in p4_item['fieldValues']['nodes'] if fv.get('field')}
        p4_start = p4_dates.get('Start date')
        p4_end = p4_dates.get('End date')

        if not p4_start or not p4_end:
            continue # Source has no dates

        if issue_num in p3_map:
            p3_data = p3_map[issue_num]
            p3_start = p3_data['dates'].get('Start date')
            p3_end = p3_data['dates'].get('End date')

            if p3_start != p4_start or p3_end != p4_end:
                print(f"  - UPDATING #{issue_num} ({content['title'][:40]}...)")
                print(f"    Current P3: {p3_start} -> {p3_end}")
                print(f"    Source  P4: {p4_start} -> {p4_end}")
                
                # Update Start Date
                mut_start = """mutation($id: ID!, $field: ID!, $val: Date) { updateProjectV2ItemFieldValue(input: {projectId: "PVT_kwDOA1jKuM4BQoor", itemId: $id, fieldId: $field, value: {date: $val}}) { item { id } } }"""
                requests.post(URL, headers=HEADERS, json={"query": mut_start, "variables": {"id": p3_data['item_id'], "field": P3_START_FIELD, "val": p4_start}})
                
                # Update End Date
                mut_end = """mutation($id: ID!, $field: ID!, $val: Date) { updateProjectV2ItemFieldValue(input: {projectId: "PVT_kwDOA1jKuM4BQoor", itemId: $id, fieldId: $field, value: {date: $val}}) { item { id } } }"""
                requests.post(URL, headers=HEADERS, json={"query": mut_end, "variables": {"id": p3_data['item_id'], "field": P3_END_FIELD, "val": p4_end}})
                
                update_count += 1
        else:
            # Logic to add missing items could go here, but focusing on existing ones first
            pass

    print(f"\nSUCCESS: Synchronized {update_count} items to Project 3.")

if __name__ == "__main__":
    sync_projects()

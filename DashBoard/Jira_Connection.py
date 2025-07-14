import requests
from requests.auth import HTTPBasicAuth
import json
import os

class JiraSprintIssuesFetcher:
    def __init__(self, base_url, sprint_id, email, api_token):
        self.base_url = base_url
        self.sprint_id = sprint_id
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            "Accept": "application/json"
        }

    def get_sprint_issues(self):
        url = f"http://{self.base_url}/rest/agile/1.0/sprint/{self.sprint_id}/issue"
        try:
            response = requests.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sprint issues: {e}")
            return None

    def display_issues(self, issues):
        print(json.dumps(issues, indent=4, sort_keys=True, separators=(",", ": ")))

# --- Example Usage ---
if __name__ == "__main__":
    # Replace these with actual credentials and values
    BASE_URL = os.getenv("BASE_URL")
    SPRINT_ID = int(input())
    EMAIL = os.getenv("Email_id")
    API_TOKEN = os.getenv("API_TOKEN")

    fetcher = JiraSprintIssuesFetcher(BASE_URL, SPRINT_ID, EMAIL, API_TOKEN)
    issues = fetcher.get_sprint_issues()
    if issues:
        fetcher.display_issues(issues)

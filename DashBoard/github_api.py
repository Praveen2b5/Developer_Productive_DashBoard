import os
import requests
import json
from dotenv import load_dotenv

#Load .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GHP_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("GITHUB_TOKEN not found in environment variables or .env file")

API_BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def make_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 409:
        print("Repository exists but has no commits.")
        return []
    response.raise_for_status()
    return response.json()


def get_authenticated_user():
    return make_request(f"{API_BASE_URL}/user")


def get_user_repos(username, per_page=100):
    url = f"{API_BASE_URL}/users/{username}/repos"
    all_repos = []
    page = 1

    while True:
        params = {"per_page": per_page, "page": page}
        repos = make_request(url, params)
        if not repos:
            break
        all_repos.extend(repos)
        page += 1

    return all_repos

def get_user_commits(owner, repo, username):
    url = f"{API_BASE_URL}/repos/{owner}/{repo}/commits"
    params = {"author": username}
    return make_request(url, params)

def get_user_pull_requests(owner, repo, author):
    """
    Fetch pull requests in a repo created by a specific author.
    Uses the GitHub search API to filter by author.
    """
    url = f"{API_BASE_URL}/search/issues"
    query = f"repo:{owner}/{repo} type:pr author:{author}"
    params = {"q": query, "per_page": 100}
    return make_request(url, params).get("items", [])


def save_to_json(data, filename="user_pull_requests.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved data to {filename}")


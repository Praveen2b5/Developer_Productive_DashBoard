from github_api import (
    get_authenticated_user,
    get_user_repos,
    get_user_commits,
    get_user_pull_requests,
    get_repo_contributors,
    save_to_json
)
from tabulate import tabulate


def main():
    try:
        user = get_authenticated_user()
        username = user['login']
        print(f"Authenticated as: {username}")

        repos = get_user_repos(username)
        if not repos:
            print("No public repositories found.")
            return

        all_developer_data = []

        for repo in repos:
            repo_name = repo['name']
            repo_owner = repo['owner']['login']
            print(f"Repo: {repo_name}")

            contributors = get_repo_contributors(repo_owner, repo_name)
            if not contributors:
                print("   ⚠️ No contributors found.")
                continue

            for contributor in contributors:
                dev_login = contributor['login']
                print(f"   🔹 Developer: {dev_login}")

                commits = get_user_commits(repo_owner, repo_name, dev_login)
                prs = get_user_pull_requests(repo_owner, repo_name, dev_login)

                dev_data = {
                    "developer": dev_login,
                    "repo": repo_name,
                    "commit_count": len(commits),
                    "pull_requests": [{
                        "number": pr["number"],
                        "title": pr["title"],
                        "state": pr["state"],
                        "created_at": pr["created_at"],
                        "url": pr["html_url"]
                    } for pr in prs]
                }

                all_developer_data.append(dev_data)

        save_to_json(all_developer_data)
        print_developer_table(all_developer_data)
    except Exception as e:
        print(f"❌ Error: {e}")

def print_developer_table(developer_data):
    table = []
    for dev in developer_data:
        for pr in dev["pull_requests"]:
            table.append([
                dev["developer"],
                dev["repo"],
                dev["commit_count"],
                pr["number"],
                pr["title"],
                pr["state"],
                pr["created_at"],
                pr["url"]
            ])

    headers = [
        "Developer",
        "Repository",
        "Commits",
        "PR #",
        "PR Title",
        "PR State",
        "Created At",
        "PR URL"
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))



if __name__ == "__main__":
    main()

from github_api import (
    get_authenticated_user,
    get_user_repos,
    get_user_commits,
    get_user_pull_requests,
    save_to_json
)


def main():
    try:
        user = get_authenticated_user()
        username = user['login']
        print(f"Authenticated as: {username}")

        repos = get_user_repos(username)
        if not repos:
            print("No public repositories found.")
            return

        all_user_prs = []

        print(f"\nRepositories owned by {username}:")
        for repo in repos:
            repo_name = repo['name']
            print(f"\n🔹 {repo_name} (⭐ {repo['stargazers_count']})")

            # Commits
            commits = get_user_commits(username, repo_name, username)
            print(f" Commits by {username}: {len(commits)}")

            # Filtered PRs by user
            user_prs = get_user_pull_requests(username, repo_name, username)
            print(f"  📥 Pull Requests by {username}: {len(user_prs)}")

            for pr in user_prs[:3]:  # Preview
                print(f"    - PR #{pr['number']}: {pr['title']} [{pr['state']}]")

            # Add to collection for export
            all_user_prs.extend([
                {
                    "repo": repo_name,
                    "number": pr["number"],
                    "title": pr["title"],
                    "state": pr["state"],
                    "created_at": pr["created_at"],
                    "url": pr["html_url"]
                } for pr in user_prs
            ])

        # Save to JSON file
        save_to_json(all_user_prs)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

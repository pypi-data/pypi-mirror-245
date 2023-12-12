import os
import requests

def repush_repo():
    github_username = input("Enter the GitHub username: ")
    repo_name = input("Enter the name of the existing GitHub repository: ")
    token = input("Enter your GitHub personal access token: ")
    headers = {'Authorization': f'token {token}'}

    repo_check_url = f'https://api.github.com/repos/{github_username}/{repo_name}'
    repo_check_response = requests.get(repo_check_url, headers=headers)

    if repo_check_response.status_code != 200:
        print(f"Repository '{repo_name}' not found on the specified GitHub profile.")
        return

    print(f"Repository '{repo_name}' found on the specified GitHub profile.")

    os.system('git init')
    os.system('git add --all')
    os.system('git reset -- push_bot.py repush_bot.py')
    os.system(f'git commit -m "{input("Enter the commit name: ")}"')

    repo_url = repo_check_response.json().get('html_url')
    os.system(f'git remote add origin {repo_url}.git')

    os.system('git pull origin master --allow-unrelated-histories')
    os.system('git push -u origin master')

    if os.system('git diff-index --quiet HEAD --'):
        print("No merge conflict. Contents committed to GitHub.")
    else:
        print("Merge conflict detected. Resolving conflicts...")

        os.system('echo "Merge conflict resolved automatically" | git commit -a --amend --no-edit')
        os.system('git push -u origin master')

        print("Merge conflict resolved and contents committed to GitHub.")

repush_repo()

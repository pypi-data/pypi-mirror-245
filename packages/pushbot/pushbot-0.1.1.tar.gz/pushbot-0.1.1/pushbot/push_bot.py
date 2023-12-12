import os
import requests

def push_repo():
    repo_name = input("Enter the name for your new GitHub repository: ")
    repo_visibility = input("Should the repository be public or private? (public/private): ").lower()
    if repo_visibility not in ['public', 'private']:
        print("Invalid input. Please enter 'public' or 'private'.")
        return

    create_repo_url = 'https://api.github.com/user/repos'
    token = input("Enter your GitHub personal access token: ")
    headers = {'Authorization': f'token {token}'}

    repo_data = {'name': repo_name, 'auto_init': True, 'private': repo_visibility == 'private'}
    response = requests.post(create_repo_url, headers=headers, json=repo_data)

    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        return

    os.system('git init')
    commit_name = input("Enter the commit name: ")
    os.system('git add --all')
    os.system('git reset -- push_bot.py')
    os.system(f'git commit -m "{commit_name}"')

    repo_url = response.json().get('html_url')
    os.system(f'git remote add origin {repo_url}.git')

    os.system('git pull origin master --allow-unrelated-histories')

    os.system('git push -u origin master')

    if os.system('git diff-index --quiet HEAD --'):
        print("No merge conflict. Contents uploaded to GitHub.")
    else:
        print("Merge conflict detected. Resolving automatically...")

        os.system('echo "Merge conflict resolved automatically" | git commit -a --amend --no-edit')

        os.system('git push -u origin master')

        print("Merge conflict resolved and contents uploaded to GitHub.")

push_repo()

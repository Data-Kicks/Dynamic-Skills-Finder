'''
Utilities to interact with GitHub repositories, download files, and handle Git LFS files.
'''

import requests
import time


'''
Function to get the contents of a GitHub repository or a specific path within it.

:param repo_url: The URL of the GitHub repository or path.
:param api_url: (Optional) The GitHub API URL for the specific path.

:return: JSON response containing the contents of the repository or path, or None if an error occurs.
'''
def get_github_contents(repo_url, api_url=None):
    if not api_url:
        parts = repo_url.replace('https://github.com/', '').split('/')
        user_repo = '/'.join(parts[:2])
        path = '/'.join(parts[4:])
        
        api_url = f"https://api.github.com/repos/{user_repo}/contents/{path}"
    
    try:
        response = requests.get(api_url, headers={'Accept': 'application/vnd.github.v3.object'})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error trying to access to {api_url}: {e}")
        return None


'''
Function to download a file from a given URL and save it to the specified path.

:param url: The URL of the file to download.
:param save_path: The local path where the file should be saved.

:return: True if the download was successful, False otherwise.
'''
def download_file(url, save_path):
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download finished: {save_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading from {url}: {e}")
        return False


'''
Function to process the contents of a GitHub repository, downloading relevant files.

:param contents: JSON response containing the contents of the repository or path.
:param base_url: The base URL of the GitHub repository.
:param base_path: The local base path where files should be saved.
:param downloaded_files: List to store the paths of downloaded files.
'''
def process_github_contents(contents, base_url, base_path, downloaded_files):
    for item in contents["entries"]:
        if item['type'] == 'file':
            if item['name'].endswith('.json') or item['name'].endswith('.csv'):
                raw_url = item['download_url']

                relative_path = item['path'].split('data/matches/')[-1]
                save_path = base_path / relative_path.split('/')[-1]

                if download_file(raw_url, save_path):
                    downloaded_files.append(str(save_path))

                time.sleep(0.1)
            
            elif item['name'].endswith('.jsonl'):
                relative_path = item['path'].split('data/matches/')[-1]
                save_path = base_path / relative_path.split('/')[-1]

                lfs_url = "https://github.com/SkillCorner/opendata/raw/refs/heads/master/data/matches/" + relative_path

                if download_file(lfs_url, save_path):
                    downloaded_files.append(str(save_path))

                time.sleep(0.1)
                
        elif item['type'] == 'dir':
            print(f"Proccessing subdirectory: {item['name']}")
            sub_contents = get_github_contents(None, item['url'])
            if sub_contents:
                process_github_contents(sub_contents, base_url, base_path, downloaded_files)
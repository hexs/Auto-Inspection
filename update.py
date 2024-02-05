import os
import subprocess
import socket
import sys

from TextColor import *
from InstallPackage import installed_packages, upgrade_pip


def is_internet_available():
    try:
        socket.create_connection(("1.1.1.1", 80), timeout=3)
        print(f"{GREEN}{ITALICIZED}Internet is available.{ENDC}")
        return True
    except OSError:
        print(f"{RED}{ITALICIZED}Internet is not available.{ENDC}")
        return False


def install_requests_if_it_is_not_installed():
    if 'requests' not in installed_packages():
        try:
            prin(BLUE)
            subprocess.run(["pip", "install", "requests"], check=True)
            print(f"{UNDERLINE}requests installed successfully.")
            prin(ENDC)
        except Exception as e:
            prin(RED)
            print(f"Failed to install requests. Error: {UNDERLINE}{str(e)}")
            prin(ENDC)


def is_git_installed():
    try:
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f"{GREEN}{ITALICIZED}Git is installed. Version:{ENDC}", result.stdout.strip())
            return True
        else:
            print(f"{RED}{ITALICIZED}Git is not installed.{ENDC}")
            return False
    except FileNotFoundError:
        print(f"{RED}{ITALICIZED}Git is not installed.{ENDC}")
        return False


def get_latest_commit_sha(owner, repo, branch='main'):
    import requests

    api_url = f'https://api.github.com/repos/{owner}/{repo}/commits/{branch}'
    response = requests.get(api_url)

    if response.status_code == 200:
        commit_data = response.json()
        return commit_data['sha']
    else:
        raise Exception(f"Failed to fetch commit information. Status code: {response.status_code}")


def get_local_commit_sha():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Failed to get local commit SHA. Error: {result.stderr}")
    except FileNotFoundError:
        raise Exception("Git is not installed.")


def git_pull():
    try:
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print(f"{GREEN}{ITALICIZED}Git pull successful.{ENDC}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git pull failed. Error: {e.stderr}")


def is_venv_present():
    venv_activate_script = '.venv/Scripts/activate.bat'
    return os.path.exists(venv_activate_script)


def create_venv():
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("Virtual environment (.venv) created successfully.")
    except Exception as e:
        print(f"Failed to create virtual environment. Error: {str(e)}")


def activate_venv_and_run_program(main_py_path):
    venv_activate_script = '.venv/Scripts/activate.bat'
    if not os.path.exists(venv_activate_script):
        print(f"Error: Virtual environment activate script not found at {venv_activate_script}")
        sys.exit(1)

    activate_cmd = f'call {venv_activate_script}'
    python_cmd = 'python'
    combined_command = f'{activate_cmd} && {python_cmd} {main_py_path}'

    try:
        subprocess.run(combined_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error executing {UNDERLINE}{main_py_path}{ENDC}{RED}: {e}{ENDC}")


def update():
    install_requests_if_it_is_not_installed()
    if is_internet_available() and is_git_installed():
        owner = 'hexs'
        repo = 'Auto-Inspection'
        try:
            local_commit = get_local_commit_sha()
            latest_commit = get_latest_commit_sha(owner, repo)

            if local_commit != latest_commit:
                print(f"Local and remote commits are {YELLOW}{ITALICIZED}not the same. Performing git pull.{ENDC}")
                git_pull()
            else:
                print(f"Local and remote commits are {GREEN}{ITALICIZED}already in sync.{ENDC}")
        except Exception as e:
            print(f"{RED}{ITALICIZED}Error:{ENDC} {RED}{str(e)}{ENDC}")


if __name__ == '__main__':
    update()
    if not is_venv_present():
        create_venv()
    upgrade_pip()
    activate_venv_and_run_program('InstallPackage.py')
    activate_venv_and_run_program('main.py')
import subprocess
import sys
import os
from TextColor import *


def installed_packages():
    try:
        result = subprocess.run(f"pip freeze", capture_output=True, text=True)
        return [p.split('==')[0] for p in result.stdout.split('\n')]
    except Exception as e:
        raise Exception(f"{RED}Error: {str(e)}{ENDC}")


def install_package(package_name):
    try:
        prin(BLUE)
        subprocess.run(["pip", "install", package_name], check=True)
        print(f"{package_name} installed successfully.")
        prin(ENDC)
    except Exception as e:
        prin(RED)
        print(f"Failed to install {package_name}. Error: {str(e)}")
        prin(ENDC)


def upgrade_pip():
    try:
        subprocess.run("python -m pip install --upgrade pip", check=True)
        print(f"{BLUE}upgrade pip installed successfully.{ENDC}")
    except Exception as e:
        print(f"{RED}Failed to upgrade pip. Error: {str(e)}{ENDC}")


def install_package_all():
    all_packages = [
        'requests',
        'numpy',
        'opencv-python',
        'Flask',
        'pygame',
        'pygame-gui',
        'tensorflow',
    ]
    ins_packages = installed_packages()

    for p in set(all_packages) - set(ins_packages):
        install_package(p)


if __name__ == '__main__':
    upgrade_pip()
    install_package_all()

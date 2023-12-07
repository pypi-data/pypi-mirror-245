# -*- coding: utf-8 -*-
"""The utils functions of the arthub_login_window."""

# Import built-in modules
import os
import re
import subprocess

# Import third-party modules
from platformdirs import user_cache_dir


def current_path():
    return os.path.dirname(__file__)


def get_client_exe_path():
    root = current_path()
    return os.path.join(root, "resources", "client", "arthub-tools.exe")


def get_resource_file(file_name):
    root = current_path()
    return os.path.join(root, "resources", file_name)


def read_file(file_path):
    with open(file_path, "r") as file_obj:
        return file_obj.read()


def write_file(file_path, data):
    with open(file_path, "w") as file_obj:
        file_obj.write(data)


def get_login_account():
    account_file = get_account_cache_file()
    if os.path.exists(account_file):
        return read_file(account_file)


def save_login_account(account, cache_file=None):
    account_file = cache_file or get_account_cache_file()
    write_file(account_file, account)


def get_account_cache_file():
    root = user_cache_dir(appauthor="arthub", opinion=False)
    try:
        os.makedirs(root)
    # Ingoing when try create folder failed.
    except (IOError, WindowsError):
        pass
    return os.path.join(root, "arthub_account")


def run_exe(exe_path, args):
    command = [exe_path] + args
    if hasattr(subprocess, 'run'):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.returncode, result.stdout
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return process.returncode, stdout


def get_token_from_file(cache_file):
    if not os.path.exists(cache_file):
        return
    text = read_file(cache_file)
    match = re.search(r'api_token:\s*([^\n]+)', text)
    if not match:
        return
    return match.group(1)

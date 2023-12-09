import os
import re
import sys
import json
import argparse
from pathlib import Path


version="v0.1.13"


def create_directory_structure(base_path, structure):
    for name, content in structure.items():
        if isinstance(content, list):

            dir_path = base_path / name
            dir_path.mkdir(exist_ok=True)

            for item in content:
                if item:
                    (dir_path / item).touch()
        elif isinstance(content, dict):

            sub_dir_path = base_path / name
            sub_dir_path.mkdir(exist_ok=True)
            create_directory_structure(sub_dir_path, content)
        else:

            (base_path / name).touch()

def check_directory_structure(directory, expected_structure=None):
    if expected_structure is None:
        expected_structure = {
            "production": "directory",
            "staging": "directory",
            "group_vars": "directory",
            "host_vars": "directory",
            "library": "directory",
            "module_utils": "directory",
            "filter_plugins": "directory",
            "site.yml": "file",
            "webservers.yml": "file",
            "dbservers.yml": "file",
            "roles": "directory"
        }
    for item, item_type in expected_structure.items():
        item_path = os.path.join(directory, item)
        if not os.path.exists(item_path):
            print(f"Missing {item_path} of type {item_type}")
        else:
            if item_type == "directory" and not os.path.isdir(item_path):
                print(f"{item_path} is expected to be a directory")
            elif item_type == "file" and not os.path.isfile(item_path):
                print(f"{item_path} is expected to be a file")

def getCustomConfig(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def createWorkSpace(workspace_name, directory_structure=None):
    if directory_structure is None:
        directory_structure = {
            "production": ["inventory file for production servers"],
            "staging": ["inventory file for staging environment"],
            "group_vars": ["group1.yml", "group2.yml"],
            "host_vars": ["hostname1.yml", "hostname2.yml"],
            "library": [],
            "module_utils": [],
            "filter_plugins": [],
            "roles": {
                "common": {
                    "tasks": ["main.yml"],
                    "handlers": ["main.yml"],
                    "templates": ["ntp.conf.j2"],
                    "files": ["bar.txt", "foo.sh"],
                    "vars": ["main.yml"],
                    "defaults": ["main.yml"],
                    "meta": ["main.yml"],
                    "library": [],
                    "module_utils": [],
                    "lookup_plugins": []
                },
                "webtier": {

                }
            },
            "site.yml": "",
            "webservers.yml": "",
            "dbservers.yml": ""
        }
    if not os.path.exists(workspace_name):
        os.mkdir(workspace_name)
    base_path = Path(workspace_name)
    create_directory_structure(base_path, directory_structure)

"""
    Privacy scan functions
"""
def scan_file_for_sensitive_info(file_path, patterns):
    with open(file_path, 'r') as file:
        content = file.read()
        for pattern in patterns['patterns']:
            matches = re.findall(pattern, content)
            if matches:
                print(f"Found sensitive information matching pattern '{pattern}' in file {file_path}: {matches}")

def scan_ansible_directory_for_sensitive_info(directory, patterns):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                scan_file_for_sensitive_info(file_path, patterns)



def main():
    parser = argparse.ArgumentParser(description="KaaS " + version)
    parser.add_argument("-c", "--create", nargs="+", help="create a KaaS workspace")
    parser.add_argument("-s", "--scan", nargs="+", help="scan a specific workspace")
    parser.add_argument("-ps", "--privacy-scan", nargs="+", help="scan a specific workspace if any privacy leaking in it")
    parser.add_argument("-p", '--policy', nargs="+", help="use a customized policy file(JSON)")
    parser.add_argument("-v", "--version", action="store_true", help="output the version of the kaas-admin")


    args = parser.parse_args()

    _c, _s, _p, _v, _ps = args.create, args.scan, args.policy, args.version, args.privacy_scan

    if _ps and not _p:
        print("Syntax error. A customized privacy policy file is required(-p)")
    if _p:
        if _c:
            createWorkSpace(_c[0], getCustomConfig(_p[0]))
        elif _s:
            check_directory_structure(_s[0], getCustomConfig(_p[0]))
        elif _ps:
            with open(_p[0], 'r') as f:
                sensitive_info_patterns = json.load(f)
            scan_ansible_directory_for_sensitive_info(_ps[0], sensitive_info_patterns)
    else:
        if _c:
            createWorkSpace(_c[0])
        elif _s:
            check_directory_structure(_s[0])

    if _v:
        print(version)

if __name__ == "__main__":
    main()



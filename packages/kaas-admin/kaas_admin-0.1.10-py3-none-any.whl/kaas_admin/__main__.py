import os
import sys
import json
import argparse
from pathlib import Path




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

def main():
    parser = argparse.ArgumentParser(description="KaaS v0.1.8")
    parser.add_argument("-c", "--create", nargs="+", help="create a KaaS workspace")
    parser.add_argument("-v", "--validate", nargs="+", help="scan a specific workspace")
    parser.add_argument("-p", "--policy", nargs="+", help="use a customized policy file(JSON)")

    args = parser.parse_args()

    _c, _v, _p = args.create, args.validate, args.policy

    if _p:
        if _c:
            createWorkSpace(_c[0], getCustomConfig(_p[0]))
        elif _v:
            check_directory_structure(_v[0], getCustomConfig(_p[0]))
    else:
        if _c:
            createWorkSpace(_c[0])
        elif _v:
            check_directory_structure(_v[0])

if __name__ == "__main__":
    main()



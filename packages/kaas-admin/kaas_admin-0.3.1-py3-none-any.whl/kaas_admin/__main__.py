import datetime
import hashlib
import os
import re
import sys
import json
import argparse
import yaml
import pytest
import shutil
import subprocess
from pathlib import Path
from tower_cli import get_resource


version="v0.3.1"
TIME_VALVE = 30

"""
    Create workspace functions
"""
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

"""
    Scan workspace functions
"""
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

"""
    Read poilcy file functions
"""
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

"""
    Unit test functions
"""
def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def test_ansible_yaml_files():
    for root, dirs, files in os.walk(ansible_directory):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                yaml_content = load_yaml_file(file_path)
                assert yaml_content is not None, f"Failed to load YAML file: {file_path}"
                for test_case in test_cases:
                    for field_name, expected_value in test_case.items():
                        print(field_name)
                        print(expected_value)
                        assert field_name in yaml_content, f"{file_path} doesn't contain field {field_name}"
                        assert yaml_content[field_name] == expected_value, f"{file_path} field {field_name} has unexpected value"

"""
    Upload an ansible project to the ansible tower
"""
# Commit the local project and generate an MD5
def generate_md5(project, fflag):
    md5_hash = hashlib.md5()
    versionFile = os.path.join(project, ".version")
    # try:
    if os.path.isfile(project):
        with open(project, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                md5_hash.update(chunk)
    elif os.path.isdir(project):
        for root, dirs, files in os.walk(project):
            if ".version" in files:
                files.remove(".version")
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        md5_hash.update(chunk)
    md5v = md5_hash.hexdigest()
    if fflag==1:
        with open(os.path.join(project, '.version'), 'w+') as f:
            f.write(md5v)

    return md5v
    # except IOError:
    #     return None

def check_md5(projectDir, old_md5=None):
    version_file = os.path.join(projectDir, ".version")
    with open(version_file, 'r') as f:
        old_md5 = f.read().strip()
    if generate_md5(projectDir, 0) == old_md5:
        print(f"{projectDir} MD5 not changed")
        return False
    else:
        print(f"{projectDir} MD5 changed!")
        return True

# upload function
def uploadToTower(username, password, tower_url, project_name, local_playbook_dir):
    if os.path.isfile(os.path.join(local_playbook_dir, ".version")):
        if check_md5(local_playbook_dir) == True:
            raise Exception("Detected changes had been made to your project. Please use --commit to commit first.")
    else:
        generate_md5(local_playbook_dir, 1)
    print("uploading the project...")
    with TowerCli(username=username, password=password, host=tower_url) as tower:
        projects = get_resource('project')

        project_data = {
            'name': project_name,
            'scm_type': 'manual',
        }
        created_project = projects.create(**project_data)

        for root, dirs, files in os.walk(local_playbook_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_playbook_dir)
                remote_file_path = f'{project_name}/{relative_path}'
                shutil.copy2(local_file_path, remote_file_path)

        print("Playbook directory uploaded to Tower.")

"""
    Run the specific ansible project in local
"""
def run_ansible_playbook(playbook_path, inventory_file):
    try:
        if sys.version_info >= (3, 7):
            process = subprocess.Popen(['ansible-playbook', '-i', inventory_file, playbook_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        else:
            process = subprocess.Popen(['ansible-playbook', '-i', inventory_file, playbook_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        output_lines = []
        task_start_times = {}
        current_task = None
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                output_lines.append(output.strip())
                if output.startswith("TASK"):
                    task_name = re.search(r'TASK \[(.*?)\]', output).group(1)
                    task_start_times[task_name] = datetime.datetime.now()
                    current_task = task_name

                if output.startswith("ok:") or output.startswith("changed:") or output.startswith("failed:") or output.startswith("ERROR!"):
                    if current_task:
                        start_time = task_start_times[current_task]
                        end_time = datetime.datetime.now()
                        duration = end_time - start_time
                        print("Task {} executed for {}".format(current_task, duration))
        process.wait()
        total_duration = datetime.timedelta()
        for task_name, start_time in task_start_times.items():
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            if duration.total_seconds() > TIME_VALVE:
                print("NEED ATTENTION -> Task [{}] took longer than {} seconds.".format(task_name, TIME_VALVE))
            total_duration += duration

        print("Total execution time: {}".format(total_duration))

    except subprocess.CalledProcessError as e:
        print("Failed to run ansible-playbook:", e)


"""
    Create a Sample ansible playbook(yaml)
"""
def create_sample_playbook(project_path, playbook_name):
    playbook_content = '''---
- name: Sample Playbook
  hosts: localhost
  tasks:
    - name: Print Hello World
      debug:
        msg: "Hello World"
'''

    playbook_path = os.path.join(project_path, playbook_name + ".yaml")
    with open(playbook_path, 'w') as playbook_file:
        playbook_file.write(playbook_content)

    print("Sample playbook created at: {}".format(playbook_path))

"""
    add an ansible role to the KaaS project
"""
def create_ansible_role(base_path, role_name):
    directory_structure = {
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
    }
    role_path = os.path.join(base_path, 'roles', role_name)
    try:
        os.makedirs(role_path, exist_ok=True)

        for directory, files in directory_structure.items():
            directory_path = os.path.join(role_path, directory)
            os.makedirs(directory_path, exist_ok=True)
            for file in files:
                with open(os.path.join(directory_path, file), "w") as f:
                    if file.endswith(".yml"):
                        f.write("# Your YAML content goes here\n")
                    elif file.endswith(".j2"):
                        f.write("# Your Jinja2 template content goes here\n")
                    else:
                        f.write("# Content of {}\n".format(file))
        print("Ansible role '{}' created at: {}".format(role_name, role_path))

    except Exception as e:
        print("Failed to create Ansible role:", e)


"""
    Main function
"""
def main():
    parser = argparse.ArgumentParser(description="KaaS " + version)
    parser.add_argument("-c", "--create", nargs="+", help="create a KaaS workspace")
    parser.add_argument("-s", "--scan", nargs="+", help="scan a specific workspace")
    parser.add_argument("-ps", "--privacy-scan", nargs="+", help="scan a specific workspace if any privacy leaking in it")
    parser.add_argument("-ss", "--sensitive-scan", nargs="+", help="scan a specific workspace if any sensitive commands in it")
    parser.add_argument("-p", "--policy", nargs="+", help="use a customized policy file(JSON)")
    parser.add_argument("-t", "--test", nargs="+", help="unit test for a yaml file")
    parser.add_argument("--commit", nargs="+", help="commit a KaaS project")
    parser.add_argument("-v", "--version", action="store_true", help="output the version of the kaas-admin")

    groupE = parser.add_argument_group('execute an KaaS project')
    groupE.add_argument("-e", "--execute", nargs="+", help="run an ansible project in local")
    groupE.add_argument("-i", "--inventory", nargs="+", help="inventory host")

    groupA = parser.add_argument_group('add resources to the KaaS project')
    groupA.add_argument("--add", action='store_true', help="add resources to the KaaS project")
    groupA.add_argument("--playbook", nargs="+", help="add an ansible playbook")
    groupA.add_argument("--role", nargs="+", help="add an ansible roles")

    group = parser.add_argument_group('connect to the ansible tower')
    group.add_argument("--connect", action='store_true', help="Connect to an ansible tower")
    group.add_argument("--url", nargs="+", help="Which url do connect to")
    group.add_argument("--username", nargs="+", help="Ansible tower login user name")
    group.add_argument("--password", nargs="+", help="Ansible tower login password")
    group.add_argument("--local-project", nargs="+", help="upload an local project")
    group.add_argument("--remote-project", nargs="+", help="specify which ansible project you're connecting to")


    args = parser.parse_args()

    _c, _s, _p, _v, _ps, _ss, _t = args.create, args.scan, args.policy, args.version, args.privacy_scan, args.sensitive_scan, args.test
    _co, _u, _us, _pa, _lp, _rp = args.connect, args.url, args.username, args.password, args.local_project,args.remote_project
    _e, _i = args.execute, args.inventory
    _a, _pl, _ro = args.add, args.playbook, args.role
    _com = args.commit

    if _com:
        generate_md5(_com[0], 1)

    if _a:
        if _pl:
            create_sample_playbook(_pl[0], _pl[1])
            return
        if _ro:
            create_ansible_role(_ro[0], _ro[1])
            return
        else:
            raise Exception("Missing a required parameters(--playbook or --role)")

    if _co:
        # try:
        uploadToTower(_us[0], _pa[0], _u[0], _rp[0], _lp[0])
        # except:
        #     print("An exception occur while uploading to the Ansible Tower. You might be missing some required parameters from (username, password, tower_url, project_name, local_playbook_dir)")
        #     print("Use -h to check for the required input parameters.")
        return

    if _e:
        if _i:
            run_ansible_playbook(_e[0], _i[0])
            return
        else:
            print("Syntax error. an inentory file must be specified(-i)")
            return

    if _ps and not _p:
        print("Syntax error. A customized privacy policy file is required(-p)")
        return
    if _ss and not _p:
        print("Syntax error. A customized privacy policy file is required(-p)")
        return
    if _t and not _p:
        print("Syntax error. A customized privacy policy file is required(-p)")
        return
    if _p:
        if _c:
            createWorkSpace(_c[0], getCustomConfig(_p[0]))
        elif _s:
            check_directory_structure(_s[0], getCustomConfig(_p[0]))
        elif _ps:
            with open(_p[0], 'r') as f:
                sensitive_info_patterns = json.load(f)
            scan_ansible_directory_for_sensitive_info(_ps[0], sensitive_info_patterns)
        elif _ss:
            with open(_p[0], 'r') as f:
                sensitive_info_patterns = json.load(f)
            scan_ansible_directory_for_sensitive_info(_ss[0], sensitive_info_patterns)
        elif _t:
            global ansible_directory, test_cases
            ansible_directory= _t[0]
            with open(_p[0], 'r') as f:
                test_cases = json.load(f)
            pytest.main([__file__])
    else:
        if _c:
            createWorkSpace(_c[0])
        elif _s:
            check_directory_structure(_s[0])

    if _v:
        print(version)

if __name__ == "__main__":
    main()



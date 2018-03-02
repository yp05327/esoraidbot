# utf-8
import json
import os
import sys
import requests

github_raw_url = "https://raw.githubusercontent.com/yp05327/esoraidbot/master/"

def read(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            jsoninfo = json.load(f)

        print("Read file %s success." % file_name)

    else:
        jsoninfo = {}
        save(file_name, jsoninfo)
        print("Init file %s success." % file_name)

    return jsoninfo

def save(file_name, info):
    with open(file_name, "w") as f:
        json.dump(info, f)

def read_version():
    if os.path.exists('version'):
        with open('version', 'r') as f:
            version = json.load(f)

        return version
    else:
        return False

def checkupdate():
    return json.loads(requests.get(github_raw_url + 'version').content)

def update():
    update_list = json.loads(requests.get(github_raw_url + 'update').content)
    for file_name in update_list['file_name']:
        file_info = requests.get(github_raw_url + file_name).content.decode(encoding='utf-8')
        with open(file_name, "w") as f:
            f.write(file_info)

    # check config.json
    exp_configs = read("config.example.json")
    configs = read("config.json")
    for config in exp_configs:
        if config not in configs:
            configs[config] = exp_configs[config]

    save("config.json", configs)

    # requirements
    os.system("pip install -r requirements.txt")

    # restart
    python = sys.executable
    os.execl(python, python, * sys.argv)





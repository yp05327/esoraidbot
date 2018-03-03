# utf-8
import json
import os
import sys
import requests
import time
import datetime

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

def change_timezone(year, month, day, hour, minute, timezone, new_timezone):
    timezone = datetime.timezone(datetime.timedelta(hours=timezone))
    new_timezone = datetime.timezone(datetime.timedelta(hours=new_timezone))
    return datetime.datetime(year, month, day, hour, minute, tzinfo=timezone).replace(tzinfo=timezone).astimezone(tz=new_timezone)

def get_timetick(year, month, day, hour, minute, timezone):
    # change time to UTC time tick
    dt = change_timezone(year, month, day, hour, minute, timezone, 0)

    return time.mktime(time.strptime(dt.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))

def get_time(tick, timezone):
    dt = datetime.datetime.fromtimestamp(tick)
    dt = change_timezone(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, timezone)
    return dt.year, dt.month, dt.day, dt.hour, dt.minute

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

    # update version
    version = read_version()
    new_version = checkupdate()
    if version:
        version[0:4] = new_version[0:4]
        save('version', version)
    else:
        print("Can't read version file, update failed.")

    # restart
    python = sys.executable
    os.execl(python, python, * sys.argv)

def check_out_of_date_event(raidinfo, file_name):
    for event in raidinfo:
        utc_now = datetime.datetime.utcnow()
        utc_now = get_timetick(utc_now.year, utc_now.month, utc_now.day, utc_now.hour, utc_now.minute, 0)
        if utc_now - event['time'] - 3600 * 2 >= 0:
            del raidinfo[event]
            save(file_name, raidinfo)



# utf-8

import utils

info = {}

# read config
def read():
    global info
    info = utils.read("config.json")
    # check info
    if not 'installed' in info:
        print("Config File Check Error:Not have 'installed' in config.json")
        return False

    if not 'token' in info:
        print("Config File Check Error:Not have 'token' in config.json")
        return False
    elif info['token'] == "":
        print("Config File Check Error:Please input 'token' into config.json")
        return False

    if not 'record_file_name' in info:
        print("Config File Check Error:Not have 'record_file_name' in config.json")
        return False
    elif info['record_file_name'] == "":
        print("Config File Check Error:Please input 'record_file_name' into config.json")
        return False

    if not 'role_list' in info:
        print("Config File Check Error:Not have 'role_list' in config.json")
        return False
    elif info['role_list'] == "":
        print("Config File Check Error:Please input 'role_list' into config.json")
        return False

    if not 'superadmin' in info:
        print("Config File Check Error:Not have 'superadmin' in config.json")
        return False

    if not 'admin_list' in info:
        print("Config File Check Error:Not have 'admin_list' in config.json")
        return False

    return True

def save():
    utils.save('config.json', info)

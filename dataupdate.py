# utf-8
import utils
import datetime

def changedata(config, old_version, new_version):
    # no new version to change
    while old_version < new_version:
        old_version = updatedata(config, old_version)

    # update version
    version = utils.read_version()
    if version:
        version[4] = new_version
        utils.save('version', version)
    else:
        print("Can't read version file, update data version failed.")

def updatedata(config, oldversion):
    if oldversion == 1:
        old_record = utils.read(config['record_file_name'])
        new_record = {}
        if config['superadmin'] == "":
            print("Update Info: Don't have superadmin, dataupdate failed")
        for event in old_record:
            new_record[event] = {'owner': config['superadmin'], 'time': datetime.datetime.utcnow(), "players": old_record[event]}
        return 2
# utf-8
import discord

import config
import utils
import dataupdate
import random

client = discord.Client()
raidinfo = {}
trials = ['aa','so', 'as', 'hrc', 'mol', 'hof']

@client.event
async def on_ready():
    global raidinfo
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    raidinfo = utils.read(config.info['record_file_name'])

@client.event
async def on_message(message):
    utils.check_out_of_date_event(raidinfo, config.info['record_file_name'])
    if message.content.startswith("!allraid"):
        if client.user != message.author:
            if raidinfo is {}:
                await client.send_message(message.channel, "No available event now.")
            else:
                if len(message.content) > 12:
                    timezone = int(message.content[12:])
                else:
                    timezone = 0

                events = ""
                for event in raidinfo:
                    year, month, day, hour, minute = utils.get_time(raidinfo[event]['time'], timezone)
                    events += event + "(%d)  %d-%d-%d %d:%d\n" % (len(raidinfo[event]['players']), year, month, day, hour, minute)

                em = discord.Embed(title="Available Events", description=events,colour=0xFFFF00)
                await client.send_message(message.channel, embed=em)

    if message.content.startswith("!status"):
        if client.user != message.author:
            _message = message.content[8:].split('-')

            event_name = _message[0]
            if len(_message) == 2:
                timezone = int(_message[1][3:])
            else:
                timezone = 0

            if event_name is not "":
                if event_name in raidinfo:
                    player_list = ""
                    for player in raidinfo[event_name]['players']:
                        role = raidinfo[event_name]['players'][player]
                        player_list += config.info['role_list'][role] + "   %s\n" % player

                    if player_list == "":
                        player_list = "No player had joined this event."

                    year, month, day, hour, minute = utils.get_time(raidinfo[event_name]['time'], timezone)
                    em = discord.Embed(title="%s Created by %s Time: %d-%d-%d %d:%d" % (event_name, raidinfo[event_name]['owner'], year, month, day, hour, minute),description=player_list, colour=0xFF0000)

                    await client.send_message(message.channel, embed=em)
                else:
                    await client.send_message(message.channel, "Not have this event.")
            else:
                 await client.send_message(message.channel, "Please use !status raidname.")

    if message.content.startswith("!join"):
        if client.user != message.author:
            _message = message.content[6:].split('#')
            if len(_message) != 2:
                await client.send_message(message.channel, "Wrong input,please check your input.")
                return
            else:
                event_name = _message[0]
                role = _message[1]
                if event_name == "" or role == "":
                    await client.send_message(message.channel, "Wrong input,please check your input.")
                    return

            # change char to int
            if role in config.info['role_list']:
                role = config.info['role_list'].index(role)
            else:
                try:
                    role = int(role)
                except:
                    await client.send_message(message.channel, "Wrong role,please check your input.")
                    return

            if role >= len(config.info['role_list']):
                await client.send_message(message.channel, "Wrong role,please check your input.")
                return

            if event_name in raidinfo:
                raidinfo[event_name]['players'][message.author.name] = role
                utils.save(config.info['record_file_name'], raidinfo)
                em = discord.Embed(title="%s has joined %s" % (message.author.name, event_name), description="Role:" + config.info['role_list'][role], colour=0x0000FF)
                await client.send_message(message.channel, embed=em)
            else:
                await client.send_message(message.channel, "Can't find this event.")

    if message.content.startswith("!gugugu"):
        if client.user != message.author:
            event_name = message.content[8:]
            if event_name is not "":
                if message.author.name in raidinfo[event_name]['players']:
                    del raidinfo[event_name]['players'][message.author.name]
                    utils.save(config.info['record_file_name'], raidinfo)
                    em = discord.Embed(title="%s has unjoined %s" % (message.author.name, event_name), description="", colour=0x00FF00)
                    await client.send_message(message.channel, embed=em)
                else:
                    await client.send_message(message.channel, "You have not joined this event.Use !join eventname#role to join.")
            else:
                await client.send_message(message.channel, "Please use !gugugu eventname.")

    if message.content.startswith("!checkname"):
        if client.user != message.author:
            await client.send_message(message.channel, message.author.name)

    if message.content.startswith("!random"):
        if client.user != message.author:
            await client.send_message(message.channel, random.choice(trials))

    # admin command
    if message.content.startswith("!create"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list']  or message.author.name == config.info['superadmin']:
                _message = message.content[8:]
                # check # char
                _message = _message.replace('#', '')

                _message = _message.split('-')
                if len(_message) > 7:
                    await client.send_message(message.channel, "Wrong input,please check your input.")
                    return
                elif len(_message) == 6:
                    timezone = 0
                else:
                    timezone = int(_message[6][3:])

                event_name = _message[0]
                year = int(_message[1])
                month = int(_message[2])
                day = int(_message[3])
                hour = int(_message[4])
                minute = int(_message[5])

                if event_name == "" or year == "" or month == "" or day == "" or hour == "" or minute == "" or timezone == "":
                    await client.send_message(message.channel, "Wrong input,please check your input.")
                    return

                if event_name in raidinfo:
                    await client.send_message(message.channel, "Raid %s existed.Use !delete eventname to delete." % event_name)
                else:
                    raidinfo[event_name] = {'owner': message.author.name, 'time': utils.get_timetick(year, month, day, hour, minute, timezone), 'players': {}}
                    utils.save(config.info['record_file_name'], raidinfo)
                    await client.send_message(message.channel, "Raid %s created." % event_name)
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!changetime"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list'] or message.author.name == config.info['superadmin']:
                _message = message.content[12:]
                _message = _message.split('-')
                if len(_message) > 7:
                    await client.send_message(message.channel, "Wrong input,please check your input.")
                    return
                elif len(_message) == 6:
                    timezone = 0
                else:
                    timezone = int(_message[6][3:])

                event_name = _message[0]
                year = int(_message[1])
                month = int(_message[2])
                day = int(_message[3])
                hour = int(_message[4])
                minute = int(_message[5])

                if event_name == "" or year == "" or month == "" or day == "" or hour == "" or minute == "" or timezone == "":
                    await client.send_message(message.channel, "Wrong input,please check your input.")
                    return

                if message.author.name == raidinfo[event_name]['owner']:
                    if event_name in raidinfo:
                        raidinfo[event_name]['time'] = utils.get_timetick(year, month, day, hour, minute, timezone)
                        await client.send_message(message.channel, "Raid %s time changed." % event_name)
                    else:
                        await client.send_message(message.channel,"Can't find raid %s." % event_name)

                else:
                    await client.send_message(message.channel, "Only the owner of this event or superadmin can change time.")

            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!delete"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list']  or message.author.name == config.info['superadmin']:
                event_name = message.content[8:]
                if event_name is not "":
                    del raidinfo[event_name]
                    utils.save(config.info['record_file_name'], raidinfo)
                    await client.send_message(message.channel, "Raid %s deleted." % event_name)
                else:
                    await client.send_message(message.channel, "Please use !delete raidname.")
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!update"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list'] or message.author.name == config.info['superadmin']:
                utils.update()
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!checkupdate"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list'] or message.author.name == config.info['superadmin']:
                _version = utils.checkupdate()
                if _version != version:
                    await client.send_message(message.channel, "ESO Raid Bot by Doa new version found: %d.%d.%d-%s(now %d.%d.%d-%s).Please use !update to update." % \
                                              (_version[0], _version[1], _version[2], _version[3], version[0], version[1], version[2], version[3]))
                else:
                    await client.send_message(message.channel, "Now is the latest version(ESO Raid Bot by Doa Version %d.%d.%d-%s, Data Version %d)." % \
                                              (version[0], version[1], version[2], version[3], version[4]))
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!version"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list'] or message.author.name == config.info['superadmin']:
                await client.send_message(message.channel, "ESO Raid Bot by Doa Version %d.%d.%d-%s, Data Version %d." % (version[0], version[1], version[2], version[3], version[4]))
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # first command
    if message.content.startswith("!install"):
        if client.user != message.author:
            if not config.info['installed']:
                config.info['installed'] = True
                config.info['superadmin'] = message.author.name
                if not message.author.name in config.info['admin_list']:
                    config.info['admin_list'].append(message.author.name)
                config.save()
                await client.send_message(message.channel, "Installed by %s." % message.author.name)
            else:
                await client.send_message(message.channel, "Has been installed.")
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")

    # superadmin command
    if message.content.startswith("!alladmin"):
        if client.user != message.author:
            # check permission
            if message.author.name == config.info['superadmin']:
                admin_list = ""
                for admin in config.info['admin_list']:
                    admin_list += "%s\n" % admin

                em = discord.Embed(title="All Admin List", description=admin_list,colour=0x000000)
                await client.send_message(message.channel, embed=em)
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # superadmin command
    if message.content.startswith("!addadmin"):
        if client.user != message.author:
            # check permission
            if message.author.name == config.info['superadmin']:
                admin_name = message.content[10:]
                if admin_name in config.info['admin_list']:
                    await client.send_message(message.channel, "This user is already admin.")
                else:
                    config.info['admin_list'].append(admin_name)
                    config.save()
                    await client.send_message(message.channel, "Admin %s added." % admin_name)
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # superadmin command
    if message.content.startswith("!deladmin"):
        if client.user != message.author:
            # check permission
            if message.author.name == config.info['superadmin']:
                admin_name = message.content[10:]
                if admin_name in config.info['admin_list']:
                    config.info['admin_list'].remove(admin_name)
                    config.save()
                    await client.send_message(message.channel, "Admin %s deleted.." % admin_name)
                else:
                    await client.send_message(message.channel, "Admin %s not found." % admin_name)
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    if message.content.startswith("!help"):
        if client.user != message.author:
            role_string = ""
            for role in config.info['role_list']:
                role_string += role + "(%d)/" % config.info['role_list'].index(role)

            # normal command
            help_string = "!allraid\nShow all avaliable events.Default timezone is UTC, you can use !allraid UTC+8 to show UTC+8 time.\n\n" \
                          "!status eventname\nTo show the status of a event.Default timezone is UTC, you can use !status eventname-UTC+8 to show UTC+8 time.\n\n" \
                          "!join eventname#role\nTo join a event.Role code is " + role_string + "\n\n" \
                          "!gugugu eventname\nTo unjoin a event.\n\n" \
                          "!checkname\nTo print your user name.\n\n" \
                          "!random\nTo show a random trial."
            em = discord.Embed(title="Normal Command You Can Use", description=help_string, colour=0x00FFFF)
            await client.send_message(message.channel, embed=em)

            # admin command
            if message.author.name in config.info['admin_list']:
                help_string = "!create eventname-year-month-day-hour-minute\nCreate a new event.Don't use '#' and '-' in event name.\nDefault timezone is UTC, you can use !create eventname-year-month-day-hour-minute-UTC+8 to create UTC+8 time event.\n\n" \
                              "!changetime eventname-year-month-day-hour-minute\nChange event time.Only the owner of the event and superadmin can change time.\nDefault timezone is UTC, you can use !changetime eventname-year-month-day-hour-minute-UTC+8 to create UTC+8 time event.\n\n" \
                              "!delete eventname\nTo delete a event.\n\n" \
                              "!update\nTo check and update new version.\n\n" \
                              "!checkupdate\nTo check new version\n\n" \
                              "!version\nTo show version."
                em = discord.Embed(title="Admin Command You Can Use", description=help_string, colour=0x00FFFF)
                await client.send_message(message.channel, embed=em)
            # superadmin command
            if message.author.name == config.info['superadmin']:
                help_string = "!install\nTo set yourself superadmin, only can be used once.\n\n" \
                              "!alladmin\nTo show all admin user list.\n\n" \
                              "!addadmin username\nTo add admin user.Please input !checkname to check user name first.\n\n" \
                              "!deladmin username\nTo delete admin user.You can use !alladmin to check all admin username."

                em = discord.Embed(title="SuperAdmin Command You Can Use", description=help_string, colour=0x00FFFF)
                await client.send_message(message.channel, embed=em)

if config.read():
    version = utils.read_version()
    if version:
        # check data type
        if utils.checkupdate()[4] > version[4]:
            print("Found new Data version. Changing...")
            dataupdate.changedata(config.info, version[4], utils.checkupdate()[4])
            print("Changed.")

        client.run(config.info['token'])
    else:
        print("Can't find file: version.")
else:
    print("Read config failed.Please check config.json.")
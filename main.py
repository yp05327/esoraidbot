# utf-8
import discord

import config
import utils
import dataupdate

client = discord.Client()
raidinfo = {}

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
    if message.content.startswith("!all"):
        if client.user != message.author:
            if raidinfo is {}:
                await client.send_message(message.channel, "No available event now.")
            else:
                events = ""
                for event in raidinfo:
                    events += event + "(%d)\n" % len(raidinfo[event])

                em = discord.Embed(title="Available Events", description=events,colour=0xFFFF00)
                await client.send_message(message.channel, embed=em)

    if message.content.startswith("!status"):
        if client.user != message.author:
            event_name = message.content[8:]
            if event_name is not "":
                if event_name in raidinfo:
                    player_list = ""
                    for player in raidinfo[event_name]:
                        role = raidinfo[event_name][player]
                        player_list += config.info['role_list'][role] + "   %s\n" % player

                    if player_list == "":
                        player_list = "No player had joined this event."

                    em = discord.Embed(title=event_name,description=player_list, colour=0xFF0000)
                    await client.send_message(message.channel, embed=em)
                else:
                    await client.send_message(message.channel, "Not have this event.")
            else:
                 await client.send_message(message.channel, "Please use !status raidname.")

    if message.content.startswith("!join"):
        if client.user != message.author:
            _message = message.content[6:].split('#')
            event_name = _message[0]
            role = _message[1]
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
                raidinfo[event_name][message.author.name] = role
                utils.save(config.info['record_file_name'], raidinfo)
                em = discord.Embed(title="%s has joined $s" % (message.author.name, event_name), description="Role:" + config.info['role_list'][role], colour=0x0000FF)
                await client.send_message(message.channel, embed=em)
            else:
                await client.send_message(message.channel, "Can't find this event.")

    if message.content.startswith("!gugugu"):
        if client.user != message.author:
            event_name = message.content[8:]
            if event_name is not "":
                if message.author.name in raidinfo[event_name]:
                    del raidinfo[event_name][message.author.name]
                    utils.save(config.info['record_file_name'], raidinfo)
                    em = discord.Embed(title="%s has unjoined $s" % (message.author.name, event_name), description="", colour=0x00FF00)
                    await client.send_message(message.channel, embed=em)
                else:
                    await client.send_message(message.channel, "You have not joined this event.Use !join eventname#role to join.")
            else:
                await client.send_message(message.channel, "Please use !gugugu eventname.")

    if message.content.startswith("!checkname"):
        if client.user != message.author:
            await client.send_message(message.channel, message.author.name)

    # admin command
    if message.content.startswith("!create"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list']:
                event_name = message.content[8:]
                # check # char
                event_name = event_name.replace('#', '')
                if event_name is not "":
                    raidinfo[event_name] = {}
                    utils.save(config.info['record_file_name'], raidinfo)
                    await client.send_message(message.channel, "Raid %d created." % event_name)
                else:
                    await client.send_message(message.channel, "Please use !create raidname.")
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!delete"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list']:
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
            if message.author.name in config.info['admin_list']:
                utils.update()
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # admin command
    if message.content.startswith("!checkupdate"):
        if client.user != message.author:
            # check permission
            if message.author.name in config.info['admin_list']:
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
            if message.author.name in config.info['admin_list']:
                await client.send_message(message.channel, "ESO Raid Bot by Doa Version %d.%d.%d-%s, Data Version %d." % (version[0], version[1], version[2], version[3], version[4]))
            else:
                await client.send_message(message.channel, "You do not have permission to use this command.")

    # superadmin command
    if message.content.startswith("!install"):
        if client.user != message.author:
            # check permission
            if message.author.name == config.info['superadmin']:
                if config.info['installed'] == False:
                    config.info['superadmin'] = message.author.name
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
            help_string = "!all\nShow all avaliable events.\n\n" \
                          "!status eventname\nTo show the status of a event.\n\n" \
                          "!join eventname#role\nTo join a event.Role code is " + role_string + "\n\n" \
                          "!gugugu eventname\nTo unjoin a event.\n\n" \
                          "!checkname\nTo print your user name."
            em = discord.Embed(title="Normal Command You Can Use", description=help_string,
                               colour=0x00FFFF)
            await client.send_message(message.channel, embed=em)

            # admin command
            if message.author.name in config.info['admin_list']:
                help_string = "!create eventname\nCreate a new event.Dont use '#' in event name\n\n" \
                              "!delete eventname\nTo delete a event.\n\n" \
                              "!update\nTo check and update new version.\n\n" \
                              "!checkupdate\nTo check new version\n\n" \
                              "!version\nTo show version."
                em = discord.Embed(title="Admin Command You Can Use", description=help_string,
                                   colour=0x00FFFF)
                await client.send_message(message.channel, embed=em)
            # superadmin command
            if message.author.name == config.info['superadmin']:
                help_string = "!install\nTo set yourself superadmin, only can be used once.\n\n" \
                              "!alladmin\nTo show all admin user list.\n\n" \
                              "!addadmin username\nTo add admin user.Please input !checkname to check user name first.\n\n" \
                              "!deladmin username\nTo delete admin user.You can use !alladmin to check all admin username."

                em = discord.Embed(title="SuperAdmin Command You Can Use", description=help_string,
                                   colour=0x00FFFF)
                await client.send_message(message.channel, embed=em)

if config.read():
    version = utils.read_version()
    if version:
        # check data type
        if utils.checkupdate()[4] > version[4]:
            print("Found new Data version. Changing...")
            dataupdate.changedata(version[4], utils.checkupdate()[4])
            print("Changed.")

        client.run(config.info['token'])
    else:
        print("Can't find file: version.")
else:
    print("Read config failed.Please check config.json.")
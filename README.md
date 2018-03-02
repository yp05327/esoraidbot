# Eso Raid Bot
A Discrod Bot for Elder Scroll Online. Powered by TenderLunar_YP of Dragon of Asia Guild. 

Author HP: https://lunareso.peryp.com 

Guild HP: https://doa-eso.com

[中文教程](https://github.com/yp05327/esoraidbot/blob/master/README-CN.md)

# Guild
* Requirment

    A server with python >= 3.5, this project is developed under python 3.6.1 so I suggest to install this version.
    
* How to install

    1.Open Discord Development HP:https://discordapp.com/developers/applications/me
    
    2.Press 'New App' to add a new app
    
    3.Then input a App Name, and Press 'Create App'
    
    4.At the setting page, Press 'Create a Bot User' and 'Yes, do it!'
    
    5.Then get your Token and Press 'Public Bot', you need to paste your Token into config.json, we will do this later.
    
    6.Then Press 'Generate OAuth2 URL', in 'SCOPES' only choose 'bot' and you will see OAuth2 URL, Press 'COPY' to copy it .
    
    7.If you have logined, visit the OAuth2 URL, then you can add this bot to your discord server.
    
        Then, The Most Important Step, Back To The Settings Page of Your Discord App, 
        
        Change 'Public Bot' Into 'Require OAuth2 Code Grant' or Do Not Select Any of Them.
        
        Don't forgot to Press 'Save changes'.If you dont do this, any other people who knows your 
        
        OAuth2 URL can use your bot at any discord server and have permission to use any normal command.
    
    8.Find config.example.json file of this project, copy it and change name into config.json.Then open config.json by Notepad or other tools, and paste your Token and save.
    
    9.Go to the root of this project, run 'pip install -r requirements.txt' to install requirements.If you don't have pip, see: https://pip.pypa.io/en/stable/installing/
    
    10.Last, run 'python3 main.py' on your server.
    
* How to use

    Normally, input commands start with '!' in chat channel.You can set permission to this bot and lock in bot channel.
    
    1.Set SuperAdmin
        
    Only one user can be super admin so the first user who input '!install' command will be super admin, or you can change config.json to set super admin.
    
    2.Use '!help' command to see all commands supported.
    
    3.HAVE FUN :D
    

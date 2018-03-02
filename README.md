# Eso Raid Bot
A discrod bot for elder scroll online. Powered by TenderLunar_YP of Dragon of Asia Guild. 

Author HP: https://lunareso.peryp.com 

Guild HP: https://doa-eso.com

# Guild
* Requirment

    A server with python >= 3.5, this project is developed under python 3.6.1 so I suggest to install this version.
    
* How to install

    1.Open Discord Development HP:https://discordapp.com/developers/applications/me
    
    2.Press 'New App' to add a new app
    
    3.Then input a App Name, and Press 'Create App'
    
    4.At the setting page, Press 'Create a Bot User' and 'Yes, do it!'
    
    5.Then get your Token and Press 'Public Bot', you need to paste into config.json, we will do this later.
    
    6.Then Press 'Generate OAuth2 URL', in 'SCOPES' only choose 'bot' and you will see one OAuth2 URL, Press 'COPY' .
    
    7.If you have logined, visit the OAuth2 URL, then you can add this bot to your server.
    
        Then, The Most Important Step, Back To The Settings Page of Your Discord App, Change 'Public Bot' Into 'Require OAuth2 Code Grant' or Do Not Select Any of Them.
        
        If you dont do this, any other people who knows your OAuth2 URL can use your bot at any discord server and can use any normal command.
    
    8.Find config.example.json of this project, copy it and change name into config.json.Then open config.json in Notepad, and paste your Token and save.
    
    9.Go to the root of this project, run 'pip install -r requirements.txt' to install requirements.If you don't have pip, see: https://pip.pypa.io/en/stable/installing/
    
    10.Last, run 'python3 main.py' on your server
    
* How to use

    Normally input commands start with '!' in channel.You can set permission to this bot and lock in bot channel.
    
    1.Set SuperAdmin
        
    Only one user can be super admin so the first user who input '!install' will be super admin, or you can change config.json to set super admin.
    
    2.Use '!help' to see all commands supported.
    

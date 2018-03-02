# Eso Raid Bot
一个 Elder Scroll Online 的 Discrod Bot 程序. 由Dragon of Asia工会TenderLunar_YP编写.

作者主页: https://lunareso.peryp.com 

工会主页: https://doa-eso.com

# 指南
* 需求

    一个安装有 python版本>= 3.5的服务器, 由于这个项目是在python 3.6.1之下开发的因此我建议安装此版本.
    
* 如何安装

    1.打开 Discord 开发者主页:https://discordapp.com/developers/applications/me
    
    2.点击 'New App' 来添加一个新的App
    
    3.输入一个 App 名称, 然后点击 'Create App'
    
    4.在设置页面点击 'Create a Bot User' 和 'Yes, do it!'
    
    5.然后获取你的 Token 并选择 'Public Bot', 你需要复制你的 Token 到 config.json, 我们将在稍后进行此步骤.
    
    6.然后点击 'Generate OAuth2 URL', 在 'SCOPES' 中仅选中 'bot' 然后你会看到 OAuth2 URL, 点击 'COPY' 来复制它.
    
    7.如果你已经登录, 访问 OAuth2 URL 链接, 然后你就可以把这个 bot 添加到你的 discord 服务器.
    
        然后是最为重要的一步, 返回你的 Discord App 的设置页面, 修改 'Public Bot' 为 'Require OAuth2 Code Grant' 
        
        或者一个都不要选择.不要忘了点击 'Save changes'.如果你不这么做的话, 任何一个知道你的 OAuth2 URL 的人都可以
        
        在任何 discord 服务器使用你的 bot 并且有权限运行任何普通指令.
    
    8.找到 config.example.json 文件, 复制并修改名称为 config.json.然后用记事本或其他工具打开 config.json , 黏贴你的 Token 并保存.
    
    9.转到项目的根目录, 运行 'pip install -r requirements.txt' 来安装运行所需求的环境.如果你没有 pip, 请看此处: https://pip.pypa.io/en/stable/installing/
    
    10.最后, 在你的服务器上运行 'python3 main.py'.
    
* 如何使用

    一般地, 在聊天频道输入以 '!' 开头的指令.你可以设置这个 bot 的权限然后锁定在一个 bot 频道.
    
    1.设置超级管理员(Super Admin)
        
    只有一个用户可以成为超级管理员, 所以第一个输入 '!install' 指令的用户 将成为超级管理员, 或者你可以修改 config.json 来设置超级管理员.
    
    2.使用 '!help' 指令来查看所有支持的指令.
    
    3.祝您使用愉快 ;D
    

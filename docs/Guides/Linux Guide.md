#Requirements

**Python 3.5+**

**Git**



#Installing Requirements

Open your console/terminal and type the following
```
apt install git
apt install python3
```



#Installing Quote & Editing Credentials

Open your console/terminal and type `git clone https://github.com/Deivedux/Quote.git`

Next step is editing the credentials.

Head to the configs folder by typing `cd Quote/configs`

To edit `config.json`, type `nano config.json`

`token`, enter your bot token which can be found at [Discord Developers Page](https://discordapp.com/developers/applications/me). *See  GIF below.*
![](http://i.imgur.com/jaxgi2P.gif)

`default_prefix`, the default prefix of your Quote bot. You can change it to whatever you like.

`owner_ids`, these are the IDs of users who can use the owner only commands, including yourself. *See how to get IDs in the GIF below.*

![](http://i.imgur.com/UQxBZfJ.gif)

After you found out and copied your owner ID and the bot's token, your `config.json` should look something like this.

![](https://i.imgur.com/MHjaCqh.png)


# Inviting Your Bot

Last but not least, inviting your bot.

Replace `<bot_id>` with your bot's ID in this link: `https://discordapp.com/oauth2/authorize?client_id=<bot id>&permissions=84992&scope=bot`

Once you replaced `<bot_id>` with your bot's ID, copy the link in a new tab (the current tab also works) and select your server.

After that, you're all set. If you have any questions, ask in the [Official Support Server](https://discord.gg/sbySHxA).
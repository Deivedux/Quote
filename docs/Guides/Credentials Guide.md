# Requirements

> Notepad++ (Or some other decent text editing software.)

---

# Explanation Of Features

> `token`, enter your bot token which can be found at [Discord Developers Page](https://discordapp.com/developers/applications/me). *See  GIF below.*

> `bot_id`, enter your bot ID. *See how to get IDs in the GIF below.*

> `default_prefix`, the default prefix of your Quote bot. You can change it to whatever you like.

> `owner_ids`, these are the IDs of users who can use the owner only commands, including yourself. *See how to get IDs in the GIF below.*

> `botlog_webhook_url`, this is the URL of the webhook in a bot log channel. The webhook will announce when a guild is added/removed. *See how to get Webook URL in the GIF below*

> `anti_bot_farm`, this is where you modify options of the Quote's auto leave from bot farming servers. To enable it, replace `false` with `true`. Under `leave_guild_if`, you'll see 2 different types of numbers. `min_member_count` is the count of how many members there are in a server. `min_bot_rate` is the rate in percentage.
If a server has less than `x` (default `20`) members and if the bots make up to `x` (default `70.0`) percent of the server population, the bot will leave automatically.

> Getting Token

![](http://i.imgur.com/jaxgi2P.gif)

> Getting Owner ID

![](http://i.imgur.com/UQxBZfJ.gif)

> Getting Webook URL

![](https://i.imgur.com/OakxxaJ.gif)

---

# Windows

> Head to the configs folder.

> Right click on `config.json` and click on **Open With Notepad++**.

> Fill out the fields, refer to [explanation of features](#explanation-of-features).

> Once you're done, save by pressing `CTRL + S`.

> You can now launch the bot from the Windows installer. Enjoy.

---

# Linux

## Via Nano

> Head to the configs folder by typing `cd Quote/configs`

> To edit `config.json`, type `nano config.json`

> Fill out the fields, refer to [explanation of features](#explanation-of-features).

> Once you're done, save by pressing `CTRL + X`.

> It will prompt you whether you want to save. Press `Y` to accept.

> You can now launch the bot from the `launcher_linux.sh`. Enjoy.

## Via FTP

> Head to the configs folder.

> Right click on `config.json` and click on **Open With Notepad++**.

> Fill out the fields, refer to [explanation of features](#explanation-of-features).

> Once you're done, save by pressing `CTRL + S`.

> You can now launch the bot from the Windows installer. Enjoy.

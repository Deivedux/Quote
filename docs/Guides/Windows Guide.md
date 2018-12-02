# Requirements

**[Git for Windows](https://git-scm.com/download/win)**

**[Python 3.5+](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)**

**[Notepad++](https://notepad-plus-plus.org/repository/7.x/7.6/npp.7.6.Installer.exe)** - Or any decent text editor.



# Installing Requirements

## Git

**Important: Install Git in `C:/Program Files/`! Refer to GIF below!**

To install Git, click [here](https://github.com/git-for-windows/git/releases/download/v2.19.1.windows.1/Git-2.19.1-64-bit.exe).

![](https://i.imgur.com/ggRHDrz.gif)

## Python 

**Important: Install Python in `C:/Program Files (x86)/`! Refer to GIF below!**

Make a new folder in `C:/Program Files (x86)/` and call it `Python36`.

To install Python 3.5+, click [here](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe).

**Launch the setup with Administrator permission!**

![](https://i.imgur.com/l5YzGWO.gif)

### Checking PIP version.

Open `Command Prompt` by either pressing `Windows Key + R` and `cmd` or opening start menu and typing `Command Prompt`.

To check the pip version, type `pip -V`.

If your pip version is not 18.1, update the pip by following how-to down below. If your pip version is 18.1, continue following this guide.

### How-To Update PIP

Open start menu and type `Git BASH`. Launch it with Administrative permission (Right Click => `Run As Administrator`).

Once it launches, you're going to type the following in:

```
curl -L https://raw.githubusercontent.com/aki-jp/QuoteRequirements/master/reqs.bat
```



# Installing Quote

Once you've installed the requirements, head over [here](https://aki-toga.tk/quote) to download the Windows installer.

After the installer installs, press `Check For Git` and then `Download`. Choose a folder where you want to install Quote and then click Continue. **Note: It is not advised to press `Cancel`**

You should see a Git terminal pop-up now. After it goes away, Quote will be installed in the folder you specified. Launch it by pressing `Launch` and selecting the folder where you installed Quote. *Refer to GIFs below.*

Downloading:
![](http://i.imgur.com/aZ1GSf5.gif)


Launching:
![](http://i.imgur.com/JjcrSf3.gif)



# Editing Credentials

Head to `configs` folder and right click on `config.json`

Edit it with Notepad++ or any decent text editing software you have. (Visual Studio Code, Atom, etc.)

Under `Token`, insert your bot's token which can be found on the [Discord developers page](https://discordapp.com/developers/applications/me). *Refer to GIF below.*

Once you've filled out the token, now it's time to edit the `owner_ids`. *Refer to GIF below.*

Token:

![](http://i.imgur.com/jaxgi2P.gif)


Owner IDs:

![](http://i.imgur.com/UQxBZfJ.gif)


After you found out your owner ID and copied it, your `config.json` should look something like this.

![](https://i.imgur.com/MHjaCqh.png)


# Inviting Your Bot

Last but not least, inviting your bot.

Replace `<bot_id>` with your bot's ID in this link: `https://discordapp.com/oauth2/authorize?client_id=<bot id>&permissions=84992&scope=bot`

Once you replaced `<bot_id>` with your bot's ID, copy the link in a new tab (the current tab also works) and select your server.

After that, you're all set. If you have any questions, ask in the [Official Support Server](https://discord.gg/sbySHxA).

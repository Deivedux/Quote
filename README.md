[![Support Server](https://discordapp.com/api/guilds/418455732741079040/widget.png?style=shield)](https://discord.gg/sbySHxA)
[![Quote Bot](https://discordbots.org/api/widget/upvotes/447176783704489985.svg)](https://discordbots.org/bot/447176783704489985/vote)
[![Code Quality](https://api.codacy.com/project/badge/Grade/81a0a0e33ddd4a32882fe57ebb5d60a1)](https://app.codacy.com/app/aki-jp/Quote?utm_source=github.com&utm_medium=referral&utm_content=Deivedux/Quote&utm_campaign=Badge_Grade_Dashboard)

# Quote and reply to messages on Discord!
Quote is a Discord bot that allows users to easily quote messages, a feature that any serious messaging platform should have but is missing from Discord.

![Here is how it looks](https://cdn.discordapp.com/attachments/154295458531901441/526119544947736595/unknown.png)

# Features

## Quoting 

* You can quote messages by reacting with 💬 (`:speech_balloon:`) to them (this feature needs to be enabled first by using the `>reactions` command).


* You can quote messages from any channel by using the `>quote` command, like this: `>quote 507103646995972096 My Optional Reply`, where the number is the ID of the message you want to quote.


  * ![Copy Link](https://cdn.discordapp.com/attachments/347329036084707330/528281615911223296/unknown.png)
  

  * To get message IDs you need to enable Developer Mode in Discord >settings >Appearance >Developer Mode, and right click on a message >Copy ID.
  
  * ![Developer Mode](https://cdn.discordapp.com/attachments/154295458531901441/526118407071072281/unknown.png)

  * ![Copy ID](https://cdn.discordapp.com/attachments/154295458531901441/526118743550722049/unknown.png)
  

* **You can now quote by directly sending a link to a message**, Quote will automatically embed the linked message.

  * ![Copy Link](https://cdn.discordapp.com/attachments/347329036084707330/528282464142229504/unknown.png)

  * To obtain the link to a message enable Developer Mode as described above and click on the three dots to the right of a message, there will be a Copy Link option.

  * ![Copy Link](https://cdn.discordapp.com/attachments/154295458531901441/526117532248047626/unknown.png)
  
  
* The footer contains useful information on the requester, channel of the original message and timestamp of the original message.


* The Original Poster name in the quote is actually a clickable link to the original message.


* The bot supports quoting of regular messages sent either by users or other bots, but also supports quoting messages containing single or multiple files attachments.

  * If the original message has a single image as an attachment Quote will automatically embed it.


## Delete Commands
* You can set the bot to automatically delete the commands used to quote messages. Type `>delcommands` to activate the option server wide.


## Random Quotes
* Get a random quote from a random (or specified) category. You can also submit your own quotes for someone else to randomize in the future.


## Pinning
* You can define a pin channel by running the command `>pinchannel #myChannel`, and have the bot embed there any message to which you add a 📌 (`:pushpin:`) reaction to. (Only users with Manage Messages permission can use this to avoid spam.)


## Snipe
* Never seen an unread message notification in a channel to then find nothing there? Quote will allow users with Manage Messages permission to check the last deleted message in a channel.
  * Use the command `>snipe` to show last deleted message in the current channel.
  * Add a channel identifier `>snipe #myChannel` to see last deleted message in #myChannel.


## Custom Prefix
* Don't like `>` as your server's prefix? You can change it by using `>prefix <your custom prefix>` eg: `>prefix !`.


## Help
* The bot comes with a `>help` function that shows the list of all available commands. 
* You can type `>help <exampleCommand>` to see more information about each command. 


## Anti-Bot Farm
* Quote will leave any server with more than 20 members that has more than 70% of the population composed of Bots.


## Other
* All of ther useful features that you'll love. We're still improving, so give us a chance.


# Self-Host
* If you'd like to selfhost Quote, you are more than welcome to by following one of the guides found on our [**Documentation Page**](https://quote.readthedocs.io/en/latest/).


# Suggestions
* Have a suggestion? Join our [**Support Server**](https://discord.gg/sbySHxA) and head over to #suggestions. Follow the template to submit your own suggestion.

# Commands list
*Some commands may require special server permissions to execute.*


## Quoting

|Command|`>quote` / `>q`|
|---|---|
|Description|Quote a message using a message ID, and optionally leave your own reply to a quoted message.|
|Example|`>quote 426100904874213387` or `>q 426100904874213387 This is my reply`|

|Command|`>quotechannel` / `>quotechan` / `>qchan` / `>qc`|
|---|---|
|Description|Quote a message using a message ID from a specific channel.|
|Example|`>qc #channel 492444904681897986 My reply!`|

|Command|`>snipe`|
|---|---|
|Description|Snipe the last deleted message from the specified channel. Defaults to current channel.|
|Example|`>snipe` or `>snipe #general`|


## Server

|Command|`>prefix`|
|---|---|
|Description|See the current prefix, or change prefix for this server.|
|Example|`>prefix` or `>prefix !`|

|Command|`>delcommands` / `>delcmds`|
|---|---|
|Description|Toggle whether to automatically command messages.|
|Example|`>delcommands`|

|Command|`>reactions`|
|---|---|
|Description|Toggle whether to let users quote messages by adding 💬 reaction to them.|
|Example|`>reactions`|

|Command|`>pinchannel` / `>pinc`|
|---|---|
|Description|Set a channel that will be used for pinning messages. Members with `Manage Messages` permission can react with 📌 to pin a message.|
|Permission|Manage Messages|
|Example|`>pinchannel #channel` or `>pinchannel`|


## Personal Quoting

|Command|`>personaladd` / `>padd`|
|---|---|
|Description|Add your personal quote, with a trigger and a response, which only you can trigger in any server. A maximum of 10 personal quotes are allowed.|
|Example|`>padd trigger response` or `>padd "my trigger" my response`|

|Command|`>personalremove` / `>premove` / `>prem`|
|---|---|
|Description|Remove your personal quote with a specified trigger.|
|Example|`>premove my trigger`|

|Command|`>personal` / `>p`|
|---|---|
|Description|Execute your personal quote with a chosen trigger.|
|Example|`>p my trigger`|

|Command|`>personallist` / `>plist`|
|---|---|
|Description|List your personal quotes.|
|Example|`>plist`|


## Owner

|Command|`>blacklistadd`|
|---|---|
|Description|Blacklist a user/server with the specified ID with an optional reason.|
|Example|`>blacklistadd 447176783704489985 Abusing bot`|

|Command|`>blacklistremove`|
|---|---|
|Description|Remove a specified user/server with the specified ID from the blacklist|
|Example|`>blacklistcheck 447176783704489985`|

|Command|`>blacklistcheck`|
|---|---|
|Description|Check if the specified ID is blacklisted.|
|Example|`>blacklistcheck 447176783704489985`|

|Command|`>donator`|
|---|---|
|Description|Add/remove a user from `>donators` using their user ID.|
|Example|`>donator 415570038175825930`|

|Command|`>leave`|
|---|---|
|Description|Leaves the server with specified ID.|
|Example|`>leave 419984865262305291`|

|Command|`>shutdown`|
|---|---|
|Description|Shuts down the bot.|
|Example|`>shutdown`|

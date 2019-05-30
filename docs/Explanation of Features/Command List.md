# Commands list
*Some commands may require special server permissions to execute.*

---

## Help

|Command|`>help`|
|---|---|
|Description|Show this message, or more details on a specific command.|
|Example|`>help`|

|Command|`>donators`|
|---|---|
|Description|List users that support Quote on Patreon.|
|Example|`>donators`|

---

## Quoting

|Command|`>quote` / `>q`|
|---|---|
|Description|Quote a message using a message ID or by saying a part of the message (case-insensitive), and optionally leave your own reply to a quoted message. Limited to 2 uses per 5 second time frame per channel.|
|Example|`>quote 426100904874213387` or `>q 426100904874213387 This is my reply` or `>quote message this is my reply` or `>quote "this message" my reply`|

|Command|`>snipe`|
|---|---|
|Description|Snipe the last deleted message from the specified channel. Defaults to current channel.|
|Example|`>snipe` or `>snipe #general`|

|Command|`>duplicate` / `>dupe`|
|---|---|
|Description|Duplicate messages from one channel to the other with a help of a webhook. First argument is the number of messages to duplicate (max 100), second argument is the channel to duplicate messages from, third argument is the target channels to duplicate messages to (defaults to current). User requires `Manage Server` permission to execute. Limited to 2 uses per 30 second time frame per server.|
|Example|`dupe 20 #from #to` or `>dupe 20 #chat`|

---

## Server

|Command|`>prefix`|
|---|---|
|Description|See currently set prefix, or change to a different prefix for this server.|
|Example|`>prefix` or `>prefix !`|

|Command|`>delcommands` / `>delcmds`|
|---|---|
|Description|Toggle whether to automatically delete the quote command message before quoting.|
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

---

## Personal Quoting

|Command|`>personaladd` / `>padd`|
|---|---|
|Description|Add your personal quote, with a trigger and a response, which only you can trigger in any server. A response can be any number of attachments and/or a follow-up message after the trigger.|
|Example|`>padd trigger response` or `>padd "my trigger" my response`|

|Command|`>qradd` / `>qr`|
|---|---|
|Description|Same as `>personaladd`, but instead creates a QR code based on the response of your trigger. Lesser characters - better performance; it is highly recommended to use a link shortener in your response, especially if it's a long link.|
|Example|`>qradd trigger response`|

|Command|`>personalremove` / `>premove` / `>prem`|
|---|---|
|Description|Remove your personal quote with a specified trigger.|
|Example|`>premove my trigger`|

|Command|`>personal` / `>p`|
|---|---|
|Description|Execute your personal quote with a chosen trigger.|
|Example|`>p trigger`|

|Command|`>personallist` / `>plist`|
|---|---|
|Description|List your personal quotes. 10 quotes per page.|
|Example|`>plist`|

|Commands|`>personalclear` / `>pclear`|
|---|---|
|Description|Deletes all your personal quotes.|
|Example|`>pclear`|

---

## Random Quotes

|Command|`>randquote`|
|---|---|
|Description|Shows a random quote from a random (or specified) category. Type `{0}randcategories` for a list of categories.|
|Example|`>randquote` or `>randquote Funny`|

|Command|`>randcategories`|
|---|---|
|Description|Shows a list of available quote categories.|
|Example|`>randcategories`|

|Command|`>randsubmit`|
|---|---|
|Description|Submit your own quote for a specified category. First argument is a category name, everything after it is a quote. Only works in DM channels. To prevent unwanted spam, command is limited to 5 uses within an hour per user, regardless of it's success. Limited to 5 uses per 60 minute time frame per user.|
|Example|`>randsubmit Meme This is a meme quote.`|

---

## Other

|Command|`>lookup`|
|---|---|
|Description|Look up general information about a Discord invite URL/code.|
|Example|`>lookup sbySHxA`|

|Command|`>snowflake`|
|---|---|
|Description|Gets the creation date and time of the specified Discord snowflake (ID).|
|Example|`>snowflake 418455732741079040`|

---

## Owner

|Command|`>randqueue`|
|---|---|
|Description|Show the next unapproved random quote from the queue.|
|Example|`>randqueue`|

|Command|`>randapprove`|
|---|---|
|Description|Approve a random quote by it's ID.|
|Example|`>randapprove 225`|

|Command|`>randdecline`|
|---|---|
|Description|Decline a random quote by it's ID with an optional reason.|
|Example|`>randdecline 225 bad quote`|

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

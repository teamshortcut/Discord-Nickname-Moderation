# Discord Nickname Moderation
A Discord bot to allow for nickname filtering, and to lock users' nicknames with a role.

# Setup
To use the bot, create a Discord role for the bot that has the necessary permissions; namely, `View Audit Log` and `Manage Nicknames`.

Replace the constants at the top of the program with the relevant IDs; these can be obtained by turning on Developer Mode. https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-

The bot will filter nicknames/usernames based on regex patterns; some starter patterns have been included, but these can be edited as required.

# Features
This bot can:

* Filter nickname changes! This allows you to prevent users circumventing a banned word filter in their nicknames.
* Lock users' nicknames! If a user is circumventing filters, you can create a `Static Nickname` role (or otherwise named) that will revert any changes to their nickname they make, while ignoring changes made by admins.
* Filter usernames! If a new member joins and their username matches the banned filters, an existing member changes their username, or if the bot would reset a nickname but the username also matches the filters, the bot will simply give them a placeholder nickname.

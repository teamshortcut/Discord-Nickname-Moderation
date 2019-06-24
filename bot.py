# Import libraries
import discord
import re

TOKEN = "XXXX"
ADMIN_ROLES = [00000000000000000, 00000000000000000] # insert numerical IDs of admin roles here - bot will ignore changes made by these users
BOT_ROLE_ID = 00000000000000000 # numerical ID of the role given to this bot - changes made by this role will be ignored
STATIC_NICKNAME_ROLE_ID = 00000000000000000 # numerical ID - bot will revert changes made by these users
PLACEHOLDER_NICKNAME = "Valued server member"
NICKNAME_PATTERNS = [
    r'(discord\.gg/)',  # invite links
    r'(nigg|fag|\bnazi\b)',  # banned words - \bword\b is exact match only
    r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'  # hyperlinks
]

client = discord.Client()

# Checks if a nickname matches any of the banned patterns
def checkName(nick):
    result = False
    for i in NICKNAME_PATTERNS:
        if re.match(i, nick, re.IGNORECASE):
            result = True
            break

    return result


# triggered on new/removed nickname
@client.event
async def on_member_update(memberBefore, memberAfter):
    # get corresponding audit log entry to find who initiated member change
    corresponding_audit_entry = None
    # get all audit log entries for Member Updated
    async for entry in client.guilds[0].audit_logs(action=discord.AuditLogAction.member_update):
        # if this entry was to the user in question, and was this specific nickname change
        if (entry.target == memberBefore and entry.after.nick == memberAfter.nick):
            corresponding_audit_entry = entry
            print(entry.user)
            print(entry.user.roles)
            break

    if corresponding_audit_entry is not None:  # successfully found audit log entry before
        # user changed their own nickname; ignore if admin/bot changed it
        admin_role_check = (corresponding_audit_entry.user.top_role.id in ADMIN_ROLES)
        bot_role_check = (corresponding_audit_entry.user.top_role.id == BOT_ROLE_ID)
        if not(admin_role_check or bot_role_check):
            for i in memberAfter.roles:
                print(i.id)
                if i.id == STATIC_NICKNAME_ROLE_ID:  # user has Static Name role
                    await memberAfter.edit(nick=memberBefore.display_name)  # revert nickname
                    return
                else:  # check for bad words
                    new_nickname = memberAfter.display_name
                    if checkName(new_nickname):  # bad display name
                        if not checkName(memberAfter.name):  # username is okay
                            await memberAfter.edit(nick=None)  # reset nickname
                        else:
                            # assign placeholder nickname
                            await memberAfter.edit(nick=PLACEHOLDER_NICKNAME)


# triggered on username change
@client.event
async def on_user_update(memberBefore, memberAfter):
    newUsername = memberAfter.name
    if checkName(newUsername):  # bad username
        # assign placeholder nickname
        await memberAfter.edit(nick=PLACEHOLDER_NICKNAME)


# check if new members' usernames need filtering
@client.event
async def on_member_join(member):
    username = member.name
    if checkName(username):  # bad username
        # assign placeholder nickname
        await member.edit(nick=PLACEHOLDER_NICKNAME)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)

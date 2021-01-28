from disc_api import Discord
from pathlib import Path
from time import sleep
import json

r = Discord();
config = Path("config.json")
if not config.is_file():
    print("config.json with username and password required")
    exit()
f = open("config.json", "r+")
info = json.load(f)
email = info.get("email")
password = info.get("password")
if "token" not in info.keys():
    print("logging in...")
    success = r.login(email, password)
    if not success:
        print("Failed to log in")
        exit()
    info["token"] = r.s.headers["Authorization"]
    f.seek(0)
    f.write(json.dumps(info, indent=4, sort_keys=True))
else:
    print("already logged in")
    r.s.headers["Authorization"] = info["token"]

for guild in r.list_guilds():
    if guild["name"] == "DynoServer" and guild["owner"] == True:
        print("found DynoServer!")
        guild_id = guild["id"]
        break
else:
    print("Found no DynoServer! Please create a server named DynoServer and add Dyno to it (you must own the server too)")
    exit()
for channel in r.list_channels(guild_id):
    if channel["name"] == "general":
        print("found general!")
        channel_id = channel["id"]
        break
else:
    print("Found no #general in the DynoServer!")
    exit()
def get_matches():
    r.send_message(channel_id, "?discrim")
    while True:
        msg = r.get_messages(channel_id)[0]
        if msg.get("author").get("id") == "155149108183695360":
            break;
        sleep(0.5)
    users = msg.get("embeds")[0].get("description")
    return users.split("\n")
ogname = r.get_info()['username'];
cool = [6969, 1337]
while True:
    currinfo = r.get_info();
    curr_discrim = int(currinfo['discriminator'])
    if curr_discrim % 1111 == 0 or str(curr_discrim) in '123456789' or curr_discrim in cool:
        print(f"Got you {currinfo['username']}#{currinfo['discriminator']}. Bye!")
        exit()
    for match in get_matches():
        uname = match.rsplit("#", 1)[0]
        if r.change_username(uname, info.get("password")):
            r.change_username(ogname, info.get("password"))
    print(f"Current place: {currinfo['username']}#{currinfo['discriminator']}")
    sleep(60*60)
URL = "https://discord.com/api/v8"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
import requests, json, random
class Discord:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT
        }
    def login(self, email: str, password: str) -> bool:
        data = json.dumps({
            'email': email,
            'password': password
        }).encode('utf-8')
        res = self.s.post(URL+"/auth/login", data=data)
        if res.status_code != 200:
            return False
        else:
            self.s.headers["Authorization"] = res.json().get("token")
            return True
    def list_guilds(self):
        res = self.s.get(URL+"/users/@me/guilds")
        if res.status_code == 200:
            return res.json()
        else:
            return None
    def list_channels(self, guild: str):
        res = self.s.get(URL+f"/guilds/{guild}/channels")
        if res.status_code == 200:
            return res.json()
        else:
            return None
    def send_message(self, channel: str, message: str, tts=False):
        data = json.dumps({
            "content": message,
            "tts": tts,
            "nonce": str(random.randint(0, 1 << 32))
        })
        res = self.s.post(URL+f"/channels/{channel}/messages", data=data)
        if res.status_code == 200:
            return res.json()
        else:
            return False
    def get_info(self):
        res = self.s.get(URL+"/users/@me")
        if res.status_code == 200:
            return res.json()
        else:
            return False
    def change_username(self, username: str, password: str) -> bool:
        info = self.get_info()
        if not info:
            return False
        data = json.dumps({
            "username": username,
            "password": password,
            "avatar": info.get("avatar")
        })
        res = self.s.patch(URL+"/users/@me", data=data)
        if res.status_code == 200:
            return True
        else:
            return False
    def get_messages(self, channel: str, limit=1):
        res = self.s.get(URL+f"/channels/{channel}/messages?limit={limit}")
        if res.status_code == 200:
            return res.json()
        else:
            return False
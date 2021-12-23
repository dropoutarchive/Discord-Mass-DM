# don't forget to leave a star <3 https://github.com/hoemotion/Disocrd-Mass-Dm
import os, sys, time, random, asyncio, json, logging; from datetime import datetime; from lib.scraper import Scraper
try:
    import psutil; from aiohttp import ClientSession; from tasksio import TaskPool
except ImportError:
    os.system("pip install aiohttp")
    os.system("pip install tasksio")
    os.system("pip install psutil")
    import psutil; from tasksio import TaskPool; from aiohttp import ClientSession

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)


class Discord(object):

    def __init__(self):
        if os.name == 'nt':
            self.clear = lambda: os.system("cls")
        else:
            self.clear = lambda: os.system("clear")

        self.clear()
        self.tokens = []
        self.blacklisted_users = []

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None
        self.g = "\033[92m"
        self.red = "\x1b[38;5;9m"
        self.rst = "\x1b[0m"
        self.success = f"{self.g}[+]{self.rst} "
        self.err = f"{self.red}[{self.rst}!{self.red}]{self.rst} "
        self.opbracket = f"{self.red}({self.rst}"
        self.closebrckt = f"{self.red}){self.rst}"
        self.question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
        self.arrow = " \x1b[38;5;9m->\x1b[0m "

        try:
            with open("data/tokens.json", "r") as file:
                tkns = json.load(file)
                if len(tkns) == 0:
                    logging.info(f"{self.err} Please insert your tokens {self.opbracket}tokens.json{self.closebrckt}")
                    sys.exit()
                for tkn in tkns:
                    self.tokens.append(tkn)
        except Exception:
            logging.info(f"{self.err} Please insert your tokens correctly in {self.opbracket}tokens.json{self.closebrckt}")
            sys.exit()
        try:
            with open("data/blacklisted_user_ids.json", "r") as file:
                blacklisted_ids = json.load(file)
                for user_id in blacklisted_ids:
                    self.blacklisted_users.append(str(user_id))
        except Exception:
            logging.info(
                f"{self.err} Please insert the blacklisted User IDs correctly {self.opbracket}blacklisted_user_ids.json{self.closebrckt}")
            sys.exit()
        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

        logging.info(
            f"{self.g}[+]{self.rst} Successfully loaded {self.red}%s{self.rst} token(s)\n" % (len(self.tokens)))
        with open("data/message.json", "r") as file:
            data = json.load(file)
        msg = data['content']
        embds = data['embeds']
        self.invite = input(f"{self.question}Invite{self.arrow}discord.gg/")
        self.leaving = input(f"{self.question}Leave Server after Mass DM? {self.opbracket}y/n{self.closebrckt}{self.arrow}")
        self.mode = input(f"{self.question}Use Proxies? {self.opbracket}y/n{self.closebrckt}{self.arrow}")
        if self.mode.lower() == "y":
            self.use_proxies = True
            self.proxy_type = input(f"{self.question}Proxy type {self.opbracket}http/https/socks4{self.closebrckt}{self.arrow}")
        else:
            self.use_proxies = False

        self.message = msg
        self.embed = embds
        try:
            self.delay = float(input(f"{self.question}Delay{self.arrow}"))
        except Exception:
            self.delay = 0
        try:
            self.ratelimit_delay = float(input(f"{self.question}Rate limit Delay{self.arrow}"))
        except Exception:
            self.ratelimit_delay = 300

        print()

    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts) * 1000 - 1420070400000) * 4194304)

    async def headers(self, token):
        async with ClientSession() as client:
            async with client.get("https://discord.com/app") as response:
                cookies = str(response.cookies)
                dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]
            async with client.get("https://discordapp.com/api/v9/experiments") as finger:
                json = await finger.json()
                fingerprint = json["fingerprint"]
            #logging.info(f"{self.success}Obtained dcfduid cookie: {dcfduid}")
            #logging.info(f"{self.success}Obtained sdcfduid cookie: {sdcfduid}")
            #logging.info(f"{self.success}Obtained fingerprint: {fingerprint}")

        return {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__dcfduid=%s; __sdcfduid=%s; locale=en-US" % (dcfduid, sdcfduid),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": fingerprint,
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }

    async def login(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as mass_dm_brrr:
                async with mass_dm_brrr.get("https://discord.com/api/v9/users/@me/library", proxy=proxy) as response:
                    try:
                        json = await response.json()
                        jsoncode = json["code"]
                        code = f"{self.opbracket}{jsoncode}{self.closebrckt} | "
                    except:
                        code = ""
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully logged in {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    if response.status == 401:
                        logging.info(f"{self.err}Invalid account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    if response.status == 403:
                        logging.info(f"{self.err}Locked account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    if response.status == 429:
                        logging.info(f"{self.err}Rate limited {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        await self.login(token, proxy)
        except Exception:
            await self.login(token, proxy)

    async def join(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as hoemotion:
                async with hoemotion.post("https://discord.com/api/v9/invites/%s" % (self.invite), json={}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        self.guild_name = json["guild"]["name"]
                        self.guild_id = json["guild"]["id"]
                        self.channel_id = json["channel"]["id"]
                        logging.info(f"{self.success}Successfully joined %s {self.opbracket}%s{self.closebrckt}" % (
                        self.guild_name[:20], token[:59]))
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 403:
                        logging.info(f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        await self.join(token, proxy)
                    elif response.status == 404:
                        logging.info(f"{self.err}Server-Invite is invalid or has expired :/")
                        self.stop()
                    else:
                        self.tokens.remove(token)
        except Exception:
            await self.join(token, proxy)

    async def create_dm(self, token: str, user: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as chupapi_munanyo:
                async with chupapi_munanyo.post("https://discord.com/api/v9/users/@me/channels",
                                                json={"recipients": [user]}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully created direct message with %s {self.opbracket}%s{self.closebrckt}" % (
                            json["recipients"][0]["username"], token[:59]))
                        return json["id"]
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403:
                        logging.info(
                            f"{self.err}Can\'t message user {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        return await self.create_dm(token, user, proxy)
                    elif response.status == 400:
                        logging.info(
                            f"{self.err}Can\'t create DM with yourself! {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 404:
                        logging.info(
                            f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    else:
                        return False
        except Exception:
            return await self.create_dm(token, user, proxy)

    async def direct_message(self, token: str, channel: str, user, proxy: str):
        embed = self.get_user_in_embed(user)
        message = self.get_user_in_message(user)
        headers = await self.headers(token)
        async with ClientSession(headers=headers) as virgin:
            async with virgin.post("https://discord.com/api/v9/channels/%s/messages" % (channel),
                                   json={"content": message, "embeds": embed, "nonce": self.nonce(),
                                         "tts": False}, proxy=proxy) as response:
                json = await response.json()
                if response.status == 200:
                    logging.info(f"{self.success}Successfully sent message {self.opbracket}%s{self.red}){self.rst}" % (
                    token[:59]))
                elif response.status == 401:
                    logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.tokens.remove(token)
                    return False
                elif response.status == 403 and json["code"] == 40003:
                    logging.info(f"{self.err}Ratelimited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 403 and json["code"] == 50007:
                    logging.info(f"{self.err}User has direct messages disabled {self.opbracket}%s{self.closebrckt}" % (
                    token[:59]))
                elif response.status == 403 and json["code"] == 40002:
                    logging.info(f"{self.err}Locked {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.tokens.remove(token)
                    return False
                elif response.status == 429:
                    logging.info(f"{self.err}Ratelimited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 400:
                    code = json["code"]
                    logging.info(f"{self.err}Can\'t DM this User! {self.opbracket}{code}{self.closebrckt} | {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                elif response.status == 404:
                    logging.info(f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                else:
                    return False

    def get_user_in_message(self, user: str = None):
        mssage = self.message
        message = mssage.replace("<user>", f"<@{user}>")
        return message

    def get_user_in_embed(self, user: str = None):
        embd = json.dumps(self.embed)
        embedd = embd.replace("<user>", f"<@{user}>")
        embed = json.loads(embedd)
        return embed

    async def send(self, token: str, user: str, proxy: str):
        channel = await self.create_dm(token, user, proxy)
        if channel == False:
            return await self.send(random.choice(self.tokens), user, proxy)
        response = await self.direct_message(token, channel, user, proxy)
        if response == False:
            return await self.send(random.choice(self.tokens), user, proxy)

    async def leave(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.delete(f"https://discord.com/api/v9/users/@me/guilds/{self.guild_id}",
                                         json={"lurking": False}, proxy=proxy) as response:
                    json = await response.json()
                    message = json["message"]
                    code = json["code"]
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 204:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 404:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 403:
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 401:
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 429:
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        await self.leave(token, proxy)
                    else:
                        logging.info(
                            f"{self.err}{response.status} | {message} | {code} | {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))


        except Exception:
            await self.leave(token, proxy)

    async def start(self):
        if len(self.tokens) == 0:
            logging.info("No tokens loaded.")
            sys.exit()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    if self.use_proxies:
                        proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                    else:
                        proxy = None
                    await pool.put(self.login(token, proxy))
                else:
                    self.stop()

        if len(self.tokens) == 0: self.stop()

        print()
        logging.info("Joining server.")
        print()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    if self.use_proxies:
                        proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                    else:
                        proxy = None
                    await pool.put(self.join(token, proxy))
                    if self.delay != 0: await asyncio.sleep(self.delay)
                else:
                    self.stop()

        if len(self.tokens) == 0: self.stop()

        scraper = Scraper(
            token=self.tokens[0],
            guild_id=self.guild_id,
            channel_id=self.channel_id
        )
        self.users = scraper.fetch()

        print()
        logging.info(f"Successfully scraped {self.red}%s{self.rst} members" % (len(self.users)))
        logging.info("Sending messages.")
        print()

        if len(self.tokens) == 0: self.stop()

        async with TaskPool(1_000) as pool:
            for user in self.users:
                if len(self.tokens) != 0:
                    if str(user) not in self.blacklisted_users:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.send(random.choice(self.tokens), user, proxy))
                        if self.delay != 0: await asyncio.sleep(self.delay)
                    else:
                        logging.info(f"{self.err}Blacklisted User: {self.red}%s{self.rst}" % (user))
                else:
                    self.stop()

        if self.leaving == "y":
            print()
            logging.info("Leaving %s" % self.guild_name)
            print()
            async with TaskPool(1_000) as pool:
                if len(self.tokens) != 0:
                    for token in self.tokens:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.leave(token, proxy))
                        if self.delay != 0:
                            await asyncio.sleep(self.delay)
                    logging.info("All Tasks are done")
                    self.stop()
                else:
                    self.stop()
        else:
            logging.info("All Tasks are done")
            self.stop()


if __name__ == "__main__":
    client = Discord()
    asyncio.get_event_loop().run_until_complete(client.start())

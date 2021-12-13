#this script will keep all your tokens online using a websocket connection which means that its only an optional feature
#made with <3 by https://github.com/hoemotion
import logging, sys, time, asyncio, threading, os, json; from datetime import datetime
try:
    import websocket
    from tasksio import TaskPool
    from aiohttp import ClientSession
    import psutil
except ImportError:
    os.system("pip install tasksio")
    os.system("pip install aiohttp")
    os.system("pip install psutil")
    os.system("pip install websocket-client")
    import websocket, psutil; from tasksio import TaskPool; from aiohttp import ClientSession

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)


class WebSocket(object):

    def __init__(self):
        if os.name == 'nt':
            self.clear = lambda: os.system("cls")
        else:
            self.clear = lambda: os.system("clear")

        self.clear()
        self.tokens = []

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None
        self.g = "\033[92m"
        self.red = "\x1b[38;5;9m"
        self.rst = "\x1b[0m"
        self.success = f"{self.g}[{self.rst}💖{self.g}]{self.rst} "
        self.err = f"{self.red}[{self.rst}!{self.red}]{self.rst} "
        self.opbracket = f"{self.red}({self.rst}"
        self.closebrckt = f"{self.red}){self.rst}"
        self.question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
        self.arrow = " \x1b[38;5;9m->\x1b[0m "
        self.heartbeat = f"{self.red}<3{self.rst}beat"

        try:
            with open("data/tokens.json", "r") as file:
                tkns = json.load(file)
                if len(tkns) == 0:
                    logging.info(f"{self.err}Please insert your tokens {self.opbracket}tokens.json{self.closebrckt}")
                    sys.exit()
                for tkn in tkns:
                    self.tokens.append(tkn)
        except Exception:
            logging.info(f"{self.err}Please insert your tokens {self.opbracket}tokens.json{self.closebrckt}")
            sys.exit()

        logging.info(
            f"{self.success}Successfully loaded {self.red}%s{self.rst} token(s)\n" % (len(self.tokens)))
    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)

    async def main(self, token):
        def send_json_requests(ws, request):
            ws.send(json.dumps(request))

        def receive_json_response(ws):
            response = ws.recv()
            if response:
                return json.loads(response)

        def heartbeat(heartbeat_interval, ws):
            logging.info(f"Entering {self.heartbeat} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
            while True:
                time.sleep(heartbeat_interval)
                heartbeat_json = {
                    "op": 1,
                    "d": "null"
                }
                send_json_requests(ws, heartbeat_json)
                logging.info(
                    f"{self.success}{self.heartbeat} was sent {self.opbracket}%s{self.closebrckt}" % (token[:59]))

        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg//?v=9&encoding=json")
        event = receive_json_response(ws)

        heartbeat_interval = event["d"]["heartbeat_interval"] / 1000


        threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

        payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "windows",
                    "$browser": "Discord",
                    "$device": "desktop"
                }
            }
        }
        send_json_requests(ws, payload)
        while True:
            event = receive_json_response(ws)
            try:
                op_ = event["op"]
                if op_ == 11:
                    logging.info(
                        f"{self.success}Received {self.heartbeat} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
            except:
                pass

    async def headers(self, token):
        async with ClientSession() as client:
            async with client.get("https://discord.com/app") as response:
                cookies = str(response.cookies)
                dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]
            async with client.get("https://discordapp.com/api/v9/experiments") as finger:
                json = await finger.json()
                fingerprint = json["fingerprint"]
            logging.info(f"{self.success} Obtained dcfduid cookie: {dcfduid}")
            logging.info(f"{self.success} Obtained sdcfduid cookie: {sdcfduid}")
            logging.info(f"{self.success} Obtained fingerprint: {fingerprint}")

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

    async def login(self, token: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as token_check:
                async with token_check.get("https://discord.com/api/v9/users/@me/library") as response:
                    if response.status == 200:
                        logging.info(f"{self.success}Successfully logged in {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    if response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    if response.status == 403:
                        logging.info(f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    if response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
        except Exception:
            await self.login(token)

    async def start(self):
        if len(self.tokens) == 0:
            logging.info("No tokens loaded.")
            sys.exit()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    await pool.put(self.login(token))
                else:
                    self.stop()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    await pool.put(self.main(token))


if __name__ == "__main__":
    client = WebSocket()
    asyncio.get_event_loop().run_until_complete(client.start())
    #asyncio.get_event_loop().run_forever()

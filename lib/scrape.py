# cr: https://github.com/vida1338/MassDN-source/blob/main/scrape.py  thx bro <3
import json, threading, time, logging, os
try: import websocket
except:
    os.system("pip install websocket-client")
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)

class Utils:
    def rangeCorrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    def getRanges(index, multiplier, memberCount):
        initialNum = int(index*multiplier)
        rangesList = [[initialNum, initialNum+99]]
        if memberCount > initialNum+99:
            rangesList.append([initialNum+100, initialNum+199])
        return Utils.rangeCorrector(rangesList)

    def parseGuildMemberListUpdate(response):
        memberdata = {
            "online_count": response["d"]["online_count"],
            "member_count": response["d"]["member_count"],
            "id": response["d"]["id"],
            "guild_id": response["d"]["guild_id"],
            "hoisted_roles": response["d"]["groups"],
            "types": [],
            "locations": [],
            "updates": []
        }

        for chunk in response['d']['ops']:
            memberdata['types'].append(chunk['op'])
            if chunk['op'] in ('SYNC', 'INVALIDATE'):
                memberdata['locations'].append(chunk['range'])
                if chunk['op'] == 'SYNC':
                    memberdata['updates'].append(chunk['items'])
                else:  # invalidate
                    memberdata['updates'].append([])
            elif chunk['op'] in ('INSERT', 'UPDATE', 'DELETE'):
                memberdata['locations'].append(chunk['index'])
                if chunk['op'] == 'DELETE':
                    memberdata['updates'].append([])
                else:
                    memberdata['updates'].append(chunk['item'])

        return memberdata


class DiscordSocket(websocket.WebSocketApp):
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.blacklisted_roles, self.blacklisted_users = [], []
        with open("./data/config.json") as f:
            blacklisted = json.load(f)
        for i in blacklisted["blacklisted_roles"]:
            self.blacklisted_roles.append(str(i))
        for i in blacklisted["blacklisted_users"]:
            self.blacklisted_users.append(str(i))

        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        super().__init__("wss://gateway.discord.gg/?encoding=json&v=9",
                         header=self.socket_headers,
                         on_open=lambda ws: self.sock_open(ws),
                         on_message=lambda ws, msg: self.sock_message(ws, msg),
                         on_close=lambda ws, close_code, close_msg: self.sock_close(
                             ws, close_code, close_msg)
                         )

        self.endScraping = False

        self.guilds = {}
        self.members = {}

        self.ranges = [[0, 0]]
        self.lastRange = 0
        self.packets_recv = 0

    def run(self):
        self.run_forever()
        return self.members

    def scrapeUsers(self):
        if self.endScraping == False:
            self.send('{"op":14,"d":{"guild_id":"' + self.guild_id +
                      '","typing":true,"activities":true,"threads":true,"channels":{"' + self.channel_id + '":' + json.dumps(self.ranges) + '}}}')

    def sock_open(self, ws):
        #print("[Gateway]", "Connected to WebSocket.")
        self.send('{"op":2,"d":{"token":"' + self.token + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}')

    def heartbeatThread(self, interval):
        try:
            while True:
                #print("sending heartbeat")
                self.send('{"op":1,"d":' + str(self.packets_recv) + '}')
                time.sleep(interval)
        except Exception as e:
            pass  # print(e)
            return  # returns when socket is closed

    def sock_message(self, ws, message):
        decoded = json.loads(message)

        if decoded is None:
            return

        if decoded["op"] != 11:
            self.packets_recv += 1

        if decoded["op"] == 10:
            threading.Thread(target=self.heartbeatThread, args=(
                decoded["d"]["heartbeat_interval"] / 1000, ), daemon=True).start()

        if decoded["t"] == "READY":
            for guild in decoded["d"]["guilds"]:
                self.guilds[guild["id"]] = {
                    "member_count": guild["member_count"]}

        if decoded["t"] == "READY_SUPPLEMENTAL":
            self.ranges = Utils.getRanges(
                0, 100, self.guilds[self.guild_id]["member_count"])
            # print(self.ranges)
            self.scrapeUsers()

        elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
            parsed = Utils.parseGuildMemberListUpdate(decoded)

            if parsed['guild_id'] == self.guild_id and ('SYNC' in parsed['types'] or 'UPDATE' in parsed['types']):
                for elem, index in enumerate(parsed["types"]):
                    if index == "SYNC":
                        # and parsed['locations'][elem] in self.ranges[1:]: #checks if theres nothing in the SYNC data
                        if len(parsed['updates'][elem]) == 0:
                            self.endScraping = True
                            break

                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                # print(f"item: {item}")
                                mem = item["member"]
                                # print(f"mem: {mem}")
                                obj = {"tag": mem["user"]["username"] + "#" +
                                              mem["user"]["discriminator"], "id": mem["user"]["id"]}
                                if not set(self.blacklisted_roles).isdisjoint(mem['roles']):
                                    logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} has a blacklisted role")
                                else:
                                    if not mem["user"].get("bot"):
                                        if not mem["user"]["id"] in self.blacklisted_users:
                                            self.members[mem["user"]["id"]] = obj
                                        else:
                                            logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} is a blacklisted user")
                                    else:
                                        logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} is a bot")


                    elif index == "UPDATE":
                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                # print(f"item: {item}")
                                mem = item["member"]
                                # print(f"mem: {mem}")
                                obj = {"tag": mem["user"]["username"] + "#" +
                                              mem["user"]["discriminator"], "id": mem["user"]["id"]}
                                if not set(self.blacklisted_roles).isdisjoint(mem['roles']):
                                    logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} has a blacklisted role")
                                else:
                                    if not mem["user"].get("bot"):
                                        if not mem["user"]["id"] in self.blacklisted_users:
                                            self.members[mem["user"]["id"]] = obj
                                        else:
                                            logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} is a blacklisted user")
                                    else:
                                        logging.info(f"{mem['user']['username'] + '#' + mem['user']['discriminator']} is a bot")


                                # print("<SYNC>", "synced", mem["user"]["id"])
                                # print("<SYNC>", "synced", mem["user"])

                    print(self.endScraping)
                    print(self.ranges)
                    print("parsed", len(self.members))

                    self.lastRange += 1
                    self.ranges = Utils.getRanges(
                        self.lastRange, 100, self.guilds[self.guild_id]["member_count"])
                    time.sleep(0.35)
                    self.scrapeUsers()

            if self.endScraping:
                self.close()

    def sock_close(self, ws, close_code, close_msg):
        pass  # print("closed connection", close_code, close_msg)


def scrape(token, guild_id, channel_id):
    sb = DiscordSocket(token, guild_id, channel_id)
    return sb.run()


if __name__ == '__main__':
    logging.info(
        "Don\'t run this File, the scraper will be automatically used in the main.py file\nClick enter to close this file")
    input()
    import sys

    sys.exit()

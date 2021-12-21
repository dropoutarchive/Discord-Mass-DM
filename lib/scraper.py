import os, logging, json, time
try:
    import discum
except ImportError:
    os.system("pip install discum")
    os.system("python -m pip install --user --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M#egg=discum")
    
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)


class Scraper(object):
    def __init__(self, guild_id, channel_id, token):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.token = token

        self.scraped = []
        self.blacklisted_roles = []
        with open("blacklisted_role_ids.json") as f:
            blacklisted = json.load(f)
        for i in blacklisted:
            self.blacklisted_roles.append(str(i))
        self.g = "\033[92m"
        self.red = "\x1b[38;5;9m"
        self.rst = "\x1b[0m"
        self.success = f"{self.g}[+]{self.rst} "
        self.err = f"{self.red}[{self.rst}!{self.red}]{self.rst} "
        self.opbracket = f"{self.red}({self.rst}"
        self.closebrckt = f"{self.red}){self.rst}"
        self.question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
        self.arrow = " \x1b[38;5;9m->\x1b[0m "

    def scrape(self):
        try:
            client = discum.Client(token=self.token, log=False)

            client.gateway.fetchMembers(self.guild_id, self.channel_id, reset=False, keep="all")

            @client.gateway.command
            def scraper(resp):
                try:
                    if client.gateway.finishedMemberFetching(self.guild_id):
                        client.gateway.removeCommand(scraper)
                        client.gateway.close()
                except Exception:
                    pass

            client.gateway.run()



            for user, info in dict(client.gateway.session.guild(self.guild_id).members).items():
                if not set(self.blacklisted_roles).isdisjoint(info['roles']):
                    username = str(client.gateway.session.guild(self.guild_id).members[user].get('username'))
                    logging.info(f"{self.question}{self.g}{username}{self.rst} has a blacklisted role.")
                    del client.gateway.session.guild(self.guild_id).members[user]
                else:
                    if not client.gateway.session.guild(self.guild_id).members[user].get("bot"):
                        self.scraped.append(str(user))



            client.gateway.close()
        except Exception:
            return
    
    def fetch(self):
        try:
            self.scrape()
            if len(self.scraped) == 0:
                return self.fetch()
            return self.scraped
        except Exception:
            self.scrape()
            if len(self.scraped) == 0:
                return self.fetch()
            return self.scraped

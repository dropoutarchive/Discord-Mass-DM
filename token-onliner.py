# this script will keep all your tokens online using a websocket connection which means that its only an optional feature
# credits: https://github.com/Its-Vichy/discord-status-insult-changer <3
import logging, sys, time, asyncio, threading, os, random, json; from datetime import datetime; from random import randint
try:
    import websocket
except ImportError:
    os.system("pip install websocket-client")
    import websocket
logging.basicConfig(level=logging.INFO, format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m", datefmt="%H:%M:%S")
g = "\033[92m"
red = "\x1b[38;5;9m"
rst = "\x1b[0m"
success = f"{g}[{rst}💖{g}]{rst} "
err = f"{red}[{rst}!{red}]{rst} "
opbracket = f"{red}({rst}"
closebrckt = f"{red}){rst}"
question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
arrow = " \x1b[38;5;9m->\x1b[0m "
heartbeat = f"{red}<3{rst}beat"

def init_websocket(token: str):
    status = ["online", "idle", "dnd"]
    ws = websocket.WebSocket()
    ws.connect(url= 'wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream')
    ws.send(json.dumps({"op" :2 ,"d" :{"token": token ,"capabilities" :125
                                       ,"properties" :{"os" :"Linux" ,"browser" :"Firefox" ,"device" :""
                                                      ,"system_locale" :"fr"
                                                      ,"browser_user_agent" :"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
                                                      ,"browser_version" :"95.0" ,"os_version" :""
                                                      ,"referrer" :"https://discord.com/"
                                                      ,"referring_domain" :"discord.com" ,"referrer_current" :""
                                                      ,"referring_domain_current" :"" ,"release_channel" :"stable"
                                                      ,"client_build_number" :107767 ,"client_event_source" :None}
                                       ,"presence" :{"status" :random.choice(status) ,"since" :0 ,"activities" :[] ,"afk" :False}
                                       ,"compress" :False
                                       ,"client_state" :{"guild_hashes" :{} ,"highest_last_message_id" :"0"
                                                        ,"read_state_version" :0 ,"user_guild_settings_version" :-1
                                                        ,"user_settings_version" :-1}}}))

    logging.info(f'{success}Connected to websocket {red}|{rst} {token}')
    return ws

def status_changer(ws: websocket.WebSocket):
    status = ["online", "idle", "dnd"]
    quotes = ["github.com/hoemotion", "guilded.gg/karma", "discord.com/terms", "<3", "github.com/hoemotion", "guilded.gg/karma", "github.com/hoemotion"]
    while True:

        ws.send(json.dumps({"op" :3 ,"d" :{"status" : random.choice(status) ,"since" :0 ,"activities" :
            [{"name" :"Custom Status" ,"type" :4 ,"state": random.choice(quotes)
             ,"emoji" :{"id" :None ,"name" :"heart" ,"animated" :False}}] ,"afk" :False}}))
        sleep = randint(20000, 35000)
        logging.info(f"{success} {token} is alive!")
        logging.info(f"Sleeping {sleep / 1000} seconds {red}|{rst} {token}")
        time.sleep(sleep / 1000)

tokens_list = []
try:
    with open("data/tokens.json", "r") as file:
        tkns = json.load(file)
        if len(tkns) == 0:
            logging.info(f"{err}Please insert your tokens {opbracket}tokens.json{closebrckt}")
            sys.exit()
        for tkn in tkns:
            tokens_list.append(tkn)
except Exception as e:
        logging.info(f"{err}Please insert your tokens correctly in {opbracket}tokens.json{closebrckt} - {e}")
        sys.exit()

for token in tokens_list:
    try:
        threading.Thread(target=status_changer, args=(init_websocket(token),)).start()
    except:
        pass

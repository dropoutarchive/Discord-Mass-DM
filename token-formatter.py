import json, os; from time import time
try:
 import rich
 from rich.progress_bar import ProgressBar
 from rich.console import Console
 from rich.live import Live
 from rich.align import Align
 from rich.highlighter import ReprHighlighter
 from rich.table import Table
 from typing import Dict, Tuple
except ModuleNotFoundError:
 os.system("pip install rich")
 os.system("pip install typing")
import logging
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)
if os.name == 'nt':
 clear = lambda: os.system("cls")
else:
 clear = lambda: os.system("clear")
def table(elapsed_ms, b, style):
 table = Table(
  title="Analyse",
  caption="github.com/hoemotion",
  caption_justify="right",
  caption_style="bright_yellow"
 )

 table.add_column(
  "Tokens Formatted", header_style="bright_cyan", style="blue", no_wrap=True
 )
 table.add_column("Formatting Style", header_style="bright_magenta", style="magenta", justify="center")
 table.add_column("Time Taken", justify="right", header_style="light_green", style="bright_green")

 table.add_row(
  f"{b} Tokens",
  f"{style}",
  f"{elapsed_ms:.0f}ms",
  style="on black",
  end_section=True,
 )


 def header(text: str) -> None:
  console.print()
  console.rule(highlight(text))
  console.print()

 console = Console()
 highlight = ReprHighlighter()

 table.width = None
 table.expand = False
 table.row_styles = ["dim", "none"]
 table.show_lines = True
 table.leading = 0
 header("Token Formatter")
 console.print(table, justify="center")

def txt_to_json_pw():
 console = Console()
 console.show_cursor(False)
 style = "email:pass:token to token (txt -> json)"
 with open('./data/tokens.json')as f:
  t = json.load(f)
 with open('./data/tokens.txt')as f:
  tkns = [i.strip() for i in f]
 f.close()
 bar = ProgressBar(width=55, total=len(tkns))
 b = 0
 all = 0
 s = time()
 with Live(console=console) as livebar:
  exchange_rate_dict: Dict[Tuple[str, str], float] = {}
  for tkn in tkns:
   all += 1
   tkn = tkn.split(':')
   for i in tkn:
    if len(i) > 50:
     if i not in t and '@' not in i and '!' not in i and '?' not in i:
      b += 1
      t.append(i)
   bar.update(all)
   livebar.update(Align.center(bar))
   console.file.write("\r")
 with open('./data/tokens.json', 'w')as f:
  json.dump(t, f)
 e = time()
 elapsed = e - s
 elapsed_ms = elapsed * 1000
 #logging.info(f'Formatted \033[92m{b}\x1b[0m tokens in {elapsed_ms:.1f}\x1b[0mms')
 table(elapsed_ms, b, style)
def txt_to_json():
 console = Console()
 console.show_cursor(False)
 style = "token to token (txt -> json)"
 with open('./data/tokens.json')as f:
  t = json.load(f)
 with open('./data/tokens.txt')as f:
  tkns = [i.strip() for i in f]
 f.close()
 bar = ProgressBar(width=50, total=len(tkns))
 b = 0
 all = 0
 s = time()
 with Live(console=console) as livebar:
  exchange_rate_dict: Dict[Tuple[str, str], float] = {}
  for tkn in tkns:
   all += 1
   if tkn not in t and len(tkn) != 0:
      b += 1
      t.append(tkn)
   bar.update(all)
   livebar.update(Align.center(bar))
   console.file.write("\r")
 with open('./data/tokens.json', 'w')as f:
  json.dump(t, f)
 e = time()
 elapsed = e - s
 elapsed_ms = elapsed * 1000
 table(elapsed_ms, b, style)
 #logging.info(f'Formatted \033[92m{b}\x1b[0m tokens in {elapsed_ms:.1f}\x1b[0mms')
def txt_to_txt():

 console = Console()
 console.show_cursor(False)
 style = "email:pass:token to token (txt -> txt)"
 with open('./data/tokens.txt')as f:
  tkns = [i.strip() for i in f]
 txtfile = input("What\'s the name of your output file \x1b[38;5;9m(\x1b[0mLeave blank for output.txt\x1b[38;5;9m)\x1b[0m? -> ")
 print()
 if len(txtfile) == 0:
  txtfile = "output.txt"
 e.close()
 out_file = open(txtfile, "a")
 f.close()
 bar = ProgressBar(width=55, total=len(tkns))
 b = 0
 all = 0
 s = time()
 with Live(console=console) as livebar:
  exchange_rate_dict: Dict[Tuple[str, str], float] = {}
  for tkn in tkns:
   all += 1
   tkn = tkn.split(':')
   for i in tkn:
    if len(i) > 50:
     if '@' not in i and '!' not in i and '?' not in i:
      b += 1
      out_file.write(i + "\n")
   bar.update(all)
   livebar.update(Align.center(bar))
   console.file.write("\r")
  out_file.close()
 e = time()
 elapsed = e - s
 elapsed_ms = elapsed * 1000
 #logging.info(f'Formatted \033[92m{b}\x1b[0m tokens in {elapsed_ms:.1f}\x1b[0mms')
 table(elapsed_ms, b, style)
def json_to_txt():

 console = Console()
 console.show_cursor(False)
 style = "email:pass:token to token (json -> txt)"
 with open('./data/tokens.json')as f:
  tkns = json.load(f)
 txtfile = input("What\'s the name of your output file \x1b[38;5;9m(\x1b[0mLeave blank for output.txt\x1b[38;5;9m)\x1b[0m? -> ")
 print()
 if len(txtfile) == 0:
  txtfile = "output.txt"
 out_file = open(txtfile, "a")
 f.close()
 bar = ProgressBar(width=55, total=len(t))
 b = 0
 all = 0
 s = time()
 with Live(console=console) as livebar:
  exchange_rate_dict: Dict[Tuple[str, str], float] = {}
  for tkn in tkns:
  
   all += 1
   if len(tkn) > 50:
     if tkn not in t and '@' not in tkn and '!' not in tkn and '?' not in tkn:
      b += 1
      t.append(tkn)
      out_file.write(tkn + "\n")
   bar.update(all)
   livebar.update(Align.center(bar))
   console.file.write("\r")
  out_file.close()
 e = time()
 elapsed = e - s
 elapsed_ms = elapsed * 1000
 #logging.info(f'Formatted \033[92m{b}\x1b[0m tokens in {elapsed_ms:.1f}\x1b[0mms')
 table(elapsed_ms, b, style)
logging.info("")
choose = input("""\033[92m[\x1b[0m1\033[92m]\x1b[0m token -> token  \x1b[38;5;9m(\x1b[0mtxt -> json\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m2\033[92m]\x1b[0m token -> token  \x1b[38;5;9m(\x1b[0mjson -> txt\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m3\033[92m]\x1b[0m email\x1b[38;5;9m:\x1b[0mpass\x1b[38;5;9m:\x1b[0mtoken -> token (the order of this format doesn\'t matter) \x1b[38;5;9m(\x1b[0mtxt -> json\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m4\033[92m]\x1b[0m email\x1b[38;5;9m:\x1b[0mpass\x1b[38;5;9m:\x1b[0mtoken -> token (the order of this format doesn\'t matter) \x1b[38;5;9m(\x1b[0mtxt -> txt\x1b[38;5;9m)\x1b[0m
>>> """)
if choose == "1":
 txt_to_json()
elif choose == "2":
 json_to_txt()
elif choose == "3":
 txt_to_json_pw()
elif choose == "4":
 txt_to_txt()
while choose != "1" and choose != "2"and choose != "3"and choose != "4":
 clear()
 logging.info("")
 choose = input("""\033[92m[\x1b[0m1\033[92m]\x1b[0m token -> token  \x1b[38;5;9m(\x1b[0mtxt -> json\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m2\033[92m]\x1b[0m token -> token  \x1b[38;5;9m(\x1b[0mjson -> txt\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m3\033[92m]\x1b[0m email\x1b[38;5;9m:\x1b[0mpass\x1b[38;5;9m:\x1b[0mtoken -> token (the order of this format doesn\'t matter) \x1b[38;5;9m(\x1b[0mtxt -> json\x1b[38;5;9m)\x1b[0m
\033[92m[\x1b[0m4\033[92m]\x1b[0m email\x1b[38;5;9m:\x1b[0mpass\x1b[38;5;9m:\x1b[0mtoken -> token (the order of this format doesn\'t matter) \x1b[38;5;9m(\x1b[0mtxt -> txt\x1b[38;5;9m)\x1b[0m
>>> """)
 if choose == "1":
  txt_to_json()
 elif choose == "2":
  json_to_txt()
 elif choose == "3":
  txt_to_json_pw()
 elif choose == "4":
  txt_to_txt()

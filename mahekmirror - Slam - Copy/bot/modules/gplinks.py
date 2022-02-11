from telegram.ext import CommandHandler, run_async
from telegram import Bot, Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.filters import CustomFilters

import requests as rq, multiprocessing, re, json, time
from urllib.parse import quote
from bs4 import BeautifulSoup as bt
import base64

class gp:
      def __init__(self, url):
          self.url = url
          self.apv = ''
          self.h = ''
          self.c = ''
          self.p = ''
          self.ref = ''
          self.r = r'\bhttps?://.*gplink\S+'

      def req(i, h, c, p, bot, update):
          time.sleep(10)
          rpt = rq.post("%s/links/go"%(i.rsplit("/",1)[0]), headers=h, cookies=c, data=p).json()
          msg = f"<b>⫸ Source URL</b> : {i}\n\n<b>⫸ Bypassed URL</b> : {rpt['url']}"
          sendMessage(msg ,bot, update)
          return

      def parse(self, bot, update):
          r = re.findall(self.r,self.url)
          if not r:
             sendMessage(f"⫸ <b>Invalid GPLink</b>", bot, update)
          else:
             ps = []
             for i in r:
              try:

                rh = rq.head(i).headers
                rg = re.findall(r"(?:AppSession|app_visitor|__cf_bm)\S+;",rh['set-cookie'])
                st = " ".join(rg).replace("=",": ",3).replace(";",",")
                rg1 = re.sub(r"([a-zA-Z_0-9.%+/=-]+)",r'"\1"','{%s __viCookieActive: true, __cfduid: dca0c83db7d849cdce8d82d043f5347bd1617421634}'%st)
                jd = json.loads(rg1)
                self.c = jd
                self.apv = jd["AppSession"]
                self.ref = rh["location"]
                self.h = {"app_visitor": self.apv,
                          "user-agent": "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba",
                          "upgrade-insecure-requests": "1",
                          "referer": self.ref}
                rget = rq.get(i, cookies=self.c, headers=self.h).content
                bs4 = bt(rget, 'html.parser', from_encoding="iso-8859-1")
                fin = bs4.find_all('input')
                dic = {}
                for g in fin:
                    dic[g.get('name')] = g.get('value')
                self.p = dic
                self.c = {"AppSession": jd["AppSession"], "csrfToken": dic["_csrfToken"]}
                self.h = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8", "accept": "application/json, text/javascript, */*; q=0.01", "x-requested-with": "XMLHttpRequest"}
                p = multiprocessing.Process(target=gp.req, args=[i, self.h, self.c, self.p, bot, update])
                p.start()
                ps.append(p)
              except Exception as e:
                msg = f"<b>⫸ Source URL</b> : {i}\n\n<b>Error while parsing</b> : {e}"
                sendMessage(msg ,bot, update)
                LOGGER.info("Error Occured : "+str(e))
             for p in ps:
                 p.join()


def gparse(update, context):
    bot = context.bot
    try:
        args = update.message.text.split(" ", maxsplit=1)
        if len(args) > 1:
           link = args[1:]
           url = link
           j = '\n'.join('\n'.join(url).split())
           r = '\n'.join(re.split(r'(?=https:\/\/)', j)[1:])

           r1 = r'http[s]:\/\/drive.hollywoodtelugupedia[a-zA-Z0-9.\/\?\=]+'
           r2 = r'/?id=[A-Za-z0-9]+'
           links = re.findall(r1,str(r))
           if links:
            li = []
            for link in links:
              ext = re.findall(r2,link)
              ext = ''.join(ext)
              li.append(ext)
            li = [i.replace('id=', '') for i in li]
            li = [base64.b64decode(f"{i}==").decode() for i in li]
            gpl = []
            d = 'https://gplinks.co/'
            for i in li:
              t = d+i
              gpl.append(t)
            c = '\n'.join(gpl)
            d = r + '\n' + c
            d = '\n'.join(re.split(r'(?=https:\/\/)', d)[1:])
           else:
            d = r
           p = gp(d).parse(bot, update)
        else:
            sendMessage('⫸ Provide a GPlink with command', bot, update)
    except Exception as e:
        sendMessage(f'⫸ <b>Something went wrong in GPLinks Module, Please check logs</b>', bot, update)
        LOGGER.info("Error Occured : "+str(e))
        return

gp_handler = CommandHandler("gp", gparse, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,run_async=True)
dispatcher.add_handler(gp_handler)
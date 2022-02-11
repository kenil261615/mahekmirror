from telegram.ext import CommandHandler, run_async
from telegram import Bot, Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils import gdriveTools
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
import traceback

import sys, os, requests as rq, re, json as js
from bs4 import BeautifulSoup as bt

class gdtot:
      def __init__(self, url):
          self.url = url
          self.list = gdtot.error(self)
          self.r = ''
          self.c = {"PHPSESSID":"k2acd9b2lgg1qjhnjkjfe4j63o", "crypt":"SG1OMVpzZDl2bzBCZHpNL1dOQ2NRRjR5RE8rVnRPQlhReTJXMVNORXEwST0%3D"}
          self.h = {
                   'upgrade-insecure-requests': '1',
                   'save-data': 'on',
                   'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi 8A Dual) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'sec-fetch-site': 'same-origin',
                   'sec-fetch-mode': 'navigate',
                   'sec-fetch-dest': 'document',
                   'referer': self.r,
                   'prefetchAd_3621940': 'true',
                   'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
                   }

      def error(self):
          print(self.url)
          url = re.findall(r'\bhttps?://.*gdtot\S+', self.url)
          return url

      def check(self):
          if c == '':
             return False
          else:
             j = js.loads(c)['cookie'].replace('=',': ').replace(';',',')
             c = re.sub(r'([a-zA-Z_0-9.%]+)', r'"\1"', "{%s}" %j)
             c = js.loads(c)
             return c

      def parse(self, bot, update):
          if len(self.list) == 0:
             return
          elif self.c == False:
             return
          else:
             for i in self.list:
                 r1 = rq.get(self.url, headers=self.h, cookies=self.c).content
                 p = bt(r1, 'html.parser').find('button', id="down").get('onclick').split("'")[1]
                 self.r = self.url
                 r2 = bt(rq.get(p, headers=self.h, cookies=self.c).content, 'html.parser').find('meta').get('content').split('=',1)[1]
                 self.r = p
                 r3 = bt(rq.get(r2, headers=self.h, cookies=self.c).content, 'html.parser').find('div', align="center")
                 if r3 == None:
                    r3 = bt(rq.get(r2, headers=self.h, cookies=self.c).content, 'html.parser')
                    f = r3.find('h4').text
                    return f
                 else:
                    s = r3.find('h6').text
                    i = r3.find('a', class_="btn btn-outline-light btn-user font-weight-bold").get('href')
                    return i



def gdt(update, context):
    bot = context.bot
    try:
        args = update.message.text.split(" ", maxsplit=1)
        if len(args) > 1:
            txt = args[1]
            links = re.findall(r'\bhttps?://.*gdtot\S+', txt)
            LOGGER.info(links)
            for link in links:
              link = gdtot(link).parse(bot, update)
              if 'google' in link:
                gd = gdriveTools.GoogleDriveHelper()
                res, size, name, files = gd.helper(link)
                result, button = gd.clone(link)
                if update.message.from_user.username:
                  uname = f'@{update.message.from_user.username}'
                else:
                  uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                if uname is not None:
                  cc = f'\n\n<b>cc: </b>{uname}'
                sendMarkup(result + cc, context.bot, update, button)
              else:
                sendMessage(link, context.bot, update)
        else:
            sendMessage('⫸ Provide a GDTOT link with command', bot, update)
    except Exception as e:
        sendMessage(f"⫸ Invalid Link, If you don't trust me check logs...", bot, update)
        LOGGER.info("Error Occured : "+str(e))
        return


gdtot_handler = CommandHandler("gdtot", gdt, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(gdtot_handler)
from telegram.ext import CommandHandler, run_async
from telegram import Bot, Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bs4 import BeautifulSoup
import requests
import re
import io

def cc_scrapper(update, context):
    bot = context.bot
    try:
        args = update.message.text.split(" ", maxsplit=1)
        if len(args) > 1:
            link = args[1]
            try:
                raw_data = BeautifulSoup(requests.get(link).text,'html.parser')
                regex = r'[0-9]+\|[0-9]+\|[0-9]+\|[0-9]+'
                matches = re.findall(regex, str(raw_data))
                matches = "\n".join(matches)
            except Exception as e:
                sendMessage(f'⫸ <b>Something went wrong while parsing the site, Please check logs</b>',bot, update)
                LOGGER.info("Error Occured : "+str(e))
                return
            try:
                with io.BytesIO(str.encode(matches)) as out_file:
                    out_file.name = "cc_scrapper.txt"
                    bot.send_document(
                        chat_id=update.effective_chat.id, document=out_file)
            except Exception as e:
                sendMessage(f'<b>Something went wrong while sending the Output File, Please check logs</b>',bot, update)
                LOGGER.info("Error Occured : "+str(e))
                return
        else:
            sendMessage('⫸ Provide a Control C link with command', bot, update)

    except Exception as e:
        sendMessage(f'⫸ <b>Something went wrong in Scrapper Module, Please check logs</b>', bot, update)
        LOGGER.info("Error Occured : "+str(e))
        return

cc_handler = CommandHandler("cc", cc_scrapper, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,run_async=True)
dispatcher.add_handler(cc_handler)
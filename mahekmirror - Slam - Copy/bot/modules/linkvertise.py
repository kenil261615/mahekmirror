from telegram.ext import CommandHandler
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, editMessageWithoutPreview
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
import requests

msg_txt = """
<b>⫸ Source URL</b> : {}

<b>⫸ Bypassed URL</b> : {}
"""


def lv_bypass(update,context):
    try:
        link = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Bypassing Link Vertise: {link}")
        reply = sendMessage('⫸ Bypassing..... Please wait!', context.bot, update)
        _apiurl = f"https://bypass.bot.nu/bypass2?url={link}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        try:
            resp = requests.get(_apiurl, headers=headers)
            if resp.status_code == 200:
                jresp = resp.json()
                src_url = f"{link}"
                editMessageWithoutPreview(msg_txt.format(src_url, jresp["destination"]), reply)
            elif resp.status_code == 415 or resp.status_code == 422:
                editMessage("⫸ Invalid Source URL", reply)
            elif resp.status_code == 404:
                jresp = resp.json()
                msg = "{}\n\nPlugin : {}"
                editMessage(msg.format(jresp["msg"], jresp["plugin"]), reply)
            else:
                msg = "⫸ API Status Code {}"
                editMessage(msg.format(str(resp.status_code)), reply)
        except BaseException as e:
            editMessage(f"Error : {e}", reply)
    
    except IndexError:
        sendMessage('⫸ Send a Linkvertise URL along with command', context.bot, update)


lv_handler = CommandHandler(BotCommands.ByPassCommand, lv_bypass,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,run_async=True)
dispatcher.add_handler(lv_handler)
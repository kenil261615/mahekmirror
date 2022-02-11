import subprocess
from bot import LOGGER, dispatcher
from telegram import ParseMode
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
import re
import requests

def get_title(data):
    matches = []
    r1 = r'INFO  : [a-zA-Z0-9. \&\-\[\]]+'
    r2 = r'Copied \(new\) to: [a-zA-Z0-9. \&\-\[\]]+'
    matches = re.findall(r2, data)
    if matches == []:
        matches = re.findall(r1, data)
    return matches[0]

def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        message.reply_text('No command to execute was given.')
        return
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        if 'Copied (new)' in stdout and 'rclone' in cmd:
            index = 'https://geek.parker-gd.workers.dev/2:/'
            title = get_title(stdout)
            title = title.replace('INFO  : ','')
            title = title.replace('Copied (new) to: ','')
            url_path = requests.utils.quote(title)
            link = index + url_path
            reply += f"*Stdout*\n`{link}`\n"
            LOGGER.info(f"Shell - {cmd} - {stdout} Index - {link}")
        else:
            reply += f"*Stdout*\n`{stdout}`\n"
            LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


SHELL_HANDLER = CommandHandler((BotCommands.ShellCommand,"s"), shell, 
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(SHELL_HANDLER)

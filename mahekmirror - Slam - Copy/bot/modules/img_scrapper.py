from telegram.ext import CommandHandler, run_async
from telegram import Bot, Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bs4 import BeautifulSoup as bt
import requests as rs
import re
from pytube import Playlist as pl

def img_scrapper(update, context):
    bot = context.bot
    try:
        args = update.message.text.split(" ", maxsplit=1)
        if len(args) > 1:
            link = args[1]
            if 'vectorstock' in link:
                try:
                    vs_regex = r"https\:\/\/cdn[0-9]+.vectorstock.com\/i\/1000x1000\/[a-zA-Z0-9/-]+.[a-z]+"
                    soup = bt(rs.get(link).text,'html.parser')
                    vector_links = re.findall(vs_regex, str(soup))
                except Exception as e:
                    sendMessage(f'⫸ <b>Something went wrong while parsing the vectorstock site, Please check</b> /{BotCommands.LogCommand}',bot, update)
                    LOGGER.info("Error Occured : "+str(e))
                    return
                try:
                    cap = f'<a href="{vector_links[0]}">Image URL</a>'
                    bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap, parse_mode='HTMl', document=vector_links[0])
                except Exception as e:
                    sendMessage(f'<b>Something went wrong while sending the Vector Image, Please check</b> /{BotCommands.LogCommand}',bot, update)
                    LOGGER.info("Error Occured : "+str(e))
                    return
            elif 'netflix' in link:
                def get_nf_img(string):
                    start = string.find('url("')
                    end = string.find('")')
                    url = string[start+len('url("'):end]
                    return url
                try:
                    soup = bt(rs.get(link).text,'html.parser')
                    logo = soup.find('img', class_='logo')['src']
                    m_img = get_nf_img(soup.find('div',class_='hero-image hero-image-mobile').get('style'))
                    d_img = get_nf_img(soup.find('div',class_='hero-image hero-image-desktop').get('style'))
                except Exception as e:
                    sendMessage(f'⫸ <b>Something went wrong while parsing the netflix site, Please check</b> /{BotCommands.LogCommand}',bot, update)
                    LOGGER.info("Error Occured : "+str(e))
                    return
                try:
                    cap1 = f'<a href="{logo}">Logo Thumbnail URL</a>'
                    bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap1, parse_mode='HTMl', document=logo)
                    cap2 = f'<a href="{m_img}">Mobile Thumbnail URL</a>'
                    bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap2, parse_mode='HTMl', document=m_img)
                    cap3 = f'<a href="{d_img}">Desktop Thumbnail URL</a>'
                    bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap3, parse_mode='HTMl', document=d_img)
                except Exception as e:
                    sendMessage(f'<b>Something went wrong while sending the Netflix Images, Please check</b> /{BotCommands.LogCommand}',bot, update)
                    LOGGER.info("Error Occured : "+str(e))
                    return

            elif 'youtu.be' or 'youtube' in link:
                def get_thumb(video_url):
                    thumb = bt(rs.get(video_url).text,'html.parser').find('link', rel='image_src').get('href')
                    return thumb
                if 'playlist' in link:
                    try:
                        playlist = pl(link)
                        for video in range(len(playlist)):
                            url = playlist[video]
                            th_url = get_thumb(url)
                            cap = f'<a href="{th_url}">{video+1}) Video Thumbnail URL</a>'
                            bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap, parse_mode='HTMl', document=th_url)
                    except Exception as e:
                        sendMessage(f'<b>Something went wrong while sending the Youtube Playlist Videos Thumbnail, Please check</b> /{BotCommands.LogCommand}',bot, update)
                        LOGGER.info("Error Occured : "+str(e))
                        return
                elif '/c/' in link or '/channel/' in link:
                    try:
                        r_b = r'"banner":{"thumbnails":[{"url":"http(s)://[a-zA-Z0-9._()/]+.[a-zA-Z0-9]+\/[a-zA-Z0-9._()/\-\=\,]+","width":1060,"height":175}'
                        r_a = r'"avatar":{"thumbnails":[{"url":"http(s)://[a-zA-Z0-9._()/]+.[a-zA-Z0-9]+\/[a-zA-Z0-9._()/\-\=\,]+","width":48,"height":48}'
                        r_endpart = r'-fcrop64=[a-zA-Z0-9\,\-]+'
                        soup = bt(rs.get(link).text,'html.parser')
                        avatar_tag = re.findall(r_a,str(soup))[0]
                        avatar = avatar_tag.replace('"avatar":{"thumbnails":[{"url":"','')
                        avatar = avatar.replace('","width":48,"height":48}','')
                        avatar = avatar.replace('=s48-c-k-c0x00ffffff-no-rj','')
                        banner_tag = re.findall(r_b,str(soup))[0]
                        banner = banner_tag.replace('"banner":{"thumbnails":[{"url":"','')
                        banner = banner.replace('","width":1060,"height":175}','')
                        banner = re.sub('-fcrop64=[a-zA-Z0-9\,\-]+','',banner)

                        cap1 = f'<a href="{avatar}">Channel Avatar URL</a>'
                        bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap1, parse_mode='HTMl', document=avatar)

                        cap2 = f'<a href="{banner}">Channel Banner URL</a>'
                        bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap2, parse_mode='HTMl', document=banner)
                    except Exception as e:
                        sendMessage(f'<b>Something went wrong while sending the Avatar & Banner Images of Youtube Channel, Please check</b> /{BotCommands.LogCommand}',bot, update)
                        LOGGER.info("Error Occured : "+str(e))
                        return
                else:
                    try:
                        vid_th = get_thumb(link)
                        cap = f'<a href="{vid_th}">Video Thumbnail URL</a>'
                        bot.sendDocument(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, caption=cap, parse_mode='HTMl', document=vid_th)
                    except Exception as e:
                        sendMessage(f'<b>Something went wrong while sending the Youtube Video Thumbnail, Please check</b> /{BotCommands.LogCommand}',bot, update)
                        LOGGER.info("Error Occured : "+str(e))
                        return
            else:
                sendMessage('⫸ Unsupported URL !!', bot, update)

        else:
            sendMessage('⫸ Provide a link with command\n\nSupported Sites: vectorstock, netflix, youtube (videos, channels, playlist)', bot, update)

    except Exception as e:
        sendMessage(f'⫸ <b>Something went wrong in Image Scrapper Module, Please check</b> /{BotCommands.LogCommand}', bot, update)
        LOGGER.info("Error Occured : "+str(e))
        return

img_handler = CommandHandler(BotCommands.ImageScrapperCommand, img_scrapper, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,run_async=True)
dispatcher.add_handler(img_handler)
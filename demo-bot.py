# -*- coding: utf-8 -*-
import logging
import os

from tock.bot import TockBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# asyncio.get_event_loop().set_debug(True)

bot = TockBot()

bot.add_story('greetings', lambda send: send(text="Greetings StoryHander !!!!"))


def goodbye_handler(send):
    send(text="Goodbye1 StoryHander !!!!")
    send(text="Goodbye2 StoryHander !!!!")
    send(text="Goodbye3 StoryHander !!!!")


bot.add_story('goodbye', goodbye_handler)

bot.add_story('gratitude', lambda send: send(text="Gratitude StoryHander !!!!"))

bot.start_websocket(apikey=os.environ['TOCK_APIKEY'])
#bot.start_webhook(host='0.0.0.0', path=os.environ['TOCK_WEBHOOK_PATH'], port=5000)

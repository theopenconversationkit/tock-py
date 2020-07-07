# -*- coding: utf-8 -*-
import asyncio
import logging
import os

from tock.server import Webhook, TockMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

asyncio.get_event_loop().set_debug(True)

Webhook(
    mode=TockMode.WEBHOOK,
    path=os.environ['TOCK_WEBHOOK_PATH']
)

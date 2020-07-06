# -*- coding: utf-8 -*-
import asyncio
import logging
import os

from tock.server import TockServer, TockMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

asyncio.get_event_loop().set_debug(True)

TockServer(
    mode=TockMode.WEBHOOK,
    path=os.environ['TOCK_WEBHOOK_PATH']
)

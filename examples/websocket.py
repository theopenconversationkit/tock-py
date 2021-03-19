import logging
import os

from tock.bot import TockBot
from tock.bus import TockBotBus
from tock.story import story

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# First create story that handle "greetings" intent
@story(
    intent="greetings",
    other_starter_intents=[],
    secondary_intents=[]
)
def greetings(bus: TockBotBus):
    bus.send("Hello i'm a tock-py bot")

# If decorator @story is not provided, the intention with the function name is user
def goodbye(bus: TockBotBus):
    bus.send("Hello i'm a tock-py bot")

# Configure your bot and start it
TockBot() \
    .register_story(greetings) \
    .register_story(goodbye) \
    .start_websocket(apikey=os.environ['TOCK_APIKEY'])

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
    intent="whoareyou",
    other_starter_intents=[],
    secondary_intents=[]
)

def whoareyou(bus: TockBotBus):
    # Get user message
    user_message = bus.request.message.text
    entities = bus.request.entities

    logging.info(f"The user sent: {user_message}")
    logging.info(f"The entities sent: {entities}")

    # Get user name if provided as entities for role 'name'

    if entities:
        first_entity = entities[0]
        role = first_entity.role        # 'name'
        content = first_entity.content  # 'stephan'
    
        logging.info(f"Role: {role}")
        logging.info(f"Content: {content}")


    # Store message in session history
    history = bus.session.get_item("history") or []
    history.append(user_message)
    bus.session.set_item("history",history)

    for msg in history:
        logging.info('--------')
        logging.info(msg)
        logging.info('--------')
    
    if entities and role == 'name':
        response = f"I am a virtual assistant created to help you, {content}. How can I assist you?"
    else:
        response = "I am a virtual assistant created to help you. How can I assist you?"
    bus.send(response)

@story(
    intent="howareyouworking",
    other_starter_intents=[],
    secondary_intents=[]
)

def howareyouworking(bus: TockBotBus):
    user_message = bus.request.message.text
    logging.info(f"The user sent: {user_message}")

    history = bus.session.get_item("history") or []
    history.append(user_message)
    bus.session.set_item("history",history)

    for msg in history:
        logging.info('--------')
        logging.info(msg)
        logging.info('--------')

    # Bot response
    response = "I work thanks to an artificial intelligence that analyzes your messages and provides tailored responses."
    bus.send(response)
    logging.info(f"Bot responded: {response}")



# Configure your bot and start it as a webhook service
service_port = int(os.getenv("PORT",5000))

TockBot() \
    .register_story(whoareyou) \
    .register_story(howareyouworking) \
    .start_webhook("0.0.0.0", "tock-py", service_port)
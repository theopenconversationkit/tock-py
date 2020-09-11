# -*- coding: utf-8 -*-
import logging
import os
from typing import List

from tock.bot import TockBot
from tock.bus import TockBotBus
from tock.intent import Intent
from tock.models import Sentence, Card, AttachmentType, Carousel
from tock.story import Story, story

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# asyncio.get_event_loop().set_debug(True)

class DemoBotBus(TockBotBus):

    @property
    def person(self) -> str:
        entity = self.context.entity("person")
        if entity:
            return entity.content


@story(
    intent="biography",
    other_starter_intents=["person"],
    secondary_intents=["birthdate"]
)
def culture(bus: DemoBotBus):
    def ask_person():
        bus.send(
            Sentence.Builder(f"Who do you want to see?")
                .add_suggestion("Mozart")
                .add_suggestion("Molière")
                .add_suggestion("Napoléon")
                .build()
        )

    def answer_birthdate():
        bus.send(
            Sentence.Builder(f"{bus.person} was born in 1500")
                .add_suggestion("En savoir plus")
                .build()
        )

    def answer_biography():
        bus.send(
            Sentence.Builder(f"{bus.person} was a great person !!!")
                .add_suggestion("En savoir plus")
                .build()
        )

    person_undefined: bool = bus.person is None
    ask_birthdate: bool = bus.is_intent("birthdate")

    if person_undefined:
        ask_person()
    elif ask_birthdate:
        answer_birthdate()
    else:
        answer_biography()


class GreetingStory(Story):

    @staticmethod
    def intent() -> Intent:
        return Intent("greetings")

    @staticmethod
    def other_starter_intents() -> List[Intent]:
        return []

    @staticmethod
    def secondary_intents() -> List[Intent]:
        return []

    def answer(self, bus: DemoBotBus):
        bus.send(Sentence.Builder("Message from greeting story").build())
        card = Card \
            .Builder() \
            .with_title("Card title") \
            .with_sub_title("Card sub title") \
            .with_attachment("https://www.sncf.com/themes/sncfcom/img/favicon.png", AttachmentType.IMAGE) \
            .add_action("visit", "http://www.sncf.com") \
            .build()
        bus.send(
            card
        )
        bus.send(
            Carousel
                .Builder()
                .add_card(card)
                .add_card(card)
                .add_card(card)
                .build()
        )


def goodbye(bus: DemoBotBus):
    bus.send("Goodbye message 1!!!!")
    bus.send("Goodbye message 2!!!!")


def error(bus: DemoBotBus):
    bus.send(Sentence.Builder("Error StoryHander !!!!")
             .add_suggestion("Retry")
             .build())


TockBot() \
    .namespace("elebescond") \
    .register_bus(DemoBotBus) \
    .register_story(GreetingStory) \
    .register_story(culture()) \
    .add_story('goodbye', goodbye) \
    .error_handler(error) \
    .start_websocket(apikey=os.environ['TOCK_APIKEY'])
# .start_websocket(apikey=os.environ['TOCK_APIKEY'], host="bot-api", port=80, protocol="ws")

# .start_webhook(host='0.0.0.0', path=os.environ['TOCK_WEBHOOK_PATH'], port=5000)

# tock-py

Build chatbots using Tock and Python

## DISCLAIMERS

 - Work in progress
 - Not production ready 
  - not yet implemented
    - Managing User / conversational context
    - Testing
    
## Prerequisites

Run a Tock bot in API mode

Create a Bot application using the web connector type in Tock Studio and get your API key

### Environment

We suggest you to create an isolated Python virtual environment:

    $ python3 -m venv env
    $ source env/bin/activate
    
Install tock-py on your project

    $ pip install tock-py

## Usage

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


    # You can also use webhook mode
    # TockBot() \
    #     .register_story(greetings) \
    #     .register_story(goodbye) \
    #     .start_webhook("0.0.0.0", "tock-py", 5000)

# Sentence

    bus.send("Hello i'm a tock sentence")
    
# Suggestion

    bus.send(
        Sentence.Builder("Hello i'm a tock sentence")
            .add_suggestion("with suggestion")
            .build()
    )

# Card with action

    bus.send(
        Card
            .Builder()
            .with_title("card title")
            .with_sub_title("with subtitle")
            .with_attachment("https://www.sncf.com/themes/sncfcom/img/favicon.png", AttachmentType.IMAGE)
            .add_action("visit", "http://www.sncf.com")
            .build()
    )

# Carousel
    card = Card \
        .Builder() \
        .with_title("Card title") \
        .with_sub_title("wit subtitle") \
        .with_attachment("https://www.sncf.com/themes/sncfcom/img/favicon.png", AttachmentType.IMAGE) \
        .add_action("visit", "http://www.sncf.com") \
        .build()
        
    bus.send(
        Carousel
            .Builder()
            .add_card(card)
            .add_card(card)
            .add_card(card)
            .build()
    )
    
# Custom state

Your bot can store custom state data in session

    def greetings(bus):
        if bus.session.get_item("greetings_flag") is None:
            bus.send("Welcome")
        else:
            bus.send("Welcome back")
        bus.session.set_item("greetings_flag", True)
        
You can clear session

    def goodbye(bus):
        bus.session.clear()
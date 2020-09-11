# tock-py

Build chatbots using Tock and Python

## DISCLAIMERS

 - Work in progress
 - Not production ready 
 - Only support text message response.
 - not yet implemented
    - carousel / card / quickplies
    - Exposing entities to storyHander
    - Managing User / conversational context
    - Testing
    - Packaging
    
## Prerequisites

Run a Tock bot in API mode

Create a Bot application using the web connector type in Tock Studio and get your API key

### Environment

We suggest you to create an isolated Python virtual environment:

    $ python3 -m venv env
    $ source env/bin/activate
    
Install dependencies

    $ make init

## Usage Websocket mode

    from tock.bot import TockBot

    bot = TockBot()

    bot.add_story('greetings', lambda send: send(text="Greetings StoryHander !!!!"))

    bot.start_websocket(apikey=os.environ['TOCK_APIKEY'])

## Usage Webhook mode

    from tock.bot import TockBot

    bot = TockBot()

    bot.add_story('greetings', lambda send: send(text="Greetings StoryHander !!!!"))

    bot.start_webhook(host='0.0.0.0', path=os.environ['TOCK_WEBHOOK_PATH'], port=5000)
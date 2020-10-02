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
    
    # Configure your bot and start it
    TockBot() \
        .register_story(greetings()) \
        .start_websocket(apikey=os.environ['TOCK_APIKEY'])

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
# Persistence
It's possible to persist  the context of current_user which is show in this class :

    class Context:

    def __init__(self,
                 user_id: UserId,
                 current_story: Optional[str] = None,
                 previous_intent: Optional[Intent] = None,
                 entities: List[Entity] = []):
        self.__current_story: Optional[str] = current_story
        self.__previous_intent: Optional[Intent] = previous_intent
        self.__entities = entities
        self.__user_id: UserId = user_id

    def entity(self, entity_type: str) -> Optional[Entity]:
        for entity in reversed(self.entities):
            parts = split(':', entity.type)
            parts.reverse()
            if parts[0] == entity_type:
                return entity

    @property
    def current_story(self):
        return self.__current_story

    @current_story.setter
    def current_story(self, story: str):
        self.__current_story = story

    @property
    def previous_intent(self):
        return self.__previous_intent

    @previous_intent.setter
    def previous_intent(self, intent: Intent):
        self.__previous_intent = intent

    @property
    def user_id(self):
        return self.__user_id

    def add_entities(self, entities: List[Entity]):
        self.__entities = self.__entities + entities

    @property
    def entities(self):
        return self.__entities

The persistence method which is named "use_contexts" is called in the file test.py :

    bot: tock.bot.TockBot = tock.bot.TockBot() \
    .namespace(namespace) \
    .use_contexts(FileContexts("./tmp/toto")) \
    .register_bus(DemoBotBus) \
    .register_story(GreetingStory) \
    .register_story(culture()) \
    .add_story('goodbye', goodbye) \
    .error_handler(error)

She is declared in the file bot.py :
    
     def use_contexts(self, contexts: Contexts):
        self.__contexts = contexts
        return self

The persistence process propose different ways to **save** the context of the current user.

1.**In Memory**

By default the context is saved in memory, so if  the bot is stopped, the context will be lost. 
The corresponding function is in the file tock-py/tock/context/memory.py
   
    class MemoryContexts(Contexts):
    def __init__(self):
        self.__contexts: List[Context] = []

    def getcontext(self, user_id: UserId) -> Context:
        for context in self.__contexts:
            if context.user_id == user_id:
                return context

        return Context(user_id)

    def save(self, context: Context):
        for item in self.__contexts:
            if item.user_id == context.user_id:
                self.__contexts.remove(item)
        self.__contexts.append(context)

2.**In a File**

It can also be saved in a binary file through the python method **"pickle"**.
More informations about pickle here : https://docs.python.org/3/library/pickle.html .

The corresponding function is in the file tock-py/tock/context/file.py :

    class FileContexts(Contexts):
    def __init__(self, basepath: str = './'):
        self.__basepath = basepath

    def getcontext(self, user_id: UserId) -> Context:
        filename = self.__filename(user_id)
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                context = pickle.load(f)
            return context
        else:
            return Context(user_id)

    def save(self, context: Context):
        if not os.path.exists(self.__basepath):
            os.makedirs(self.__basepath)
        user_file = self.__filename(context.user_id)
        with open(user_file, "wb") as f:
            pickle.dump(context, f)

    def __filename(self, user_id: UserId):
        return self.__basepath + '/' + user_id.id + '.pkl'

It's possible to choose the directory that will contain the file, if it doesn't exist
the program will create it thanks to this part of code :
            
            if not os.path.exists(self.__basepath):
            os.makedirs(self.__basepath)
It's also possible to implement an other way of backup, for example a data base.
It's possible thanks to architecture of the code: the different ways of saving are  concrete classes which inherits from one abstract class which is :

    
    class Contexts(ABC):

    @abstractmethod
    def getcontext(self, user_id: UserId):
        pass

    @abstractmethod
    def save(self, context: Context):
        pass



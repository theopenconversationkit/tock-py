# -*- coding: utf-8 -*-
from datetime import datetime


def buildMessage(text):
    return {
        "delay": 0,
        "suggestions": [],
        "text": {
            "text": text,
            "args": [],
            "toBeTranslated": True,
            "length": text.__len__()
        },
        "type": "sentence"
    }


def buildBotResponse(request_id, messages):
    return {
        "botResponse": {
            "context": {
                "date": datetime.now(),
                "requestId": request_id
            },
            "entities": [],
            "messages": messages,
            "storyId": "python_story"
        },
        "requestId": request_id
    }
# return TockMessage(
#     requestId=request_id,
#     botResponse=BotResponse(
#         messages=[
#             BotMessageSentence(
#                 text=text,
#                 suggestions=[],
#                 delay=1000
#             )
#         ],
#         storyId="python_story",
#         step=None,
#         entities=[],
#         context=ResponseContext(
#             requestId=request_id,
#             date=datetime.now()
#         )
#     )
# )

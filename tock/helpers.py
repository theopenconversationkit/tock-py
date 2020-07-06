# -*- coding: utf-8 -*-
from datetime import datetime


def buildMessage(request_id, text):
    return {
        "botResponse": {
            "context": {
                "date": datetime.now(),
                "requestId": request_id
            },
            "entities": [],
            "messages": [
                {
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
            ],
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

# -*- coding: utf-8 -*-
from datetime import datetime


#  TODO Using classes models.py
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

# -*- coding: utf-8 -*-

from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import random, string

import FakeServer
from bot import MoMoBot

random.seed(25500889)
LINEBOT_CHANNEL_ACCESS_TOKEN = ''.join(random.choices(string.hexdigits, k=25))
LINEBOT_CHANNEL_SECRET = ''.join(random.choices(string.hexdigits, k=25))

def test_myself():
    client = FakeServer.HttpClient()
    line_bot_api = LineBotApi(LINEBOT_CHANNEL_ACCESS_TOKEN, http_client = client)

    bot = MoMoBot(line_bot_api)

    handler = WebhookHandler(LINEBOT_CHANNEL_SECRET)
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        bot.handle_message(event)

    bot.set_handler(handler)
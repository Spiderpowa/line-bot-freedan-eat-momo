from bot import MoMoBot
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.models import (
    MessageEvent, TextMessage,
)
import os

line_bot_api = LineBotApi(os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN'])

app = MoMoBot(line_bot_api)

handler = WebhookHandler(os.environ['LINEBOT_CHANNEL_SECRET'])
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    app.handle_message(event)

app.set_handler(handler)

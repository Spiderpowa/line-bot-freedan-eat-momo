from bot import MoMoBot
from linebot import (
    LineBotApi, WebhookHandler
)
import os

line_bot_api = LineBotApi(os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINEBOT_CHANNEL_SECRET'])
app = MoMoBot(line_bot_api, handler)
app.run()

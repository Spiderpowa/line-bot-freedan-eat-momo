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


class MoMoBot:
    def __init__(self, line_bot_api):
        self.app = Flask(__name__)
        self.line_bot_api = line_bot_api
        self.handler = None

        self.app.add_url_rule("/callback", None,
                              self.__callback, methods=['POST'])

    def set_handler(self, handler):
        self.handler = handler

    def handle_message(self, event):
        print(event)
        if '吃MoMo'.casefold() in event.message.text.casefold():
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='京站MoMo訂位專線:(02)2550-0889'))
        if event.source.user_id is None:
            return
        if event.source.type == 'user':
            profile = self.line_bot_api.get_profile(event.source.user_id)
        elif event.source.type == 'group':
            profile = self.line_bot_api.get_group_member_profile(
                event.source.group_id, event.source.user_id)
        print(profile)
        freedan = ['FreeDan', '弗力丹', '阿丹']
        for name in freedan:
            if (name in profile.display_name and
                ('吃什麼' in event.message.text or
                 '吃甚麼' in event.message.text or
                 '吃啥' in event.message.text)):
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='阿丹吃MoMo阿'))
                return

    def __callback(self):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        self.app.logger.info("Request body: " + body)

        if self.handler is None:
            abort(202)  # Accept

        # handle webhook body
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'

    def run(self):
        self.app.run()

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


if __name__ == "__main__":
    line_bot_api = LineBotApi(os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN'])

    bot = MoMoBot(line_bot_api)

    handler = WebhookHandler(os.environ['LINEBOT_CHANNEL_SECRET'])

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        bot.handle_message(event)

    bot.set_handler(handler)
    bot.run()

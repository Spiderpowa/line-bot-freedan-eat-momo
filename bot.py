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

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINEBOT_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    if '吃MoMo' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='京站MoMo訂位專線:(02)2550-0889'))
    if event.source.type == 'user':
        profile = line_bot_api.get_profile(event.source.user_id)
    elif event.source.type == 'group':
        profile = line_bot_api.get_group_member_profile(
            event.source.group_id, event.source.user_id)
    print(profile)
    freedan = ['FreeDan', '弗力丹', '阿丹']
    for name in freedan:
        if name in profile.display_name:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='阿丹吃MoMo阿'))
            return


if __name__ == "__main__":
    app.run()

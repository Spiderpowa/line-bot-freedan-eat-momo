# -*- coding: utf-8 -*-

from linebot import (
    LineBotApi
)

from linebot.models import (
    MessageEvent
)

from linebot.models.sources import (
    SourceUser
)

from linebot.models.messages import (
    TextMessage
)

from linebot.models.responses import (
    Profile
)

from bot import MoMoBot
from unittest.mock import MagicMock
import pytest


class TestMoMoBot:
    @pytest.fixture(scope='class')
    def line_bot_api(self):
        return LineBotApi('access_token')

    @pytest.fixture(scope='class')
    def bot(self, request, line_bot_api):
        return MoMoBot(line_bot_api)

    def test_momo_phone(self, bot, line_bot_api):
        profile = Profile(display_name="RandomGuy")

        line_bot_api.get_profile = MagicMock(return_value=profile)
        line_bot_api.get_group_member_profile = MagicMock(return_value=profile)

        source = SourceUser("Uxxxxxxxxx")
        message = TextMessage()
        event = MessageEvent(source=source, message=message)

        # Test '吃MoMo' case insensitive
        line_bot_api.reply_message = MagicMock()
        message.text = "吃MoMo"
        bot.handle_message(event)
        message.text = "吃momo"
        bot.handle_message(event)
        message.text = "來吃mOmO"
        bot.handle_message(event)
        message.text = "想吃MOMO阿"
        bot.handle_message(event)

        assert line_bot_api.reply_message.call_count == 4
        for (reply, _) in line_bot_api.reply_message.call_args_list:
            assert reply[1].text == '京站MoMo訂位專線:(02)2550-0889'

        # Test normal message
        line_bot_api.reply_message.reset_mock()
        message.text = "沒有要吃喔"
        bot.handle_message(event)
        assert line_bot_api.reply_message.call_count == 0

    def test_freedan(self, bot, line_bot_api):
        source = SourceUser("Uxxxxxxxxx")
        event = MessageEvent(source=source,
                             message=TextMessage(text="RandomMessage"))
        line_bot_api.reply_message = MagicMock()

        profile = Profile()
        line_bot_api.get_profile = MagicMock(return_value=profile)

        # Test 'FreeDan' and his possible name and message
        profile.display_name = 'FreeDan - 啊哈'
        event.message.text = '今天晚餐吃甚麼?'
        bot.handle_message(event)
        event.message.text = '今天晚餐吃什麼?'
        bot.handle_message(event)
        event.message.text = '今天晚餐吃啥?'
        bot.handle_message(event)

        profile.display_name = '數學教師弗力丹'
        event.message.text = '今天午餐吃甚麼?'
        bot.handle_message(event)
        event.message.text = '今天午餐吃什麼?'
        bot.handle_message(event)
        event.message.text = '今天午餐吃啥?'
        bot.handle_message(event)

        profile.display_name = '阿丹不是阿舟'
        event.message.text = '明天早餐吃甚麼?'
        bot.handle_message(event)
        event.message.text = '明天早餐吃什麼?'
        bot.handle_message(event)
        event.message.text = '明天早餐吃啥?'
        bot.handle_message(event)

        assert line_bot_api.reply_message.call_count == 9
        for (reply, _) in line_bot_api.reply_message.call_args_list:
            assert reply[1].text == '阿丹吃MoMo阿'

        line_bot_api.reply_message.reset_mock()
        event.message.text = '晚餐吃麥當勞'
        # Test 'FreeDan' and his possible name
        profile.display_name = 'FreeDan - 啊哈'
        bot.handle_message(event)
        profile.display_name = '數學教師弗力丹'
        bot.handle_message(event)
        profile.display_name = '阿丹不是阿舟'
        bot.handle_message(event)

        assert line_bot_api.reply_message.call_count == 0

        line_bot_api.reply_message.reset_mock()
        # Test normal people
        line_bot_api.reply_message.reset_mock()
        profile.display_name = '冰凍麵包'
        bot.handle_message(event)
        assert line_bot_api.reply_message.call_count == 0

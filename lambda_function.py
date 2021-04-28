# -*- coding: utf-8 -*-

# これは、スキルビルダーのハンドラークラスを使用した実装の
# アプローチにより作成された単純なHello WorldのAlexaスキルです。
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import gmaps

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """スキルを起動するハンドラーです。"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "バイクに乗ろう"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("HIROKI2NAIST", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelloWorldIntentHandler(AbstractRequestHandler):
    """ハローワールドインテント用ハンドラー。"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "クラスを使ったPythonの世界へようこそそそそそ。"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ハローワールド", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class ToSchoolIntentHandler(AbstractRequestHandler):
    """home -> school"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ToSchoolIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        slot_time = slots['Time']
        slot_duration = slots['Duration']
        instance = gmaps.Gmaps()
        instance.direction = 'ToSchool'
        instance.set_coordinate()
        if slot_time.value is not None:
            instance.time = slot_time.value
            # instance.get_dep_time()
            speech_text = '{}に出発します'.format(slot_time.value)
        elif slot_duration.value is not None:
            instance.duration = slot_duration.value
            # instance.get_dep_time()
            speech_text = '{}後に出発します'.format(slot_duration.value)
        else:
            speech_text = '安全運転で！'
        instance.get_dep_time()
        ret = instance.get_json()
        speech_text = 'ルート{}で最短{}で到着します'.format(ret[0], ret[1])

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("出発時間は{}で計算　".format(ret[2]), speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class ToHomeIntentHandler(AbstractRequestHandler):
    """school -> home"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ToHomeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        slot_time = slots['Time']
        slot_duration = slots['Duration']
        instance = gmaps.Gmaps()
        instance.direction = 'ToHome'
        instance.set_coordinate()
        if slot_time.value is not None:
            instance.time = slot_time.value
            # instance.get_dep_time()
            # speech_text = '{}に出発します'.format(slot_time.value)
        elif slot_duration.value is not None:
            instance.duration = slot_duration.value
            # instance.get_dep_time()
            # speech_text = '{}後に出発します'.format(slot_duration.value)
        else:
            speech_text = '安全運転で！'
        instance.get_dep_time()
        ret = instance.get_json()
        speech_text = 'ルート{}で最短{}で到着します'.format(ret[0], ret[1])

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("出発時間は{}で計算　".format(ret[2]), speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Helpインテントのハンドラー。"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "こんにちは。と言ってみてください。"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "ハローワールド", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """CancelおよびStopインテントの単一ハンドラー。"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "さようなら"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ハローワールド", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntentはこれらのロケールで利用できます。
    このハンドラーは、サポートされていないロケールではトリガーされません。
    そのため、どのロケールでも安全にデプロイできます。
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "ハローワールドスキルは、お手伝いできません。"
            "こんにちは。と言ってみてください。")
        reprompt = "こんにちは。と言ってみてください。"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """セッション終了のハンドラー。"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """すべての例外ハンドラーを取得し、例外をログに記録して、
    カスタムメッセージで応答します。
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "申し訳ありません。問題が発生しました。後でもう一度試してください。"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(ToSchoolIntentHandler())
sb.add_request_handler(ToHomeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
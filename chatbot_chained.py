import deepl
from . import chatbot_direct as cd
from .parameters import *

# use os.getenv() for actual deployment in order to hide the API key
translator = deepl.Translator("688506d1-e0db-eb66-9b4f-b2ba1a41dfad:fx")

def translate(text, target_lang):
    return str(translator.translate_text(text, target_lang=target_lang))

start_sequence = "AI:"
restart_sequence = "Human:"
# session_prompt = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. The assistant also talks in very simple English.

# Human: Hello, who are you?
# AI: I am an AI created by OpenAI. What would you like to talk about today?"""

def chat(bot):
    # somewhat ad-hoc way to add context to translation
    separator = "\n\n"
    translated = ""
    def translate_with_context(text, target_lang):
        nonlocal translated
        translated = translate(translated + separator + text, target_lang).split(separator)[1]
        return translated

    def user_hook(input):
        return translate_with_context(input, "EN-US")
    def bot_hook(bot_response):
        return translate_with_context(bot_response, "JA")
    bot.chat(user_hook, bot_hook)

class ChainedChatbot:
    def __init__(self, 
            lang_code="JA", 
            inner_lang_code="EN-US",
            session_prompt="",
            chat_parameters=chat_parameters1):
        self.bot = cd.Chatbot(
            start_sequence,
            restart_sequence,
            session_prompt,
            cd.make_get_bot_response(chat_parameters)
        )
        self.session_prompt = session_prompt  # should be in inner language
        self.lang_code = lang_code
        self.inner_lang_code = inner_lang_code
        self.chat_parameters = chat_parameters
    
    def user_hook(self, input):
        return translate(input, self.inner_lang_code)

    def bot_hook(self, bot_response):
        return translate(bot_response, self.lang_code)

    def get_chat_log(self):
        return self.bot.chat_log
    
    def chat_once(self, input_history):
        return self.bot.chat_once(input_history, self.user_hook, self.bot_hook)

if __name__ == "__main__":
    cd.welcome()
    bot = ChainedChatbot()
    chat(bot)

#     inputs = """どこに住んでる？
# 結婚している？
# 車を持ってる？
# サークルに入ってる？
# 兄弟がいる？何人いる？
# どんなスポーツがすき？
# どんな食べ物が好き？
# どんな音楽が好き？
# あした、大学に来る？
# 今日、宿題がある？
# 毎日、何時に起きる？
# 毎日、洗濯する？
# 毎日、ビデオゲームする？
# 週末、よく何する？
# 子供の時、よく何した？
# 将来、何になりたい？
# 今、何が一番ほしい？
# どこに一番行きたい？
# 冬休みには、何をしたい？
# 日本語が上手になりたいんだけど、どうしたらいい？
# やせたいんだけど、どうしたらいい？
# のどがかわいてるんだけど…
# おなかがすいてるんだけど…
# 今晩、何をするつもり？
# 東京から大阪まで電車でどのぐらいかかる？
# 図書館で大きい声で話してもいい？
# この本、ちょっと借りてもいい？
# 今朝、朝ごはんを食べた？
# メガネをかけてる？
# インド料理を食べたことがある？"""
#
#     def test_chat(query):
#         bot = ChainedChatbot()
#         return bot.chat_once(query)
#
#     outputs = list(map(test_chat, inputs.split("\n")))
#     print("\n".join(outputs))
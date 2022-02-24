import deepl
import chatbot_direct as cd
from parameters import *

# use os.getenv() for actual deployment in order to hide the API key
translator = deepl.Translator("688506d1-e0db-eb66-9b4f-b2ba1a41dfad:fx")

def translate(text, target_lang):
    return str(translator.translate_text(text, target_lang=target_lang))

cd.start_sequence = "AI:"
cd.restart_sequence = "Human:"
cd.session_prompt = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. The assistant also talks in very simple English.

Human: Hello, who are you?
AI: I am an AI created by OpenAI. What would you like to talk about today?"""

cd.chat_parameters = chat_parameters1

def chat():
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
    cd.chat_base(user_hook, bot_hook)

if __name__ == "__main__":
    cd.welcome()
    chat()

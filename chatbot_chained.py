import deepl
from chatbot_direct import *

# use os.getenv() for actual deployment in order to hide the API key
translator = deepl.Translator("688506d1-e0db-eb66-9b4f-b2ba1a41dfad:fx")

def translate(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)

start_sequence = "AI:"
restart_sequence = "Human:"
session_prompt = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

Human: Hello, who are you?
AI: I am an AI created by OpenAI. How can I help you today?"""

chat_parameters = chat_parameters1

def chained_chat():
    chat_log = session_prompt
    while True:
        user_input = translate(input(), "EN-US")
        chat_log += f'\n{restart_sequence} {user_input}\n{start_sequence} '
        bot_response = get_bot_response(chat_log)
        chat_log += bot_response
        print(translate(bot_response, "JA"))
        # print("debug chat_log:\n" + chat_log)

if __name__ == "__main__":
    welcome()
    chained_chat()

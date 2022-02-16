import deepl
from chatbot_direct import *

# use os.getenv() for actual deployment in order to hide the API key
translator = deepl.Translator()

# note: untested code, as we need an api key

def translate(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)

start_sequence = "AI:"
restart_sequence = "Human:"
session_prompt = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

Human: Hello, who are you?
AI: I am an AI created by OpenAI. How can I help you today?
Human:"""

chat_parameters = chat_parameters1

def chained_chat():
    chat_log = session_prompt
    while True:
        # only translate the input. Maybe translating the entire chat
        # log would make the responses better, but that'll also be
        # more expensive
        user_input = translate(input(), "EN")
        chat_log += f'\n{restart_sequence} {user_input}\n{start_sequence} '
        bot_response = translate(get_bot_response(chat_log), "JA")
        chat_log += bot_response
        print(bot_response)

if __name__ == "__main__":
    welcome()
    chained_chat()

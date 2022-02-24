import deepl
from chatbot_direct import *

# use os.getenv() for actual deployment in order to hide the API key
translator = deepl.Translator("688506d1-e0db-eb66-9b4f-b2ba1a41dfad:fx")

def translate(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)

model_name = "けん"
model_name_en = "Ken"
human_name = "ロバート"
human_name_en = "Robert"
situation = "Robert and Ken are vacationing in Okinawa."
opening_line = "ロバートさんはどんなスポーツが好きですか。"

session_prompt = f"""{situation}\n\n{model_name}: {translate(opening_line, "EN-US")}"""

chat_parameters = chat_parameters1


def chained_chat():
    chat_log = f"""{situation}\n\n{model_name_en}: {translate(opening_line, "EN-US")}"""
    print(f"{model_name}: {opening_line}")
    while True:
        print("---")
        print(f"{human_name}: ", end="")
        user_input = translate(input(), "EN-US")
        chat_log += f'\n{human_name}: {user_input}\n{model_name}: '

        print("---")
        bot_response = get_bot_response(chat_log)
        chat_log += bot_response
        print(f"""{model_name}: {translate(bot_response, "JA")}""")
        # print("debug chat_log:\n" + chat_log)

if __name__ == "__main__":
    welcome()
    chained_chat()

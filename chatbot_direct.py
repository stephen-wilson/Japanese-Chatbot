import openai
#import os
from parameters import *

# use os.getenv() for actual deployment in order to hide the API key
openai.api_key = "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"

# for importing, you may want to modify start_sequence,
# restart_sequence, session_prompt, and chat_parameters
start_sequence = "誠:"
restart_sequence = "あなた:"
session_prompt = """誠は優しくて、協力的で、親切で、頭のいいチャットボットです。

あなた: 最近元気ですか？
誠: はい、げんきですか。聞いてくれてありがとうございます。
あなた: 一番好きなアニメは何ですか？
誠: 『進撃の巨人』が一番好きです。あなたは一番好きなアニメが何ですか？
あなた: 私も『進撃の巨人』です。
誠: 『進撃の巨人』はとても楽しいアニメですね。
あなた: そうですね。他のアニメ見ますか？
誠: 他のアニメも楽しんでいます。
あなた: 本当ですか！？
誠: いえ、まだ見ていません。がんばります！
あなた: 嘘つき！
誠: いえ、本当です。勉強になります。
あなた: 今日何したいんですか？
誠: 今日は勉強に励んでいきたいです。
あなた: 何を勉強していますか？
誠: 今日は、友達とコミュニケーションを取っています。
あなた: どうして？
誠: 仕事でも、友達とコミュニケーションを取っていると、とても楽しいです。
あなた: 一番楽しいことが何ですか？
誠: 一番楽しいことは、友達と一緒に過ごすことです。
あなた: いい友達ですね
誠: いい友達です。"""

chat_parameters = chat_parameters0

def get_bot_response(prompt):
    response = openai.Completion.create(
        prompt=prompt,
        stop=[start_sequence, restart_sequence],
        **chat_parameters
    )
    bot_response = response['choices'][0]['text']
    return str(bot_response)

def welcome():
    print("""Welcome to the chatbot!
 NOTE: Please try not to use too many tokens for the chatbot (e.g. a whole paragraph or essay as input for each message) as that will start to reach my quota limit...
 But besides that, feel free to test out the bot! Press 'ctrl C' to stop the chat!
 Type a message to Makoto!""")

def chat_base(user_hook, bot_hook):
    '''
    user_hook is given the user input, and should return text to give to the bot
    bot_hook is given the bot response, and should return text to send to the user
    '''
    chat_log = session_prompt
    while True:
        user_input = user_hook(input())
        chat_log += f'\n{restart_sequence} {user_input}\n{start_sequence} '
        bot_response = get_bot_response(chat_log).strip()
        chat_log += bot_response
        print(bot_hook(bot_response))
        print("debug chat_log:\n" + chat_log)
        
def identity(x):
    return x

def chat():
    chat_base(identity, identity)
        
if __name__ == "__main__":
    welcome()
    chat()

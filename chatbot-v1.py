# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 21:25:01 2022

@author: Stephen
"""

# for using os.getenv() for if it is actually being deployed, in order to hide the API key
#import os
import openai

openai.api_key = "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"

start_sequence = "\n誠: "
restart_sequence = "\nあなた: "
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
# \nあなた: 
chat_log = session_prompt

def chat(chat_input, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence} {chat_input}{start_sequence}'
    response = openai.Completion.create(
      engine="text-curie-001",
      prompt= prompt_text,
      temperature=0.7,
      max_tokens=64,
      top_p=1,
      frequency_penalty=0.1,
      presence_penalty=0,
      stop=["あなた:", "誠:"]
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(chat_input, bot_response, chat_log=None):
    if chat_log == None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {chat_input}{start_sequence}{bot_response}'

print("""Welcome to the chatbot!
 NOTE: Please try not to use too many tokens for the chatbot (e.g. a whole paragraph or essay as input for each message) as that will start to reach my quota limit...
 But besides that, feel free to test out the bot! Press 'ctrl C' to stop the chat!
 Type a message to Makoto!""")
while True:
    user_input = input()
    chat_log = chat_log
    bot_response = chat(user_input, chat_log)
    chat_log = append_interaction_to_chat_log(user_input, bot_response, chat_log)
    print(bot_response)

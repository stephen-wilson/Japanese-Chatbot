# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 21:25:01 2022

@author: Stephen
"""

# for using os.getenv() for if it is actually being deployed, in order to hide the API key
#import os
import openai

openai.api_key = "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"

# translated version of OpenAI's english chatbot session prompt
start_sequence = "AI: "
restart_sequence = "人間: "
session_prompt = """以下は、AIアシスタントとの会話です。このアシスタントは、親切で、創造的で、賢くて、とてもフレンドリーです。

人間: こんにちは、あなたは誰ですか？
AI: 私はOpenAIによって作られたAIです。本日はどのようなご用件でしょうか？"""
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
      stop=[start_sequence, restart_sequence],
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(chat_input, bot_response, chat_log=None):
    if chat_log == None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {chat_input}{start_sequence}{bot_response}'

print("Welcome to the chatbot!\n NOTE: Please try not to use too many tokens for the chatbot (e.g. a whole paragraph or essay as input for each message) as that will start to reach my quota limit...\n But besides that, feel free to test out the bot! Press 'ctrl C' to stop the chat!\n Type a message to Makoto!")
print(session_prompt)
while True:
    print(restart_sequence, end='')
    user_input = input()
    chat_log = chat_log
    bot_response = chat(user_input, chat_log)
    chat_log = append_interaction_to_chat_log(user_input, bot_response, chat_log)
    print(start_sequence + bot_response)
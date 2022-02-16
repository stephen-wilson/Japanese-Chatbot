# Japanese-Chatbot
Research and Development of a Japanese chatbot using various methods such as different API and pretrained models. A Spring 2022 MIT Undergraduate Research Opportunities Program project.

## Organization
`data-log` contains scenarios and chat logs for testing and evaluation of different chatbot models.

`parameters.py` contains various chat parameters to use.

`chatbot_direct.py` implements a GPT-3 Japanese chatbot.

`chatbot_chained.py` implements a DeepL&rarr;GPT-3&rarr;DeepL Japanese chatbot, taking in Japanese, translating it to English, running GPT-3 on it, and then translating back to Japanese.

## How to Use
Chat with the GPT-3 Japanese chatbot by running:

`python chatbot_direct.py`

Chat with the chained Japanese chatbot by running:

`python chatbot_chained.py`

# Japanese-Chatbot
Research and Development of a Japanese chatbot using various methods such as different API and pretrained models. A Spring 2022 MIT Undergraduate Research Opportunities Program project.

## Purpose
Provide an easy-to-use, convenient, non-judgemental, and productive AI language partner for languager learners to practice input and output and develop confidence in their language abilities. This chatbot should also be easy for instructors to use and modify. 

## Features
- [x] Baseline models using API
- [ ] Pretrained models
- [ ] Multiple chatbots
  - [ ] For different ability levels (eg. beginner, intermediate, advanced)
  - [ ] Domain-specific (eg. trip advisor, teacher, student, etc.)
  - [ ] Different personalities
- [ ] Correct user input or Provide feedback
- [ ] Speech-to-text and text-to-speech

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

## Tasks

### Baseline Models
- [x] GPT-3 J->J direct system
- [x] DeepL -> GPT-3 -> DeepL chained system

### Model Improvements/Research
- [x] Improve baseline models
  - [x] Give (part of) chat log to DeepL, slightly improving translation quality
- [ ] Look into using pretrained models
  - [ ] BERT
  - [ ] GPT-2
- [ ] Look into ways for correcting or providing feedback on user input
- [ ] Look into ways to tune difficulty of output (eg. word choice, output length)
- [ ] Make sure the model doesn't output anything inappropriate

### Testing
- Scenarios
  1. [ ] Create multiple scenarios
  2. [ ] Test on different scenarios
  3. [ ] Rate on quality of responses
- Colloquial Japanese
- Different dialects
- [ ] Note down strengths and weaknesses (limitations) of different models (eg. customizability, quality of responses, etc.)

### Journal Research
- [x] Look into English chatbots for ESL

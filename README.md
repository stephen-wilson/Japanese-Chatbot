# Japanese-Chatbot
Research and Development of a Japanese chatbot using various methods such as different API and pretrained models. A Spring 2022 MIT Undergraduate Research Opportunities Program project.

## Purpose
- Use for (Japanese) education
- Able to correct user input
- Easy for Japanese educators to use and modify

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
- [ ] Look into ways for correcting user input
- [ ] Look into ways to tune difficulty of output
- [ ] Look into using pretrained models
- [ ] Make sure the model doesn't output anything inappropriate

### Testing
- Scenarios
  1. [ ] Create multiple scenarios
  2. [ ] Test on different scenarios
  3. [ ] Rate on quality of responses
- Colloquial Japanese
- Different dialects

### Journal Research
- [ ] Look into English chatbots for ESL

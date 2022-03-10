import re

from transformers import T5Tokenizer, AutoModelForCausalLM

tokenizer = T5Tokenizer.from_pretrained("ushikado/yuyuyui-chatbot")
model = AutoModelForCausalLM.from_pretrained("ushikado/yuyuyui-chatbot")

class Interlocutor():
    def __init__(self, tokenizer, model, character_token, initial_line=None,
                 max_context_length=512, max_response_length=128):
        self.tokenizer = tokenizer
        self.model = model
        self.character_token = character_token
        self.max_context_length = max_context_length
        self.max_response_length = max_response_length
        self.context = ""
        if initial_line is not None:
            self.context = f"{character_token}{initial_line}"
        return

    def generate(self, query):
        nanigashi = self.tokenizer.additional_special_tokens[0]
        nanigashi_id = self.tokenizer.additional_special_tokens_ids[0]
        self.context += nanigashi + query + self.tokenizer.eos_token + self.character_token
        context_tensor = self.tokenizer.encode(self.context, add_special_tokens=False, return_tensors="pt")
        context_length = context_tensor.size()[-1]
        if self.max_context_length < context_length:
            context_tensor = context_tensor.narrow(1, context_length - self.max_context_length, self.max_context_length)
            context_length = context_tensor.size()[-1]
        max_length = context_length + self.max_response_length
        context_tensor = self.model.generate(context_tensor, do_sample=True, max_length=max_length,
                                             pad_token_id=self.tokenizer.eos_token_id)
        self.context = re.sub(self.tokenizer.eos_token, "", self.tokenizer.decode(context_tensor[0]))
        response = self.context[self.context.rindex(self.character_token) + len(self.character_token):].strip()
        return response


model_name = "山伏 しずく"
human_name = "某"
opening_line = """どんなスポーツが好きなの？"""
# to continue a conversation, append the rest of the log to the opening line
opening_line = re.sub("\\n\\*?", "", opening_line)

interlocutor = Interlocutor(tokenizer, model, f"<{model_name}>",
                            initial_line=opening_line)
print(interlocutor.context)

def chat():
    while True:
        print(f"<{human_name}>", end="")
        user_input = input()
        if "exit" in user_input:
            break
        if "clear" in user_input:
            continue
        model_input = interlocutor.generate(user_input)
        print(f"*<{model_name}>{model_input}")

if __name__ == "__main__":
    chat()

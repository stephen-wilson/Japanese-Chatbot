import json
from pathlib import Path
import re

def remove_parentheticals(s):
    return re.sub(r'（.*?）|＜.*?＞', '', s)

def load_conversation(data):
    """
    Loads and returns the metadata and conversation. Each turn in the
    conversation is a tuple of the speaker and their utterance.
    """
    metadata = data['メタデータ']
    conversation = data['会話']
    # convert turn into a tuple of speaker and utterance for simplicity
    conversation = [(turn['話者'], turn['発話'])
                    for turn in conversation]
    return metadata, conversation

def clean_conversation(metadata, conversation):
    """
    Removes parentheticals from the conversation
    and stop conversation when ＊ is reached.
    Returns new conversation
    """
    result = []
    for s, u in conversation:
        u = remove_parentheticals(u)
        # note: this is fairly drastic, but we should still have
        # sufficient data for fine-tuning. But keeping it is probably
        # fine? (we can restrict output to not contain ＊ (?))
        # data:
        # original number of turns: 72884
        # claned number of turns: 7248
        if '＊' in u:
            break
        result.append((s, u))
    return result

def format_metadata(metadata):
    place = f"<場所>{metadata['場所']}\n"
    participants = ''.join(f"<参加者>{p['コード']}<描写>{p['描写']}\n"
                             for p in metadata['参加者'])
    relation = metadata['参加者の関係']
    if relation is None:
        relation = ''
    else:
        relation = f"<参加者の関係>{relation}\n"
    return f'{place}{participants}{relation}'

def format_conversation(conversation):
    return '<会話>\n' + '\n'.join(f"<{s}>{u}" for s, u in conversation)

def format_full_conversation(metadata, conversation):
    """
    Formats the conversation so that it is easy to fine-tune on
    """
    data = format_metadata(metadata) + format_conversation(conversation)
    # also replace speaker names: [F023, M016] -> [F1, M2]
    for i, p in enumerate(metadata['参加者'], 1):
        code = p['コード']
        data = data.replace(code, code[0] + str(i))
    return data

if __name__ == '__main__':
    input_directory = Path('nucc_clean/')
    output_directory = Path('nucc_for_finetune/')
    output_directory.mkdir(exist_ok=True)
    
    for filepath in input_directory.glob('*'):
        filename = filepath.name
        with open(filepath) as f:
            data = json.load(f)
            
        metadata, conversation = load_conversation(data)
        conversation = clean_conversation(metadata, conversation)
        
        # skip conversation if less than 10 turns after cleaning
        if len(conversation) < 10:
            continue
        
        print(f'{filename}:{len(conversation)}')
        
        data = format_full_conversation(metadata, conversation)
        
        with open(output_directory / filename, 'w') as f:
            f.write(data)

import json
from pathlib import Path
import re

# speakers are of form Fddd, Mddd, ％ｃｏｍ, Ｘ, X, or ＭＳ
# (eg. X happens for waiters in restaurants)
speaker_regex = r'(?:F\d+|M\d+|％ｃｏｍ|Ｘ|X|ＭＳ)'

def parse_metadata(s):
    """
    Parses the metadata. Returns the metadata and the rest of the
    conversation.
    """
    # match for the first turn; before that is metadata
    metadata, s = re.match(f'(.+?)\n({speaker_regex}：.+)', s, flags=re.DOTALL).groups()
    # some metadata lines don't start with '＠'
    metadata = metadata.replace('\n', '').split('＠')
    assert(metadata[0] == '')
    metadata = metadata[1:]
    return metadata, s

def combine_turns(conversation):
    """
    Combine adjacent turns with the same speaker
    """
    combined = []
    speaker, utterance = conversation[0]
    for turn in conversation[1:]:
        if speaker == turn[0]:
            utterance += turn[1]
        else:
            combined.append((speaker, utterance))
            speaker, utterance = turn
    combined.append((speaker, utterance))
    return combined

def parse_conversation(s):
    """
    Parses the conversation. Output the metadata and the
    conversation as lists. Each turn (element) in the
    conversation is a tuple of the speaker and their utterance.
    """
    metadata, s = parse_metadata(s)
    # remove newlines in the string and split again
    # (the speaker is not always in the beginning of the line)
    s = s.replace('\n', '')
    # allow any number of '：' since duplicates appear sometimes
    conversation = re.split(f'({speaker_regex})：+', s)[1:]
    # remove speakers with no utterance
    conversation = [(s, u) for s, u in zip(conversation[::2], conversation[1::2])
                    if u != '']
    # combine adjacent turns with the same speaker
    conversation = combine_turns(conversation)
    return metadata, conversation

def conversation_speakers(conversation):
    return {t[0] for t in conversation}

def sanity_check(conversation):
    """
    Sanity checks the conversation:
    1. Utterances are non-empty
    2. Utterances don't contain ： nor ＠
    3. Each turn has a different speaker
    Prints the speaker(s) and utterance(s) which fail the sanity check.
    """
    for speaker, utterance in conversation:
        if '：' in utterance or '＠' in utterance:
            print(speaker, utterance)
    # for 1, output context
    for (s1, u1), (s2, u2) in zip(conversation, conversation[1:]):
        if u1 == '' or u2 == '' or s1 == s2:
            print((s1, s2), (u1, u2))

# TODO: japanese for duration, speaker, utterance, description, participants, external speakers
def jsonify_participants(metadata_ps):
    participants = []
    for metadata_p in metadata_ps:
        participant, description = re.match('参加者(.+)：(.+)', metadata_p).groups()
        participants.append({'コード': participant,
                             '描写': description})
    return participants
    
def jsonify_metadata(metadata, speakers):
    data_number, duration = re.match('(?:データ|テープ)：?(\d+)（(.+)）', metadata[0]).groups()
    time, = re.match('(?:収集年月日|日時|収集)：?(.+)', metadata[1]).groups()
    place, = re.match('(?:収集)?場所[：；](.+)', metadata[2]).groups()
    maybe_relation = re.match('参加者(?:間?)の関係：(.+)', metadata[-1])
    if maybe_relation:
        relation, = maybe_relation.groups()
        participants = jsonify_participants(metadata[3:-1])
    else:
        relation = None
        participants = jsonify_participants(metadata[3:])
    external_speakers = list(speakers - {p['コード'] for p in participants})
    return {'データ': data_number,
            '期間': duration,
            '収集年月日': time,
            '場所': place,
            '参加者': participants,
            '参加者の関係': relation,
            '外部話者': external_speakers}

def jsonify_conversation(conversation):
    return [{'話者': t[0], '発話': t[1]}
            for t in conversation]

def clean_nucc(input_directory, output_directory):
    """
    Create a directory for globally-usable cleaned-up nucc files.
    """
    output_directory.mkdir(exist_ok=True)
    for filepath in input_directory.glob('*'):
        print(filepath.name)
        with open(filepath) as f:
            s = f.read()
        # remove last ＠ＥＮＤ line
        # Note: this also appears as @ＥＮＤ and ＠Ｅｎｄ
        s = s.rstrip('\n@＠ＥＮＤｎｄ')
        # for consistency (and my own sanity), remove '　'
        s = s.replace('　', '')
        
        metadata, conversation = parse_conversation(s)

        sanity_check(conversation)

        speakers = conversation_speakers(conversation)
        
        data = {'メタデータ': jsonify_metadata(metadata, speakers),
                '会話': jsonify_conversation(conversation)}
        
        with open(output_directory / f'{filepath.stem}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # Note: I've manually fixed a few human input errors
    # which can be found by sanity check
    input_directory = Path('nucc_fixed/')
    clean_directory = Path('nucc_clean/')
    clean_nucc(input_directory, clean_directory)

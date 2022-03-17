import argparse
import os
import re

def clean_file(s, human_name, model_name):
    lines = []
    model_code = None
    human_code = None
    line = None
    for l in s.split():
        if "＠" in l:
            code = re.match(r"＠参加者([F|M]\d+)", l)
            if code:
                if model_code is None:
                    model_code = code.groups()[0]
                elif human_code is None:
                    human_code = code.groups()[0]
                else:
                    print("too many participants; skipping...")
                    return None
            continue
        delim = "："
        if re.match(r"[F|M]\d+"+delim, l):
            [author, message] = l.split(delim, maxsplit=1)
            author = human_name if author == human_code else \
                model_name if author == model_code else None
            if author is None:
                print("too many participants; skipping...")
                return None
            if line is not None:
                lines.append(line)
            line = author + delim + message
        elif line is not None:
            line += l
    lines.append(line)
    print(len(lines))
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', default="AI")
    parser.add_argument('--human_name', default="人間")
    parser.add_argument('-n', '--filename_format', type=eval, dest="filename_of",
                        default=lambda i: f"data{i+1:03}.txt",
                        help="labeling function (e.g. 0 => 'data001.txt', etc.)")
    parser.add_argument('rawpath', help="path to folder of raw data")
    parser.add_argument('path', help="path to output folder")

    args = parser.parse_args()
    rawpath = args.rawpath
    path = args.path

    assert os.path.isdir(rawpath)
    assert not os.path.isfile(path)
    os.makedirs(path, exist_ok=True)
    print(f"writing from directory '{rawpath}' into '{path}'...")

    i = 0
    while 1:
        fn = args.filename_of(i)
        rawpath_fn = os.path.join(rawpath, fn)
        if not os.path.exists(rawpath_fn): break
        with open(rawpath_fn, mode='r', encoding='UTF-8') as f:
            s = f.read()
        output = clean_file(s, args.human_name, args.model_name)
        if output is not None:
            with open(os.path.join(path, fn), mode='w', encoding='UTF-8') as f:
                f.write(output)
        print(f"cleaned file '{fn}'...")
        i += 1
    print(f"no more files of requested format in '{rawpath}'; done")

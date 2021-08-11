import argparse
from os import replace
import requests
import pprint
import json
import re

api_url = "https://script.google.com/macros/s/AKfycbzKjxnq7rQOY-GDPHIheMeRJ0k_Xc29Xmvi4GL808KFuCQ9pa7DmNGRffAC7qChVoTC/exec"
source = "en"
target = "ja"
input_file = "PyLIS_README.md"

def translate(text_box):
    print(text_box)
    params = {
        'text': text_box,
        'source': source,
        'target': target
    }

    for i in range(10):
        try:
            r_post = requests.post(api_url, data=params)
        except Exception as e:
            print(str(i) + ': ' + e)
            continue

    loadstr = json.loads(r_post.text)
    trans_box = loadstr['text']
    print(trans_box)
    return trans_box

def trans_topic(line):
    ret = {'topic' : False, 'trans' : ""}

    strip = line.strip()
    if (strip == ''):
        return ret
        
    if (strip[0] == '#'):
        strip = strip.strip('# ')
        ret['topic'] = True
        ret['trans'] = translate(strip)
    elif (strip[0] == '-'):
        strip = strip.strip('- ')
        ret['topic'] = True
        ret['trans'] = translate(strip)
    
    if (ret['topic'] and strip == ret['trans']):
        ret['trans'] = ""

    return ret

def is_url_only(line):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    find_url = re.findall(pattern, line)

def is_break(line):
    if (line[0] == '[' or line[0] == '!'):
        return True
    if (line == '\n'):
        return True
    return False

def name_output_file(input_file):
    input_file_1 = input_file[::-1]
    target_str = "_translated_" + target + ".md"
    output_file_1 = input_file_1.replace(".md"[::-1], target_str[::-1], 1)
    return output_file_1[::-1]

def main():
    output_file = name_output_file(input_file)

    fw = open(output_file, 'w')

    text_box = ""
    with open(input_file, 'r', encoding="utf-8") as fr:
        in_codeblock = False

        for line in fr:
            if (line.startswith('```')):
                if in_codeblock:
                    in_codeblock = False
                else:
                    in_codeblock = True

            if in_codeblock:
                if (text_box != ""):
                    trans_box = translate(text_box)
                    fw.write(trans_box)
            else:
                tt = trans_topic(line)
                if (tt['topic']):
                    if (tt['trans'] != ""):
                        line = line.rstrip() + "<br>" + tt['trans'] + '\n'
                elif (is_break(line)):
                    if (text_box != ""):
                        trans_box = translate(text_box)
                        fw.write(trans_box)
                        fw.flush()
                        text_box = ""
                else:
                    text_box += line

            fw.write(line)

        # 最終行
        if (text_box != ""):
            trans_box = translate(text_box)
            fw.write(trans_box)

    fw.close()

if __name__ == "__main__":
    main()

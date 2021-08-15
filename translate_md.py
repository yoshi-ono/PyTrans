import argparse
from os import replace
import requests
import pprint
import json
import re

api_url = "https://script.google.com/macros/s/AKfycbzKjxnq7rQOY-GDPHIheMeRJ0k_Xc29Xmvi4GL808KFuCQ9pa7DmNGRffAC7qChVoTC/exec"
source = "en"
target = "ja"

class TranslateMd():
    def __init__(self, md_file) -> None:
        self.input_file = md_file
        self.output_file = self.name_output_file()
        print(self.input_file, "=>", self.output_file)

    def translate(self, text_box):
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

    def trans_comment(self, line):
        ret = {'comment' : False, 'trans' : ""}

        rip = line.strip()
        if (rip == ''):
            return ret
            
        pos = rip.find('#')
        if (pos >= 0):
            rip = rip[pos:].strip('# ')
            ret['comment'] = True
            ret['trans'] = self.translate(rip)
        
        table = str.maketrans({' ': None, '（': '(', '）': ')', '、': ','})
        if (ret['comment'] and rip.replace(' ', '').lower() == ret['trans'].translate(table).lower()):
            ret['trans'] = ""

        return ret

    def trans_topic(self, line):
        ret = {'topic' : False, 'trans' : ""}

        strp = line.strip()
        if (strp == ''):
            return ret
            
        if (strp[0] == '#'):
            strp = strp.strip('# ')
            ret['topic'] = True
            ret['trans'] = self.translate(strp)
        elif (strp[0] == '-'):
            strp = strp.strip('- ')
            ret['topic'] = True
            ret['trans'] = self.translate(strp)
        
        if (ret['topic'] and strp == ret['trans']):
            ret['trans'] = ""

        return ret

    def is_url_only(self, line):
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        find_url = re.findall(pattern, line)

    def is_break(self, line):
        if (line[0] == '[' or line[0] == '!' or line[0] == '`'):
            return True
        if (line == '\n'):
            return True
        return False

    def name_output_file(self):
        input_file_1 = self.input_file[::-1]
        target_str = "_translated_" + target + ".md"
        output_file_1 = input_file_1.replace(".md"[::-1], target_str[::-1], 1)
        return output_file_1[::-1]

    def start(self):
        fw = open(self.output_file, 'w', encoding="utf-8")

        text_box = ""
        with open(self.input_file, 'r', encoding="utf-8") as fr:
            in_codeblock = False

            for line in fr:
                if (line.startswith('```')):
                    if in_codeblock:
                        in_codeblock = False
                    else:
                        in_codeblock = True

                if in_codeblock:
                    if (text_box != ""):
                        trans_box = self.translate(text_box)
                        fw.write(trans_box)
                        fw.flush()
                        text_box = ""

                    tc = self.trans_comment(line)
                    if (tc['comment']):
                        if (tc['trans'] != ""):
                            line = line.rstrip() + " {" + tc['trans'] + "}\n"
                else:
                    tt = self.trans_topic(line)
                    if (tt['topic']):
                        if (tt['trans'] != ""):
                            line = line.rstrip() + "<br>" + tt['trans'] + '\n'
                    elif (self.is_break(line)):
                        if (text_box != ""):
                            trans_box = self.translate(text_box)
                            fw.write(trans_box)
                            fw.flush()
                            text_box = ""
                    else:
                        text_box += line

                fw.write(line)
                fw.flush()

            # 最終行
            if (text_box != ""):
                trans_box = self.translate(text_box)
                fw.write(trans_box)

        fw.close()

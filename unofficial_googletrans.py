# googletrans は Google 非公式
from googletrans import Translator
 
with open('./test.txt') as f:
    lines = f.readlines()
    f.close()
 
    translator = Translator()
    for line in lines:
        translated = translator.translate(line, dest="ja")
        print(line)  # 翻訳したい文章
        print(translated.text)  # 翻訳後の文章

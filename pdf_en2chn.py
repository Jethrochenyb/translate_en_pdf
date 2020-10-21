import fitz
import re
from googletrans import Translator

translator = Translator(service_urls=[
      'translate.google.cn',])

def numofupper(txt):
    num=0
    for x in txt:
        if x.isupper(): num+=1
        elif x.islower(): num-=1
    return num

def process_sent(x, xx):
    with open('./result.txt', 'a', encoding='UTF-8') as f:
        f.write('\n\r------------------------------------------------')
        f.write('\n\r'+x)
        f.write('\n\r'+xx)

file_pdf = fitz.open("./test3.pdf")

sent= ''
for page in file_pdf:
    t = page.getText()
    context = t.split('\n')
#    print('----------------------------------------------')
    for line_idx in range(len(context)-1):  # 每页最后出问题
        if line_idx == len(context)-3:
            if len(context[line_idx+1])<2: break
            elif context[line_idx+1][-2] == '.':
                    sent += context[line_idx]
                    sent += context[line_idx+1]
                    break
        else: # normal
            if len(context[line_idx]) >=2 and context[line_idx][-2] == '.' and context[line_idx+1][0].isupper():
                sent += context[line_idx]
                sent = re.sub("\(\d+\)", "", sent)  # ref and formula.
                sent = re.sub("\[[^\]]*\]", "", sent)  # [^a] means any but a
                result = translator.translate(sent, src = 'en', dest = 'zh-cn')
                process_sent(sent, result.text)
                sent = ''

            else:
                if context[line_idx][-1] == '-': context[line_idx] = context[line_idx][:-1]
                if numofupper(context[line_idx]) > 0: context[line_idx]=''
                sent += context[line_idx]



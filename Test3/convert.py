import jieba
import requests
from bs4 import BeautifulSoup
import re

def get_resource(url):
    # headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    #            "AppleWebKit/537.36 (KHTML, like Gecko)"
    #            "Chrome/63.0.3239.132 Safari/537.36"}
    headers = {
                'User-Agent': 'Googlebot'
    }           
    return requests.get(url, headers=headers,allow_redirects=True )

def parse_html(r):
    if r.status_code == 200:
        r.encoding = "utf8"
        soup = BeautifulSoup(r.text, "html.parser")        
    else:
        print("HTTP請求錯誤...")
        soup = None
    return soup 

def word_process():
    url='https://phabricator.wikimedia.org/source/mediawiki/browse/master/languages/data/ZhConversion.php'
    soup=parse_html(get_resource(url))
    words = soup.find_all('td',class_='phabricator-source-code')
    all_word = [word.text for word in words]
    all_word = all_word[14:-2]

    pattern = "'(.*)' => '(.*)'"
    chinese_dic=dict()
    for word in all_word:
        r = re.search(pattern,word)
        if r is not None:
            r1 = r.group(1).strip()
            r2 = r.group(2).strip()
            new = {r1:r2}
            chinese_dic.update(new)
    return chinese_dic

def chinese_convert(sentence,chinese_dic):
    cut_word=jieba.cut(sentence,HMM=True)
    words = [word for word in cut_word]
    convert_sentence=[]
    for word in words:
        if chinese_dic.get(word) is None:
            if len(word) > 1:
                for letter in word:
                    if chinese_dic.get(letter) is None:
                        convert_sentence.append(letter)
                    else:
                        convert_sentence.append(chinese_dic.get(letter))
            else:
                convert_sentence.append(word)
        else:  
            convert_sentence.append(chinese_dic.get(word))
    output=''.join(convert_sentence)
    return output
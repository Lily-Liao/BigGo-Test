import jieba
import requests
from bs4 import BeautifulSoup
import re

#取得url相關內容與狀態
def get_resource(url):
    headers = {
                'User-Agent': 'Googlebot'
    }

    return requests.get(url, headers=headers)

def parse_html(r):
    #檢查HTTP回應碼是否為200(200表示內容取得成功)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")        
    else:
        print("HTTP請求錯誤...")
        soup = None
    return soup 

#根據網頁的內容將其處理成字典，好方便後續轉換查詢
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
        new = {}
        if r is not None:
            r1 = r.group(1).strip()
            r2 = r.group(2).strip()
            new = {r1:r2}
            chinese_dic.update(new)
    return chinese_dic

#先將句子用jieba斷詞，再將斷詞透過自己編寫的字典做查詢
def chinese_convert(sentence,chinese_dic):
    cut_word=jieba.cut(sentence,HMM=True)
    words = [word for word in cut_word]
    convert_sentence=[]

    for word in words:
        convert_sentence.append(''.join([letter if chinese_dic.get(letter) is None else chinese_dic.get(letter) for letter in word]) if chinese_dic.get(word) is None and len(word) > 1 
        else word if chinese_dic.get(word) is None and len(word)==1 else chinese_dic.get(word))

    #下段程式碼與上面程式碼意思一樣
    # for word in words:
    #     if chinese_dic.get(word) is None and len(word) > 1:
    #         sentence=[letter if chinese_dic.get(letter) is None else chinese_dic.get(letter) for letter in word]
    #         convert_sentence.append(''.join(sentence))
                
    #     elif chinese_dic.get(word) is None and len(word)==1:
    #         convert_sentence.append(word)
    #     else:  
    #         convert_sentence.append(chinese_dic.get(word))
       
    output=''.join(convert_sentence)
    return output


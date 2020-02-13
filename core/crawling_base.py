import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
import re
import string
import pprint
import json
import time
from urllib.request import urlopen
from collections import defaultdict

class CrawlingBase(object):
    def __init__(self,url="https://biz.chosun.com",json_save_dir='crawling_data'):
        self.df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        self.company_object = self.df['회사명']
        self.company_list = list(self.company_object)
        self.company_dict = defaultdict(list)
        self.url = url
        self.html = urlopen(url)
        self.bsObject = BeautifulSoup(self.html, "html.parser")
        self.save_dir=json_save_dir

    def preprocess_word(self,x):
        m = x.replace('%', 'per')
        m = re.sub(r'(?:\b[0-9a-zA-Zㄱ-ㅎㅏ-ㅣ]\b|[?!\W]+)\s*', ' ', m).strip()
        m = re.sub('per', '%', m)
        m = " ".join(m.split())
        return m

    def get_string_from_chosun(self):
        text_list = []
        for i, meta in enumerate(self.bsObject.find_all("a")):
            text_list.append(meta.get_text())
        return text_list

    def add_company_info_from(self,s_list, verbose=True):
        for s in s_list:
            processed_words = []
            for word in s.split(' '):
                new_word = self.preprocess_word(word)
                if new_word in ["속보", "전체보기"]:
                    continue
                elif new_word and new_word != '':
                    processed_words.append(new_word)
            if processed_words and verbose: print('*' * 20);print(processed_words)
            for word in processed_words:
                if word in self.company_list:
                    self.company_dict[word].append(" ".join(processed_words))

    def save_json_newsdata(self):
        save_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        crawl_name = self.url.split("//")[-1].strip('/')
        file_name = f"{save_time}_{crawl_name}.json"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        save_path = os.path.join(self.save_dir, file_name)
        print(f"save_json_path : {save_path}")
        with open(save_path, "w") as json_file:
            json.dump(self.company_dict, json_file)

    def start_crawling(self):
        chosun_news = self.get_string_from_chosun()
        self.add_company_info_from(chosun_news)
        pprint.pprint(self.company_dict)
        self.save_json_newsdata()


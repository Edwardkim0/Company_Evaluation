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
from util.handling_json import print_from_json


class CrawlingBase(object):
    def __init__(self,url="https://biz.chosun.com",json_save_dir='crawling_data',name=None):
        self.df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        self.company_object = self.df['회사명']
        self.company_list = list(self.company_object)
        self.company_list_edit()
        self.company_dict = defaultdict(list)
        self.url = url
        self.html = urlopen(url)
        self.bsObject = BeautifulSoup(self.html, "html.parser")
        self.save_dir=json_save_dir
        self.name = name

    def company_list_edit(self):
        added_list = ["삼성","현대","SK","두산그룹","삼성그룹","현대그룹","LG가전","LGD","SDC","SDS","현대차","기아차","삼성차","현대자동차그룹"]
        self.company_list += added_list

    def preprocess_word(self,x):
        m = x.replace('%', 'per')
        m = re.sub(r'(?:\b[0-9a-zA-Zㄱ-ㅎㅏ-ㅣ]\b|[?!\W]+)\s*', ' ', m).strip()
        m = re.sub('per', '%', m)
        m = " ".join(m.split())
        return m

    def get_string_from(self):
        text_list = []
        for i, meta in enumerate(self.bsObject.find_all("a")):
            text_list.append(meta.get_text())
        for i, meta in enumerate(self.bsObject.find_all("p")):
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

    def save_json_newsdata(self,check_save):
        save_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if self.name != None:
            crawl_name = f"{self.name}_" + self.url.split("/")[2]
        file_name = f"{save_time}_{crawl_name}.json"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.save_path = os.path.join(self.save_dir, file_name)
        print(f"save_json_path : {self.save_path}")
        with open(self.save_path, "w",encoding='utf-8') as json_file:
            json.dump(self.company_dict, json_file,indent=4,ensure_ascii=False)
        if check_save:
            print_from_json(self.save_path)

    def post_process(self):
        company_keys = list(self.company_dict.keys())
        for company in company_keys:
            # list내 중복된 요소 제거
            self.company_dict[company] = list(set(self.company_dict[company]))
            # "한국경제" : ["한국경제"] 이런 요소들 제거
            self.company_dict[company] = [x for x in self.company_dict[company] if x!=company]
            # 비었으면 dict에서 제거
            if not self.company_dict[company]:
                del self.company_dict[company]
            elif company=="NAVER" and self.company_dict[company]==["NAVER Corp"]:
                del self.company_dict[company]



    def start_crawling(self,check_save=False):
        news = self.get_string_from()
        self.add_company_info_from(news )
        pprint.pprint(self.company_dict)
        self.post_process()
        self.save_json_newsdata(check_save=check_save)


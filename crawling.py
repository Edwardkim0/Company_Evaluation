import os
from selenium import webdriver
from core.crawling_base import CrawlingBase
from util.config import process_config


class CrwalBizChosun():
    def __init__(self,web_driver_path="C:\\project\\code\\ai_company_evaluatuion\\chromedriver_win32\\chromedriver.exe"):
        self.web_driver_path = web_driver_path
        self.driver = webdriver.Chrome(self.web_driver_path)
        self.driver.implicitly_wait(3)
        self.url = "https://biz.chosun.com"
        self.driver.get(self.url)
        self.num_pages = 150
        self.schedule_all_events()
        self.crawler = CrawlingBase(url=self.url,json_save_dir='crawling_data\\biz_chosun',name=None)

    def schedule_all_events(self):
        ## 클릭시 이벤트 dict
        self.xpath = {}
        self.xpath["industry"] = [];self.xpath["tech"] = [];self.xpath["finance"] = [];self.xpath["total"] = []

        # target_pages = list(range(2,13)) #[2,3,4,5,6,7,8,9,10,11,12]
        # self.xpath["industry"].append("""//*[@id="header"]/div[3]/div[2]/div[1]/ul[1]/li[1]/a""")
        # self.xpath["industry"].append("""//*[@id="list_left_aside_id"]/ul/li[2]/a""")
        # for i in range(self.num_pages+2):
        #     i %= len(target_pages)
        #     self.xpath["industry"].append(f"""//*[@id="contents"]/div/div[2]/div[2]/ul/li[{target_pages[i]}]/a""")
        # self.xpath["tech"].append("""//*[@id="header"]/div[2]/div[2]/div[1]/ul[1]/li[4]/a""")
        # self.xpath["tech"].append("""//*[@id="list_left_aside_id"]/ul/li[3]/a""")
        # self.xpath["tech"].append("""//*[@id="list_left_aside_id"]/ul/li[4]/a""")
        # self.xpath["finance"].append("""//*[@id="header"]/div[2]/div[2]/div[1]/ul[1]/li[5]/a""")
        # menu 버튼 클릭
        self.xpath["menu"] = """//*[@id="header"]/div[3]/div[2]/div[1]/div[1]/a"""
        # 전체 기사 보기
        self.xpath["total"].append("""//*[@id="header"]/div[3]/div[2]/div[1]/div[3]/ul/li[1]/a""")
        # 전체 기사 페이지
        target_pages = list(range(3,13)) #[3,4,5,6,7,8,9,10,11,12]
        for i in range(self.num_pages+2):
            i %= len(target_pages)
            self.xpath["total"].append(f"""//*[@id="contents"]/div/div[2]/div[2]/ul/li[{target_pages[i]}]/a""")

    def visit_and_crwal_url(self):
        # 메인
        self.crawler.start_crawling(check_save=True)
        # 산업
        # self.driver.find_element_by_xpath(self.xpath_industry["industry"]).click()
        # self.driver.implicitly_wait(3)
        # html = self.driver.page_source
        # self.crawler.set_bsojbect(html,"industry")
        # self.crawler.start_crawling(check_save=True)
        self.driver.find_element_by_xpath(self.xpath["menu"]).click()
        self.driver.implicitly_wait(3)
        ## 산업/ 기업
        for i,url in enumerate(self.xpath["total"]):
            self.driver.find_element_by_xpath(url).click()
            self.driver.implicitly_wait(5)
            html = self.driver.page_source
            self.crawler.set_bsojbect(html,name=f"fromNewest{self.num_pages}")
            self.crawler.start_crawling(check_save=False)
        ## crawling  결과 저장
        self.crawler.save_json_newsdata(check_save=True)

        ## 테크

#
# def crwal(url="https://biz.chosun.com",json_save_dir='crawling_data',name=None):
#     crwaler = CrawlingBase(url,json_save_dir,name)
#     crwaler.start_crawling(check_save=True)

if __name__ == '__main__':
    # config_path =  os.path.join("config","crawling_v0.1.json")
    # config_path =  os.path.join("config","crawling_v0.11.json")
    # config = process_config(config_path)
    crawler = CrwalBizChosun()
    crawler.visit_and_crwal_url()
    # for k in config:
    #     url = config[k]['url']
    #     crwal(url,name=k)
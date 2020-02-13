from core.crawling_base import CrawlingBase
from util.config import process_config
import os

def crwal(url="https://biz.chosun.com",json_save_dir='crawling_data'):
    chosun_crwaler = CrawlingBase(url,json_save_dir)
    chosun_crwaler.start_crawling()

if __name__ == '__main__':
    config_path =  os.path.join("config","crawling_v0.1.json")
    config = process_config(config_path)
    for k in config:
        url = config[k]['url']
        crwal(url)
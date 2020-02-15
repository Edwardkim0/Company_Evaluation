from core.crawling_base import CrawlingBase
from util.config import process_config
import os


def crwal(url="https://biz.chosun.com",json_save_dir='crawling_data',name=None):
    crwaler = CrawlingBase(url,json_save_dir,name)
    crwaler.start_crawling(check_save=True)

if __name__ == '__main__':
    # config_path =  os.path.join("config","crawling_v0.1.json")
    config_path =  os.path.join("config","crawling_v0.11.json")
    config = process_config(config_path)
    for k in config:
        url = config[k]['url']
        crwal(url,name=k)
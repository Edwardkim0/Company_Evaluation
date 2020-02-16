from urllib.request import urlopen
import pandas as pd
import json


class FinancialIndexCrawler:
    def __init__(self):
        self.key = 'APR28X9L09OHOZB0PFO1'

    def get_stat_code(self, request_count):
        url = "http://ecos.bok.or.kr/api/StatisticTableList/" + self.key + "/json/kr/1/" + str(request_count)
        result = urlopen(url)
        html = result.read()
        data = json.loads(html)
        data = data["StatisticTableList"]["row"]
        statistic_table_list = pd.DataFrame(data)
        stat_code = statistic_table_list['STAT_CODE'].values

        return stat_code

    def get_index_data(self, stat_code, writer, request_count, period, start_date, end_date):
        for code in stat_code:
            url = "http://ecos.bok.or.kr/api/StatisticSearch/" + self.key + "/json/kr/1/" + str(
                request_count) + "/" + code + "/" + period + "/" + start_date + "/" + end_date + "/?/?/?/"
            try:
                result = urlopen(url)
                html = result.read()
                data = json.loads(html)
                if 'StatisticSearch' in data:
                    data = data["StatisticSearch"]["row"]
                    index_data = pd.DataFrame(data)
                    if (index_data["ITEM_CODE1"] == "KOR").any():
                        index_data_kr = index_data[index_data["ITEM_CODE1"] == "KOR"]
                        index_data_kr.to_excel(writer, sheet_name=index_data_kr['STAT_NAME'][0])
                    else:
                        index_data.to_excel(writer, sheet_name=index_data['STAT_NAME'][0])
                else:
                    continue
            except Exception as e:
                print(e)
            writer.save()


def main():
    index_crawler = FinancialIndexCrawler()
    file_name = "경제지수.xlsx"
    writer = pd.ExcelWriter(file_name)

    stat_code = index_crawler.get_stat_code(10)
    index_crawler.get_index_data(stat_code, writer, 1000, "YY", "201501", "201805")


if __name__ == "__main__":
    main()

import FinanceDataReader as fdr
import pandas as pd
import re
import requests
import json
from pandas import json_normalize
import itertools


class FinancialStatementsCrawler:
    def __init__(self):
        self.url_template = 'http://companyinfo.stock.naver.com/v1/company/cF3002.aspx?' \
                            'cmp_cd={cmp_cd}&frq={frq}&rpt={rpt}&finGubun={finGubun}&frqTyp={frq}&cn=&encparam={encparam}'

    @staticmethod
    def get_encparam(url):
        html_text = requests.get(url).text
        encparam = re.findall("encparam: '(.*?)'", html_text)[0]

        return encparam

    def get_page(self, cmp_cd, frq, rpt, finGubun, encparam):
        url = self.url_template.format(cmp_cd=cmp_cd, frq=frq, rpt=rpt, finGubun=finGubun, frqTyp=frq,
                                       encparam=encparam)

        headers = {'Referer': url}
        web_page = json.loads(requests.get(url, headers=headers).text)

        return web_page

    @staticmethod
    def get_data_frame(web_page):
        date_str_list = []
        df = json_normalize(web_page, 'DATA')

        # DATA1~DATA6 컬럼 이름 바꾸기
        web_page_yymm = web_page['YYMM'][:6]
        for yymm in web_page_yymm:
            m = re.search('(\d{4}/\d{0,2}).*', yymm)
            date_str_list.append(m.group(1) if m else '')
        data_n_list = ['DATA' + str(i) for i in range(1, 7)]
        yymm_cols = zip(data_n_list, date_str_list)
        cols_map = dict(yymm_cols)
        df.rename(columns=cols_map, inplace=True)
        df['ACC_NM'] = df['ACC_NM'].str.strip().replace('[\.*\[\]]', '', regex=True)
        df.set_index(['ACCODE', 'ACC_NM'], inplace=True)
        df = df.iloc[:, 5:11]  # 날짜 컬럼만 추출
        df = df.T  # Transpose (컬럼, 인덱스 바꾸기)
        df.index = pd.to_datetime(df.index)
        df.index.name = '날짜'

        return df


def main():
    krx_list = fdr.StockListing('KRX')
    frq_list = [('0', '연간'), ('1', '분기')]
    rpt_list = [('0', '손익계산서'), ('1', '재무상태표'), ('2', '현금흐름표')]

    fs_crawler = FinancialStatementsCrawler()
    url = 'http://companyinfo.stock.naver.com/v1/company/c1030001.aspx?cmp_cd=005930'

    encparam = fs_crawler.get_encparam(url)
    for ix, row in krx_list[:3].iterrows():
        fn = "%s_%s_재무제표.xlsx" % (row['Symbol'], row['Name'])
        writer = pd.ExcelWriter(fn)
        for frq, rpt in itertools.product(frq_list, rpt_list):
            page = fs_crawler.get_page(cmp_cd=row['Symbol'], rpt=rpt[0], frq=frq[0], finGubun='IFRSL',
                                       encparam=encparam)
            df = fs_crawler.get_data_frame(page)
            df.to_excel(writer, sheet_name=rpt[1] + '_' + frq[1])
        writer.save()


if __name__ == "__main__":
    main()

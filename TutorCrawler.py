# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: gyy
import requests
from pyquery import PyQuery as pq
from alive_progress import alive_bar
import pandas as pd
import time
import traceback


class TutorCrawler:
    def __init__(self):
        self.url = 'https://yjszs.ecnu.edu.cn/system/sszszy_detail.asp?zydm=081200&zsnd=2022&yxdm=135'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
        }
        self.tutor_link = {}

    def get_link(self):
        response = requests.get(self.url, verify=False)
        if response:
            response.encoding = 'gb2312'
            doc = pq(response.text, parser='html')
            names = doc('#AutoNumber1 tr:nth-child(6) a').items()
            for i in names:
                self.tutor_link[i.text()] = i.attr('href')
        else:
            print('error')

    def get_tutor_info(self):
        result = []
        with alive_bar(len(self.tutor_link), force_tty=True) as bar:
            for key, value in self.tutor_link.items():
                try:
                    time.sleep(0.5)
                    response = requests.get(value, headers=self.headers)
                    if response:
                        response.encoding = 'utf8'
                        doc = pq(response.text, parser='html')
                        info_dict = {}
                        info_dict['姓名'] = doc('.news_title').text()
                        info_dict['职称'] = doc('.news_meta').text()
                        info_dict['学位'] = doc('div.maincon:nth-child(1) ul:nth-child(1) li:nth-child(3) span.txt').text()
                        info_dict['学历'] = doc('div.maincon:nth-child(1) ul:nth-child(1) li:nth-child(4) span.txt').text()
                        info_dict['毕业院校'] = doc('div.maincon:nth-child(1) ul:nth-child(1) li:nth-child(2) span.txt').text()
                        info_dict['联系电话'] = doc('div.maincon:nth-child(1) ul:nth-child(2) li:nth-child(1) span.txt').text()
                        info_dict['电子邮箱'] = doc('div.maincon:nth-child(1) ul:nth-child(2) li:nth-child(3) span.txt').text()
                        info_dict['办公地址'] = doc('div.maincon:nth-child(1) ul:nth-child(2) li:nth-child(4) span.txt').text()
                        info_dict['通讯地址'] = doc('div.maincon:nth-child(1) ul:nth-child(2) li:nth-child(5) span.txt').text()
                        info_dict['个人简介'] = doc('div.maincon:nth-child(1) div:nth-child(4) div.con').text().replace('\xa0','')
                        info_dict['研究方向'] = doc('div.maincon:nth-child(2) div.con').text().replace('\xa0','')
                        info_dict['开授课程'] = doc('div.maincon:nth-child(3) div.con').text().replace('\xa0','')
                        info_dict['科研项目'] = doc('div.maincon:nth-child(4) div.con').text().replace('\xa0','')
                        info_dict['学术成果'] = doc('div.maincon:nth-child(5) div.con').text().replace('\xa0','')
                        info_dict['荣誉奖励'] = doc('div.maincon:nth-child(6) div.con').text().replace('\xa0','')
                        info_dict['教育经历'] = doc('div.maincon:nth-child(1) div:nth-child(2) div.con').text().replace('\xa0','')
                        info_dict['工作经历'] = doc('div.maincon:nth-child(1) div:nth-child(3) div.con').text().replace('\xa0','')
                        info_dict['社会兼职'] = doc('div.maincon:nth-child(1) div:nth-child(5) div.con').text().replace('\xa0','')
                        # print(key)
                        result.append(info_dict)
                        bar()
                except Exception as e:
                    print(e)
                    continue
        return result

    def run(self):
        self.get_link()
        print(self.tutor_link)
        res = self.get_tutor_info()
        df = pd.DataFrame(res)
        df.to_excel('计专导师信息.xlsx', index=False)

tc = TutorCrawler()
tc.run()
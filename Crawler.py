# -*- coding: UTF-8 -*-
import json
import requests
import time
import urllib2, sys
import os

def main():
    crawler = Dcardcrawler(board="fitness",page=5)
    crawler.crawl()

class Dcardcrawler(object):
    root_url = "https://www.dcard.tw/_api/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    def __init__(self,board,page):
        self.board = board
        self.form_url = self.root_url+"forums/"+board+"/posts?"
        self.art_url = self.root_url+"posts/"
        self.page = page
    def get_req(self,url):
        """
        對url發出request以及解讀json response
        """
        req = urllib2.Request(url,headers=self.hdr)
        response = urllib2.urlopen(req)
        data2 = json.loads(response.read().decode('utf-8'))
        return data2

    def get_id(self,data2):
        """
        獲取文章id以便查詢內文
        """
        for d in data2:
            yield(self.art_url+str(d['id']))

    def output(self, filename, data):
        """
        輸出
        """
        with open("data/"+filename+".json", 'w') as ope:
            ope.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'))

    def crawl(self):
        final = []
        result = []
        comment = []
        allcomment = []
        m = self.get_req(self.form_url)
        for p_id in self.get_id(m):
            m2 = self.get_req(p_id)
            m3 = self.get_req(p_id+"/comments")
            for abc in m3:
                allcomment.append(abc)
            result.append(m2)
        for t in result:
            final.append(t)
        for i in range(self.page):
            pp_id = result[len(result)-1]['id']
            result = []
            m = self.get_req(self.form_url+"&before="+str(pp_id))
            for p_id in self.get_id(m):
                m2 = self.get_req(p_id)
                m3 = self.get_req(p_id+"/comments")
                result.append(m2)
                for abc in m3:
                    comment.append(abc)
                if len(m3)>29:
                    c_num=0
                    while (len(m3)==30):
                        c_num = c_num+30
                        m3 = self.get_req(p_id+"/comments?after="+str(c_num))
                        for abc in m3:
                            comment.append(abc)
            for t in result:
                final.append(t)
            for tt in comment:
                allcomment.append(tt)
            self.output(self.board,final)
            self.output(self.board+"_comments",allcomment)
            print("Already crawl "+str(i+1)+" pages")
            print("Already crawl "+str(len(final))+" articles")
            print("Already crawl "+str(len(allcomment))+" comments")

if __name__ == '__main__':
    main()

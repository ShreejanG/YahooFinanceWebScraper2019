# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:54:24 2019

@author: shree
"""

import bs4
import requests
from bs4 import BeautifulSoup
import time
from time import sleep
from lxml import html
import json
import argparse
from collections import OrderedDict
def praseTicker(ticker):
    summary_data = OrderedDict()
    r=requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
    soup=bs4.BeautifulSoup(r.text,"xml")

    price = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)' })[0].find('span').text
    summary_data.update({'Price' : price})

    left_table = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($c-fuji-grey-c)'})[0]
    left_data = left_table.find_all('td')

    a = 0
    while a < 8:
        summary_data.update({left_data[a].find('span').text: left_data[a+1].find('span').text})
        a += 2

    b = 8
    while b < 16:
        summary_data.update({left_data[b].text: left_data[b+1].text})
        b += 2

    right_table = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($c-fuji-grey-c)'})[0]
    right_data = right_table.find_all('td')

    i = 0
    while i < 10:
        summary_data.update({right_data[i].find('span').text: right_data[i+1].find('span').text})
        i += 2

    j = 10
    while j < 16:
        summary_data.update({right_data[j].text: right_data[j+1].text})
        j += 2

    return summary_data

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker',help = '')
    args = argparser.parse_args()
    ticker = args.ticker
    print ("Parsing %s"%(ticker))
    scraped_data = praseTicker(ticker)
    print ("Creating File")
    with open('%s.json'%(ticker),'w') as fp:
        json.dump(scraped_data,fp,indent = 4)

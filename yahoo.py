# -*- coding: utf-8 -*-
"""
Created on Wed July 7 06:00:00 2019

@author: Shreejan Gupta <sg3gj@virginia.edu> 
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

    # prase stock information from the left side of summary table 
    left_table = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($c-fuji-grey-c)'})[0]
    left_data = left_table.find_all('td')

    # update summary_data with prased data
    index = 0 
    while index < len(left_data): 
        first = left_data[index].find('span')
        second = left_data[index + 1].find('span')
        if (first is None or second is None): 
            summary_data.update({left_data[index].text: left_data[index+1].text})
        elif (first is not None and second is None): 
            summary_data.update({first.text: left_data[index+1].text})
        elif (first is None and second is not None): 
            summary_data.update({left_data[index].text: second.text})
        else: 
            summary_data.update({first.text: second.text})
        index += 2

    # prase stock information from the right side of summary table
    right_table = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($c-fuji-grey-c)'})[0]
    right_data = right_table.find_all('td')

    # update summary_data with prased data
    index = 0 
    while index < len(right_data): 
        first = right_data[index].find('span')
        second = right_data[index + 1].find('span')
        if (first is None or second is None): 
            summary_data.update({right_data[index].text: right_data[index+1].text})
        elif (first is not None and second is None): 
            summary_data.update({first.text: right_data[index+1].text})
        elif (first is None and second is not None): 
            summary_data.update({right_data[index].text: second.text})
        else: 
            summary_data.update({first.text: second.text})
        index += 2

    return summary_data

def filterStock(scraped_data): 

    retValue = True

    # Filter stocks with specified criterion
    for key, value in scraped_data.items(): 
        # print (key, value)
        if (key == 'PE Ratio (TTM)'): 
            if (value == 'N/A'): 
                retValue = False
            elif (float(value) > 20.00): 
                retValue = False

    return retValue

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker',help = '')
    args = argparser.parse_args()
    ticker = args.ticker
    print ("parsing information for %s"%(ticker))
    scraped_data = praseTicker(ticker)
    toExport = filterStock(scraped_data); 

    if (toExport): 
        print ("creating summary file for %s"%(ticker))
        with open('%s.json'%(ticker),'w') as fp:
            json.dump(scraped_data,fp,indent = 4)
    else: 
        print('stock does not meet specified criteria')
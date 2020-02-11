'''
This Script is able to retrieve a web site and convert data to shape file and Data Frame 
Alireza Naziri, Fornebu, Equinor, Jan 2020
'''

import pandas as pd 
import numpy as np
import os

#pip install BeautifulSoup4 (python3); pervious version is not supported anymore
from bs4 import BeautifulSoup

#Standard Lib
import urllib.request

#############
# Get Method
# myURL=r"http://www.infp.ro/index.php"
# myURL=r"http://www.infp.ro"
# req = urllib.request.Request(myURL)
# req.set_proxy('www-authproxy.statoil.net:80', 'http') 
# response = urllib.request.urlopen(req)
# html = response.read()

############
# Post Method
#Maximum pages and language
MaxPages=50
Lang='ro' # Lang='en' #Lang='ro'

res=[]
for page in range(1,MaxPages):

    url2=r"http://www.infp.ro/list.php"
    values={'pagina': str(page) , 'lang': Lang , 'zone' : 'ALL'}
    headers = {'User-Agent' 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url2,data.encode('utf-8'),headers)
    req.set_proxy('www-authproxy.statoil.net:80', 'http') 
    response = urllib.request.urlopen(req)
    html = response.read()

    ############
    soup = BeautifulSoup(html, 'html.parser')

    # items_tbody=soup.find_all('tbody')
    # len(items_tbody)

    items=soup.find_all(title="Detalii cutremur")
    #items[1]


    for item in items[1:]:
        # print(item)
        tt=item.find_all('td')
        # print(tt.text)
        ee=item.find_next('tr')
        tt2=ee.find_all('td')
        row2=[item2.text.strip() for item2 in tt2 if item2.text.strip()]
        row=[item2.text.strip() for item2 in tt if item2.text.strip()]
        rowtotal=row + row2
        if row:
            res.append(rowtotal)
           
cols=['col'+str(i) for i in range(0,len((rowtotal)))]
df=pd.DataFrame(res,columns=cols)        

df.to_csv(r'Romania_crawl_en.csv')
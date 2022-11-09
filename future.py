import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

def crawl(date):

    r = requests.get("https://www.taifex.com.tw/cht/3/futContractsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&queryDate={}%2F{}%2F{}&commodityId=".format(date.year,date.month,date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        print("順利拿到data日期", date)
    else:
        print("connection error")   
    try: 
        table = soup.find("table", class_="table_f") #要來找table 條件在後面
        trs = table.find_all("tr")#再下去找tr
    except AttributeError:
        print("no data for" ,date)
        return
    rows = trs[3:]#把第三個之後的tr放進去
    for row in rows:
        tds = row.find_all("td")
        ths = row.find_all("th")#需要找th的第二個 [1]

        cells = [td.text.strip() for td in tds]#strip裡面如果有空格要清掉
        th = [th.text.strip() for th in ths]
        
        if len(th) == 3:
            title=th[1]
            product = th[2]

            data = [product] + cells[0:]
            final = [title] + data #list相加         data不用[]為什麼啊？
            print(len(final))
        else:
            
            product = th[0]
            data = [product] + cells
            final = [title] + data #他會自己去外面找title？
            print(len(final))
date = datetime.today()
while True:
    crawl(date)
    date = date - timedelta(days=1)#進來回圈之後date會一直減少
    if date < datetime.today() - timedelta(days=2):#如果date減到小於 現在moment-5天的那個date 就停
        break
    
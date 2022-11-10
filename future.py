import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from pprint import pprint

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
    rows = trs[3:-4]#把第三個之後的tr放進去
    final = {} #不進回圈不然會被洗掉
    for row in rows:
        tds = row.find_all("td")
        ths = row.find_all("th")#需要找th的第二個 [1]

        cells = [td.text.strip() for td in tds]#strip裡面如果有空格要清掉
        th = [th.text.strip() for th in ths]
        
        if len(th) == 3:
            title=th[1]
            product = th[2]

            data = [product] + cells[0:]
            row_final = [title] + data #list相加         data不用[]為什麼啊？
            
        else:
            
            product = th[0]
            data = [product] + cells
            row_final = [title] + data #他會自己去外面找title？
        # print(final)
        converted = [int(f.replace(",","")) for f in row_final[2:]] #出來是數字的字串

        row_final = row_final[:2] + converted#商品 身份 +後續一串數字(12個)
        # print(final)

        headers =["商品名稱", "身份別" , "交易多方口數" ,"交易多方金額","交易空方口數","交易空方金額", "多空淨額口數","多空淨額金額","未平倉多方口數","未平倉多方金額","未平倉空方口數","未平倉空方金額","未平倉多空淨額口數","未平倉多空淨額金額"]
        #print(len(headers))
        
        #product（美國道瓊） -> who -> what(headers的內容)
        product = row_final[0]#美國道瓊那些
        who = row_final[1]#投信自營商
        contents = {headers[i]: row_final[i] for i in range(2,len(headers))} #len要加一？ 先處理後面數字以及名稱對應，之後再來處理開頭的（誰：外資）還有什麼交易：美國道瓊
        #三層字典 上面這個是最深層的字典 #range 2~14 相當於第三個到第13個
        # print(contents)
        if product not in final:
            final[product] = {who:contents}#final裡頭這個字典 就會創一個key:product value:一個字典 這個字典由key:who value:contents產生
        else:
            final[product][who] = contents#final字典裡面key:product 對應的value再輸入key為who 就會產生value:contents
        pprint(final)

date = datetime.today()
while True:
    crawl(date)
    date = date - timedelta(days=1)#進來回圈之後date會一直減少
    if date < datetime.today() - timedelta(days=2):#如果date減到小於 現在moment-5天的那個date 就停
        break
    
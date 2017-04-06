# -*- coding: utf-8 -*-
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def download_file(line_no, title, link):
    title = title.decode('utf8') if isinstance(title, str) else title
    headers = {'Cookie': "Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1489391132; ASP.NET_SessionId=0gletgjt5nvozeutahy1ehuf; CheckIPAuto=0; CheckIPDate=2017-04-05 02:26:27; 0gletgjt5nvozeutahy1ehufisIPlogin=1; User_User=%c9%cf%ba%a3%bd%bb%cd%a8%b4%f3%d1%a7; FWinCookie=1; Catalog_Search=(%ce%a8%d2%bb%b1%ea%d6%be%3d1970324845312945%2c1970324845317279%2c1970324845353893%2c1970324845353894%2c1970324845353895%2c1970324845353896%2c1970324845353897%2c1970324845353898%2c1970324845353899%2c1970324845353900%2c1970324845353901%2c1970324845353902%2c1970324845353903%2c1970324845353904%2c1970324845353905%2c1970324845353906%2c1970324845353907%2c1970324845362943%2c1970324845362944%2c1970324845362945)+and+%c8%ab%ce%c4%3d%27SLC(%2c)%27; CookieId=0gletgjt5nvozeutahy1ehuf; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1489390962,1491335503; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1491335503"}
    r = requests.get(link, headers=headers, stream=True)
    if r.status_code == 200:
        with open("Docs/23/"+str(line_no) + '-' + title.replace('/', '') + '.doc', 'wb') as f:
            for chunk in r:
                f.write(chunk)

if __name__ == '__main__':
    with open('out23.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if reader.line_num <= -1:
                continue
            print reader.line_num
            title = row[0]
            link = row[7]
            print title
            download_file(reader.line_num, title, link)

# -*- coding: utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

provinces = ('北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区')
pnames = ('北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆')


def get_page_data(pagenum):
    print pagenum
    url = "http://www.pkulaw.cn/doSearch.ashx"
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': "bdyh_record=123673871%2C123673870%2C119892646%2C119892655%2C119892678%2C121216334%2C120431644%2C119565612%2C; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1447430907; ASP.NET_SessionId=0anhtjahey4fwqylgqrhhdas; FWinCookie=1; CookieId=uij2mxt5sxiofucof0m0sdcg; CheckIPAuto=0; CheckIPDate=2015-11-16 17:11:23; Catalog_Search=(å¯ä¸æ å¿=119888118,119761915,119793883,119793884,119827639,119827640,119883158,119755921,119755922,119755920,119793993,119820593,119731229,119742202,119761738,119820557,119771388,119794012,119794079,119794157) and å¨æ='SLC(,)'"}
    payload = {
                'txtNumtiao': 23,
                'range': 'name',
                'Db': 'alftwotitle',
                'km': 'fnl',
                'tiao': 23,
                'htmgid': 199310,
                'subkm': 0,
                'orderby': 'fdate',
                'hidtrsWhere': 'DFFD208ED7A13C05581CA038F59CE0EB174717E2016AE7E4FD4EFA992D2535EA3A2A8F53CB4DB9E54B5B53EB81F06422C501C52688EE2BBA2924FF93A9431340978CEF3E90E606E5CD33CCA552EAF674A4E48FFA776523B2',
                '':'',
                'nomap':'',
                'clusterwhere': '((((km%253d%2527%2525fnl%2525%2527)%2520and%2520tiao%253d23)%2520and%2520htmgid%253d199310)%2520and%2520subkm%253d0)%2520and%2520fnl_anyou%253d00206',
                'aim_page': pagenum,
                'page_count': 15,
                'clust_db': 'alftwotitle',
                'menu_item': 'clink',
                'EncodingName': '',
                'time': 0.9583643651217888
               }

    response = requests.post(url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "lxml")
    items = soup.find_all('a', class_='main-lj_big')
    data = []
    if items:
        for item in items:
            node = item.find_next('tr')
            if node:
                court = node.find(attrs={'title': '审理法院'})
                num = node.find(attrs={'title': '案件字号'})
                date = node.find(attrs={'title': '审结日期'})

                if not court:
                    court = 'null'
                else:
                    court = court.text.strip()
                if not num:
                    num = 'null'
                else:
                    num = num.text.strip()
                if not date:
                    date = 'null'
                else:
                    date = date.text.strip()

                case_id = item.get('href').split('pfnl_')[1].split('.html')[0]
                download_link = 'http://www.pkulaw.cn/case/FullText/DownloadFile?library=pfnl&gid=' + case_id + '&type=doc'

                if '初字' in num:
                    rank = '初'
                elif '终字' in num:
                    rank = '终'
                else:
                    rank = '未知'

                province = '未知'
                city = '未知'
                for idx, p in enumerate(provinces):
                    if p in court:
                        province = pnames[idx]
                        rest = court.split(p)[1]
                        if '市' in rest:
                            city = rest.split('市')[0]
                        elif '区（县）'in rest:
                            city = rest.split('区（县）')[0]
                        elif '区' in rest:
                            city = rest.split('区')[0] + '区'
                        elif '县' in rest:
                            city = rest.split('县')[0] + '县'
                        elif '自治州' in rest:
                            city = rest.split('自治州')[0] + '自治州'
                        break

                data.append({'title': item.text,
                             'link': download_link,
                             'court': court,
                             'num': num,
                             'date': date,
                             'rank': rank,
                             'province': province,
                             'city': city
                             })
    return data

if __name__ == '__main__':
    res = []
    for i in range(15):
        res.extend(get_page_data(i))
    with open('out23.csv', 'wb') as out:
        csv_out = csv.writer(out)
        for row in res:
            row = [row['title'], row['num'], row['date'], row['court'], row['province'], row['city'], row['rank'], row['link']]
            row = [v.decode('utf8') if isinstance(v, str) else v for v in row]
            csv_out.writerow(row)


from app.utils import scheduler
from app import db
from app.models import ProvinceInfo, CityInfo
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def spider_common(url, Model):
    r1 = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
    )

    soup = BeautifulSoup(r1.text, 'html.parser')
    item_list = soup.find(name='div', attrs={'class': 'info'}).find('ul').find_all('li')
    for item in item_list:
        time = item.find(name='div', attrs={'class': 'time curr'})
        day = time.find('span').text
        year_month = list(time.children)[-1].strip()
        date_string = year_month + "-" + day
        date = datetime.strptime(date_string, "%Y-%m-%d")

        a = item.find('a')
        href = a['href'] if 'http' in a['href'] else "http://www.ccgp-sichuan.gov.cn"+a['href']
        title = a.find(name='div', attrs={'class': 'title'}).text

        pur_obj = Model.query.filter(Model.title == title).first()
        # if pur_obj:
        #     print('该条数据已经采集过:'+title)
        # else:
        if not pur_obj:
            purchase_info = Model()
            purchase_info.purchase_time = date
            purchase_info.title = title
            purchase_info.url = href
            db.session.add(purchase_info)
            db.session.commit()


def spider_province():
    with scheduler.app.app_context():
        url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&chnlCodes=8a817eb738e5e70c0138e62ab6430c0a&chnlNames=\u7701\u91C7\u8D2D\u516C\u544A&years=2018&title=\u8F6F\u4EF6&startTime=&endTime=&distin_like=510000&province=510000&city=&town=&provinceText=\u56DB\u5DDD\u7701&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&pageSize=10&searchResultForm=search_result_anhui.ftl"
        spider_common(url, ProvinceInfo)


def spider_city():
    with scheduler.app.app_context():
        url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&chnlCodes=8a817eb738e5e70c0138e65ad1a10e0a&chnlNames=\u5E02\u53BF\u7EA7\u91C7\u8D2D\u516C\u544A&years=2018&title=\u8F6F\u4EF6&startTime=&endTime=&distin_like=510000&province=510000&city=&town=&provinceText=\u56DB\u5DDD\u7701&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&pageSize=10&searchResultForm=search_result_anhui.ftl"
        spider_common(url, CityInfo)



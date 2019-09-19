from app.utils import scheduler
from app import db
from app.models import ProvinceInfo, CityInfo
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def spider_common(url, Model, page, name):
    print("开始爬取：" + name)
    for i in range(1, page+1):
        r1 = requests.get(
            url=url.format(i),
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
            if not pur_obj:
                if '软件' in title:
                    print('该公告标题和软件有关系:' + title)
                    purchase_info = Model()
                    purchase_info.purchase_time = date
                    purchase_info.title = title
                    purchase_info.url = href
                    db.session.add(purchase_info)
                    db.session.commit()
                    continue
                r2 = requests.get(url=href)
                r2.encoding = 'utf-8'
                soup = BeautifulSoup(r2.text, 'html.parser')
                content = soup.find(name='div', id='myPrintArea').text
                if '软件' in content:
                    print('该公告内容和软件有关系:'+title)
                    purchase_info = Model()
                    purchase_info.purchase_time = date
                    purchase_info.title = title
                    purchase_info.url = href
                    db.session.add(purchase_info)
                    db.session.commit()
    print("本次爬取结束："+name)


def spider_province():
    with scheduler.app.app_context():
        url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&rp=25&page={0}&moreType=provincebuyBulletinMore&channelCode=cggg"
        spider_common(url, ProvinceInfo, 20, 'spider_province')


def spider_city():
    with scheduler.app.app_context():
        url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&rp=25&page={0}&moreType=provincebuyBulletinMore&channelCode=shiji_cggg"
        spider_common(url, CityInfo, 100, 'spider_city')



# coding:utf-8

# 引入相关模块
import re
import json
import redis
import cfscrape
from bs4 import BeautifulSoup


def DB():
    pool = redis.ConnectionPool(host='10.10.10.200', port=6379, decode_responses=True, db=4)
    r = redis.Redis(connection_pool=pool)
    return r


# 获取采集信息的 token 钥匙
def Token():
    # # 第一步获取采集数据的门槛，分别拿到sid和session
    # # 实例化一个create_scraper对象
    # scraper = cfscrape.create_scraper()
    # # 请求报错，可以加上时延
    # # scraper = cfscrape.create_scraper(delay = 10)
    # # 获取网页源代码
    # url = "https://bscscan.com/token/0x12bb890508c125661e03b09ec06e404bc9289040"
    # response = scraper.get(
    #     url,
    #     proxies={
    #         "https": "https://pmgr-customer-hl_e32a409a.zproxy.lum-superproxy.io:24000",
    #         # "https": "https://127.0.0.1:24000",
    #     }
    # )
    # cookies = response.cookies
    # # 从网页html/js中，用正则匹配替换出 sid
    # sidArr = re.findall(r"var sid = \'(.+?)\';\r\n", str(response.content, "utf-8"))
    # # 获取 ASP.NET_SessionId
    # session = "ASP.NET_SessionId=" + cookies['ASP.NET_SessionId']
    # sid = "sid=" + sidArr[0]
    # # 第一步获取采集数据的门槛，分别拿到sid和session
    # return [session, sid]
    return ['ASP.NET_SessionId=1jmk0z3gjx1gmlk4rymwh2g3', 'sid=020b9b8e05d3e82858a38b0a26dc0612']


# 获取列表数据
def getList(p):
    scraper = cfscrape.create_scraper()
    Info = Token()
    # print(Info)
    session = Info[0]
    sid = Info[1]
    # 第二步真正获取数据
    listUrl = "https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x12bb890508c125661e03b09ec06e404bc9289040&a=&" + sid + "&p=" + p
    print(listUrl)
    listRes = scraper.get(
        listUrl,
        headers={
            "Cookie": session
        }
        # , proxies={
        #     # "https": "https://pmgr-customer-hl_e32a409a.zproxy.lum-superproxy.io:24000",
        #     # "https": "http://lum-customer-hl_e32a409a-zone-isp:l4z2hyzxackl@zproxy.lum-superproxy.io:22225",
        # }
    )
    return str(listRes.content, "utf-8")


# 启动采集
def Start(page):
    print("第" + page + "页")
    listRes = getList(page)
    tbody = BeautifulSoup(listRes, 'lxml').findAll("tbody")
    if len(tbody) > 0:
        trArray = []
        for tr in tbody[0].findAll("tr"):
            td = tr.findAll("td")
            tdItem = {
                "TxnHash": td[0].find("a").get_text(),
                "Method": td[1].find("span").get_text(),
                "showDate": td[2].find("span").get_text(),
                "showAge": td[3].find("span").get_text(),
                "From": td[4].find("a").get_text(),
                "direction": td[5].find("i")["class"],
                "To": td[6].find("a").get_text(),
                "Quantity": td[7].get_text(),
                "End": td[8].get_text(),
            }
            trArray.append(tdItem)
        rJson = json.dumps(trArray)
        ok = DB().lpush("list", rJson)
        print(ok)
        print(rJson)
        return rJson
    else:
        print(tbody)
        return False

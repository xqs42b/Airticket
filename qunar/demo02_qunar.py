# coding=utf-8

import requests
import time
import json
import string
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ss = requests.session()

url1 = 'https://flight.qunar.com/'
headers1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
rp1 = ss.get(url1, headers=headers1)

def get_city_code(city_name):
    livesearch_url = 'https://www.qunar.com/suggest/livesearch2.jsp'
    headers2 = {
        'Referer': 'https://flight.qunar.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    params2 = {
        'lang': 'zh',
        'q': city_name,
        'sa': 'true',
        'ver': '1',
        'callback': '',
        '_': ''
    }
    rp2 = ss.get(livesearch_url, headers=headers2, params=params2)
    print rp2.text

city1_name = '广州'
city1_code = get_city_code(city1_name)
city2_name = '北京'
city2_code = get_city_code(city2_name)

url3 = 'https://flight.qunar.com/twell/flight/Search.jsp'
params3 = {
    'from': 'flight_dom_search',
    'searchType': 'OnewayFlight',
    'fromCity': '广州(CAN)',
    'toCity': '北京(BJS)',
    'fromDate': '2019-02-23',
    'toDate': '2019-02-25',
    'ishttps': '1'
}
headers3 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://flight.qunar.com/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
rp3 = ss.get(url3, headers=headers3, params=params3)
rp3_url = rp3.url
print rp3_url


def get_random_str(str_num):
    ''' 获取随机字符串 '''
    if not str_num:
        return ''
    all_strs = string.ascii_lowercase + string.digits
    strs_list = random.sample(all_strs, str_num)
    new_strs = ''
    new_strs = new_strs.join(strs_list)
    return new_strs


t1 = time.time()
t2 = time.time() + 1000
url5 = 'https://log.flight.qunar.com/l'
params5 = {
    'r': 'domestic_3w_list_api',
    'et': t1,
    'at': t2,
    'p': 'oneway_list'
}
headers5 = {
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://flight.qunar.com',
    'Referer': 'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E5%B9%BF%E5%B7%9E&searchArrivalAirport=%E5%8C%97%E4%BA%AC&searchDepartureTime=2019-02-24&searchArrivalTime=2019-02-27&nextNDays=0&startSearch=true&fromCode=CAN&toCode=BJS&from=flight_dom_search&lowestPrice=null',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
rp5 = ss.post(url5, headers=headers5, params=params5)
print rp5.status_code

url4 = 'https://flight.qunar.com/touch/api/domestic/wbdflightlist'
headers4 = {
    get_random_str(6): get_random_str(32),
    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    get_random_str(6): get_random_str(32),
    'content-type': 'application/x-www-form-urlencoded',
    'referer': rp3_url,
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'w': '0',
    'x-requested-with': 'XMLHttpRequest'
}
params4 = {
    'departureCity': city1_name,
    'arrivalCity': city2_name,
    'departureDate': '2019-02-23',
    'ex_track': '',
    '__m__': get_random_str(32),
    'sort': '',
    '_v': '1'
}

rp4 = ss.get(url4, headers=headers4, params=params4)
print json.loads(rp4.text)['msg']

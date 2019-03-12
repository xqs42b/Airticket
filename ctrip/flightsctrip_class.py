# coding=utf-8

import requests
import json
import time
import traceback

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class FlightsCtrip(object):
    ''' 获取携程机票数据 '''

    def __init__(self):
        self.init_url = 'https://flights.ctrip.com/'
        self.city_data_url = 'https://flights.ctrip.com/domestic/poi'
        self.ss = requests.session()
        self.is_init_page = self.load_init_page()

    def load_init_page(self):
        ''' 请求初始页面 '''
        headers = self.make_headers()
        rp = self.back_reponse(self.init_url, headers=headers)
        if not rp:
            return False
        return True

    def get_city_data(self, city_name):
        ''' 获取城市信息 '''
        params = {
            'channel': '1',
            'mode': '1',
            'f': '2',
            'key': city_name,
            'v': '0'           
        }
        headers = self.make_headers()
        headers['accept'] = '*/*'
        headers['referer'] = 'https://flights.ctrip.com/'
        rp = self.back_reponse(self.city_data_url, headers=headers, params=params)
        if not rp:
            return None
        city_text = rp.text
        equal_index = city_text.find('=')
        if equal_index == -1:
            return None
        city_json = city_text[equal_index+1:]
        city_data = json.loads(city_json)
        return city_data 
    
    def get_city_code(self, city_name):
        ''' 获取城市的code '''
        if not city_name:
            return None
        city_data = self.get_city_data(city_name)
        if not city_data:
            return None
        Datas = city_data.get('Data', '') 
        if (not Datas) and isinstance(Datas, list):
            return None
        Data = Datas[0]
        city_code = Data.get('Code', '')
        return city_code

    def load_flight_page(self, city1_code, city2_code, url):
        ''' 加载机票产品页面 '''
        date_str = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24))
        if (not city1_code) and (not city2_code) and (not url):
            return None 
        headers = self.make_headers()
        headers['cache-control'] = 'max-age=0'
        headers['content-type'] = 'application/x-www-form-urlencoded'
        headers['origin'] = 'https://flights.ctrip.com'
        headers['referer'] = 'https://flights.ctrip.com/'

        form_data = {
            'DCity1': city1_code, 
            'ACity1': city2_code, 
            'DDate1': date_str, 
            'DCity2': '',
            'ACity2': '',
            'DDate2': '',
            'TransitCity': '',
            'DCityName1': '(unable to decode value)',
            'DCityName2': '',
            'ACityName1': '(unable to decode value)',
            'ACityName2': '',
            'IsSingleSearchPost': 'T',
            'SEOAirlineDibitCode': '',
            'FlightSearchType': 'S',
            'ClassType': ''
        }
        rp = self.back_reponse(url, headers=headers, form_data=form_data, is_get=False)
        if not rp:
            return False
        return True
        
    def get_fligth_product(self, city1_name, city2_name):
        ''' 获取机票信息 '''
        #  判断是否加载首页
        is_init_page = self.is_init_page
        if not self.is_init_page:
            if not self.load_init_page():
                return None

        date_str = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24))        
        city1_code = self.get_city_code(city1_name)
        city2_code = self.get_city_code(city2_name)
        flight_page_url = 'https://flights.ctrip.com/booking/%s-%s-day-1.html?ddate1=%s'%(city1_code, city2_code, date_str)
        if not self.load_flight_page(city1_code, city2_code, flight_page_url):
            return None
        headers = self.make_headers()
        headers['accept'] = '*/*'
        headers['content-type'] = 'application/json'
        headers['origin'] = 'https://flights.ctrip.com'
        headers['referer'] = flight_page_url 
        
        products_url = 'https://flights.ctrip.com/itinerary/api/12808/products'
        payload_data = {
            "flightWay":"Oneway",
            "classType":"ALL",
            "hasChild":False,
            "hasBaby":False,
            "searchIndex":1,
            "airportParams":[{
                "dcity":city1_code,
                "acity":city2_code,
                "dcityname":city1_name,
                "acityname":city2_name,
                "date":date_str,
                "dcityid":32,
                "acityid":1
                }]
            }
        rp = self.back_reponse(products_url, headers=headers, json_data=payload_data, is_get=False)
        if not rp:
            return None
        try:
            products_data = json.loads(rp.text)
            route_data = self.get_select_flight_data(products_data)
            print json.dumps(route_data)
        except:
            return None
        return products_data 

    def get_select_flight_data(self, original_data):
        ''' 筛选飞机票数据 '''

        route_data = []
        # routeType: 路线类型; Flight(飞机直达), FlightTrain(飞机转火车)
        Flight = 'Flight'
        FlightTrain = 'FlightTrain'
        route_kw_data = 'data'
        routeList = 'routeList'
        routeType = 'routeType'
        legs = 'legs'
        legs_flight = 'flight'
        flight_keyword_list = ['flightNumber', 'airlineName', 'craftTypeCode', 'craftTypeName',\
            'craftTypeKindDisplayName', 'departureDate', 'arrivalDate', 'punctualityRate',\
            'departureAirportInfo', 'arrivalAirportInfo']
        departureAirportInfo = 'departureAirportInfo'
        arrivalAirportInfo = 'arrivalAirportInfo'
        cityName = 'cityName'
        airportName = 'airportName'
        terminal = 'terminal'
        name = 'name'
        departure_cityname = 'departureCityName'
        departure_terminalname = 'departureTerminalName'
        arrival_cityname = 'arrivalCityName'
        arrival_terminalname = 'arrivalTerminalName'
        cabins = 'cabins'
        cabins_price = 'price'
        cabins_rate = 'rate'
        cabinClass = 'cabinClass'
        '''
        cabinClass: Y(经济舱)
        cabinClass: C(公务舱)
        cabinClass: F(头等舱)
        '''
        seatecount = 'seatCount'
        childPolicy = 'childPolicy'
        babyPolicy = 'babyPolicy'
        additionalProductGroups = 'additionalProductGroups'
        additional_product = 'products'

        try:
            routeList_data = original_data[route_kw_data][routeList]
            print 'route_num:', len(routeList_data)
            for route in routeList_data:
                air_data = {}
                flight = {} 
                new_cabins_list = []
                if route[routeType] == Flight:
                    legs0_data = route[legs][0]
                    air_data[routeType] = Flight
                    legs_flight_data = legs0_data[legs_flight]
                    for f_kw in flight_keyword_list:
                        if f_kw == departureAirportInfo:
                            departure_data = legs_flight_data[f_kw]
                            flight[departure_cityname] = departure_data[airportName]
                            flight[departure_terminalname] = departure_data[terminal][name]
                            continue
                        if f_kw == arrivalAirportInfo:
                            arrival_data = legs_flight_data[f_kw]
                            flight[arrival_cityname] = arrival_data[airportName]
                            flight[arrival_terminalname] = arrival_data[terminal][name]
                            continue
                        flight[f_kw] = legs_flight_data[f_kw]

                    cabins_list = legs0_data[cabins]
                    for cabin in cabins_list:
                        price_dict = {}
                        price_dict[cabins_price] = cabin[cabins_price][cabins_price]
                        price_dict[cabins_rate] = cabin[cabins_price][cabins_rate]
                        price_dict[seatecount] = cabin[seatecount]
                        price_dict[cabinClass] = cabin[cabinClass]
                        childPolicy_data = cabin.get(childPolicy, '')
                        babyPolicy_data = cabin.get(babyPolicy, '')
                        if not childPolicy_data:
                            price_dict[childPolicy + cabins_price] = childPolicy_data
                        else:
                            price_dict[childPolicy + cabins_price] = childPolicy_data[cabins_price]
                        
                        if not babyPolicy_data:
                            price_dict[babyPolicy + cabins_price] = babyPolicy_data 
                        else:
                            price_dict[babyPolicy + cabins_price] = babyPolicy_data[cabins_price]

                        new_cabins_list.append(price_dict)

                    flight[cabins] = new_cabins_list
                    air_data[legs_flight] = flight
                if routeType == FlightTrain:
                    air_data[routeType] = FlightTrain
                    pass
                route_data.append(air_data)
            return route_data 
        except:
            traceback.print_exc()
            return route_data 

    def make_headers(self):
        ''' 制作请求头 '''
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu\
                Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36'            
        }
        return headers

    def back_reponse(self, url, headers, params=None, form_data=None, json_data=None, is_get=True):
        ''' 操作requests模块 '''
        try:
            if is_get:
                rp = self.ss.get(url, headers=headers, params=params)
            else:
                rp = self.ss.post(url, headers=headers, params=params, data=form_data, json=json_data)
            if rp.status_code == 200:
                return rp 
            else:
                None
        except:
            return None
        
if __name__ == '__main__':
    fc = FlightsCtrip()
    city1_name = u'广州'
    city2_name = u'成都'
    fc.get_fligth_product(city1_name, city2_name)

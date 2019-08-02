# coding=utf-8

import time
import ele_utils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from citys import all_city_list


class FlightCtrip(object):
    """携程机票"""

    def __init__(self):
        self.driver = self.back_driver()

    @staticmethod
    def back_driver():
        """返回浏览器对象"""
        num = 0
        driver = None
        while 1:
            if num > 5:
                return None
            try:
                option = webdriver.ChromeOptions()
                # 隐藏头信息
                # option.add_argument('--headless')
                # option.add_argument('User-Agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
                #     Chrome/75.0.3770.142 Safari/537.36"')
                # 关闭开发者模式
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                driver = webdriver.Chrome(chrome_options=option)
                driver.set_window_size(1366, 768)
                # driver.maximize_window()
            except Exception as error:
                num += 1
                print("back_driver_error:", error)
                continue
            break

        init_url = 'https://flights.ctrip.com'
        try:
            driver.get(init_url)
        except Exception as error:
            print("back_driver_error:", error)
        return driver

    def choose_fighttype(self, flighttype="RoundTrip"):
        """选择航班类型"""
        if flighttype == 'Oneway':
            flighttype_xpath = '//input[@data-ubt="SingleTrip"]'
        else:
            flighttype_xpath = '//input[@data-ubt="RoundTrip"]'

        flighttype_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            flighttype_xpath
        )
        if not flighttype_ele:
            return False
        flighttype_ele.click()
        return True

    def send_from_city(self, city_name):
        """输入出发城市"""
        from_city_xpath = '//input[@id="DepartCity1TextBox"]'
        from_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            from_city_xpath
        )
        if not from_city_ele:
            return False
        from_city_ele.send_keys(city_name)
        return True

    def send_to_city(self, city_name):
        """输入到达城市"""
        to_city_xpath = '//input[@id="ArriveCity1TextBox"]'
        to_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            to_city_xpath
        )
        if not to_city_ele:
            return False
        to_city_ele.send_keys(city_name)
        return True

    def send_date1(self, cur_date):
        """输入出发日期"""
        date_xpath = '//input[@id="DepartDate1TextBox"]'
        date_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            date_xpath
        )
        if not date_ele:
            return False
        date_ele.send_keys(cur_date)
        return True

    def send_date2(self, cur_date):
        """输入到达日期"""
        return_date_xpath = '//input[@id="ReturnDepartDate1TextBox"]'
        return_date_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            return_date_xpath
        )
        if not return_date_ele:
            return False
        return_date_ele.send_keys(cur_date)
        return return_date_ele

    def search_btn(self):
        """搜索机票数据"""
        search_xpath = '//input[@id="search_btn"]'
        search_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            search_xpath
        )
        if not search_ele:
            return False
        search_ele.click()
        return True

    def itinerary_send_from_city(self, icity_name):
        """在行程页面中输入出发城市"""
        itinerary_from_city_xpath = '//input[@id="dcity0"]'
        itinerary_from_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            itinerary_from_city_xpath
        )
        if not itinerary_from_city_ele:
            return False
        itinerary_from_city_ele.click()
        while 1:
            itinerary_from_city_ele.clear()
            itinerary_from_city_ele.send_keys(icity_name)
            time.sleep(1)
            itinerary_from_city_ele.send_keys(Keys.ENTER)
            send_city_name = itinerary_from_city_ele.get_attribute('value')
            # print(send_city_name)
            if icity_name not in send_city_name:
                continue
            break
        return True

    def itinerary_send_to_city(self, icity_name):
        """在行程页面中输入到达城市"""
        itinerary_to_city_xpath = '//input[@id="acity0"]'
        itinerary_to_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            itinerary_to_city_xpath
        )
        if not itinerary_to_city_ele:
            return False
        itinerary_to_city_ele.click()
        itinerary_to_city_ele.clear()
        itinerary_to_city_ele.send_keys(icity_name)
        time.sleep(1)
        itinerary_to_city_ele.send_keys(Keys.ENTER)
        return True

    def itinerary_research(self):
        """在行程页面中搜索"""
        research_xpath = '//a[@data-ubt="c_search_research"]'
        research_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            research_xpath
        )
        if not research_ele:
            return False
        research_ele.click()
        return True

    def get_flight_data(self, from_city, to_city):
        """获取最低机票数据"""
        ctmp_data = {
            'flight': {
                'arrivalAirportInfo': {'cityName': to_city, 'airportName': ''},
                'departureAirportInfo': {'cityName': from_city, 'airportName': ''},
                'airlineName': '',
                'departureDate': '',
                'arrivalDate': '',
                'flightNumber': ''
            },
            'lowestPrice': 0,
        }
        # 航线名称
        airline_name_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/div/div/\
            div/span/span/strong'
        airline_name_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            airline_name_xpath
        )
        if airline_name_ele:
            ctmp_data['flight']['airlineName'] = airline_name_ele.text

        flight_number_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/\
            div/div/div/span/span/span'
        flight_number_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            flight_number_xpath
        )
        if airline_name_ele:
            ctmp_data['flight']['flightNumber'] = flight_number_ele.text

        departure_date_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/div[2]/\
            div/strong'
        departure_date_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            departure_date_xpath
        )
        if departure_date_ele:
            ctmp_data['flight']['departureDate'] = departure_date_ele.text

        departure_airport_name_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/\
            div/div[2]/div[2]'
        departure_airport_name_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            departure_airport_name_xpath
        )
        if departure_airport_name_ele:
            ctmp_data['flight']['departureAirportInfo']['airportName'] = departure_airport_name_ele.text

        arrival_date_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/div[4]/\
            div/strong'
        arrival_date_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            arrival_date_xpath
        )
        if arrival_date_ele:
            ctmp_data['arrivalDate'] = arrival_date_ele.text

        arrival_airport_name_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/\
            div[4]/div[2]'
        arrival_airport_name_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            arrival_airport_name_xpath
        )
        if arrival_airport_name_ele:
            ctmp_data['flight']['arrivalAirportInfo']['airportName'] = arrival_airport_name_ele.text

        lowest_price_xpath = '//div[@class="search_box search_box_tag search_box_light Label_Flight"][1]/div/div[7]/\
            div/span'
        lowest_price_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            lowest_price_xpath
        )
        if lowest_price_ele:
            ctmp_data['lowestPrice'] = int(lowest_price_ele.text[1:])
        return ctmp_data

    def close(self):
        """关闭页面"""
        self.driver.close()

    def main(self, province, to_city, tdate1, tdate2, tflighttype="RoundTrip"):
        """入口"""
        city_list = all_city_list[province]
        data_list = list()
        if not self.choose_fighttype(tflighttype):
            return data_list
        from_city0 = city_list[0]
        if not self.send_from_city(from_city0):
            return data_list
        if not self.send_to_city(to_city):
            return data_list
        if not self.send_date1(tdate1):
            return data_list
        if not self.send_date2(tdate2):
            return data_list
        if not self.choose_fighttype(tflighttype):
            return data_list
        if not self.search_btn():
            return data_list
        flight_data0 = self.get_flight_data(from_city0, to_city)
        data_list.append(flight_data0)
        if len(city_list) < 2:
            return data_list
        for i in range(1, len(city_list)):
            cur_from_city = city_list[i]
            if not self.itinerary_send_from_city(cur_from_city):
                return False
            time.sleep(2)
            if not self.itinerary_send_to_city(to_city):
                return False
            time.sleep(2)
            if not self.itinerary_research():
                return False
            flight_data = self.get_flight_data(cur_from_city, to_city)
            data_list.append(flight_data)
        # 按价格排序由低到高
        data_list = sorted(data_list, key=lambda x: x['lowestPrice'])
        return data_list


if __name__ == '__main__':
    fc = FlightCtrip()
    # cur_province = 'shanghai'
    cur_province = 'guangdong'
    cur_to_city = u'北京'
    date1 = '2019-08-06'
    date2 = '2019-08-09'
    print(fc.main(cur_province, cur_to_city, date1, date2))
    fc.close()

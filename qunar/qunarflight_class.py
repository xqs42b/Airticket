# coding=utf-8

import time
import json
import traceback
import ele_utils
import re
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class QunarFlight(object):
    ''' 去哪儿网机票数据查询 '''

    def __init__(self):
        self.driver = self.load_init_page()

    def load_init_page(self):
        ''' 加载初始页面 '''
        url = 'https://flight.qunar.com/'
        # driver = webdriver.Firefox()
        option = webdriver.ChromeOptions()
        option.add_experimental_option(
            'excludeSwitches',
            ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=option)
        driver.maximize_window()
        init_num = 0
        while True:
            if init_num > 6:
                # print '网络有问题， 请稍候请求！'
                return None
            try:
                driver.get(url)
            except:
                init_num += 1
                time.sleep(1)
                driver.refresh()
                continue
            return driver

    def find_event(self, cityName1, cityName2, date1=None, date2=None):
        ''' 入口 '''
        if not self.operate_city_date(cityName1, cityName2, date1, date2):
            return None
        self.get_flight_data()

    def get_flight_data(self):
        ''' 获取飞机票数据 '''
        self.click_direct_flight_checkbox()

        flight_company_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[1]/span'
        flight_number_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[2]/span[1]'
        flight_type_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[2]/span[2]'
        set_out_date_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-lf"]/h2'
        set_out_airport_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-lf"]/p/span[1]'
        set_out_railway_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-lf"]/p/span[2]'
        time_cost_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-ct"]'
        arrival_date_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-rt"]/h2'
        arrival_airport_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-rt"]/p/span[1]'
        arrival_railway_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-rt"]/p/span[2]'
        discount_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div[2]/div/span'
        price_html_i_xpath = '//div[@id="content"]/div/div[3]/div[4]/div/div/div/div/div[2]/p/span/span/span/em/b[1]'
        em_html_xpath = '//div[@id="content"]/div/div[3]/div[4]/div/div/div/div/div[2]/p/span/span/span/em'

        em_html_ele_list = self.get_text_ele_list(em_html_xpath)
        for em in em_html_ele_list:
            print '====================================='
            print em.text

    def click_direct_flight_checkbox(self):
        ''' 勾选直飞框 '''
        checkbox_xpath = '//label[@class="lab"]/input'
        checkbox_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            checkbox_xpath,
        )
        if not checkbox_ele:
            return False
        if not ele_utils.request_num(checkbox_ele):
            return False
        return True

    def operate_city_date(self, cityName1, cityName2, date1, date2):
        ''' 城市，时间操作 '''
        fromcity_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[2]/\
            div[1]/div[1]/input'
        if not self.send_city_name(cityName1, fromcity_xpath):
            return False

        if not self.sends_date(date1):
            return False

        if self.is_date_frame:
            print '日期弹框已经弹出来了！'
            if not self.click_date_btn():
                return False

        tocity_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[2]/\
            div[2]/div/input'
        if not self.send_city_name(cityName2, tocity_xpath):
            return False

        self.click_city_frame_close_btn()
        if not self.click_flight_search_btn():
            return False
        return True

    def is_date_frame(self):
        ''' 是否有日期弹框 '''
        date_frame_xpath = '//div[@class="t"]'
        text_ele_list = self.get_text_ele_list(date_frame_xpath, timeout=2)
        if not text_ele_list:
            return False
        if len(text_ele_list) > 0:
            return True
        return False

    def click_city_frame_close_btn(self):
        ''' 关闭热门城市选择按钮 '''
        close_btn_xpath = '//i[@id="closeXI20"]'

        close_btn_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            close_btn_xpath,
            timeout=2
        )
        if not close_btn_ele:
            return False
        if not ele_utils.request_num(close_btn_ele):
            return False
        return True

    def click_flight_search_btn(self):
        ''' 点击机票搜索按钮 '''

        if self.is_date_frame():
            if not self.click_date_btn():
                return False

        btn_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[4]/\
            button'
        btn_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            btn_xpath)
        if not btn_ele:
            return False
        if not ele_utils.request_num(btn_ele):
            return False
        return True

    def send_city_name(self, cityName, cityXpath):
        ''' 输入城市名 '''
        time.sleep(1)
        cityName_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            cityXpath)
        if not cityName_ele:
            return False
        try:
            cityName_ele.clear()
            cityName_ele.send_keys(cityName)
        except:
            return False
        return True

    def click_date_btn(self):
        ''' 点击日历弹框按钮 '''
        time.sleep(1)
        date_btn_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[3]/\
            div[1]/div/div/div[3]/b'
        date_btn_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            date_btn_xpath
        )
        if not date_btn_ele:
            return False
        try:
            date_btn_ele.click()
        except:
            return False
        return True

    def sends_date(self, fromdate):
        ''' 输入时间 '''
        time.sleep(1)
        fromto_date_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/\
            div[3]/div[1]/div/input'
        fromto_date_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            fromto_date_xpath
        )
        fromto_date_value = fromto_date_ele.get_attribute('value')
        if not fromto_date_ele:
            return False
        try:
            fromto_date_ele.click()
            # fromto_date_ele.clear()
            fromto_date_count = len(fromto_date_value)
            n = 0
            while 1:
                if n > fromto_date_count:
                    break
                time.sleep(0.2)
                fromto_date_ele.send_keys(Keys.BACKSPACE)
                n += 1
            fromto_date_ele.send_keys(fromdate)
        except:
            return False
        return True

    def get_text(self, textXpath):
        ''' 获取元素里面的text值 '''
        text_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            textXpath
        )
        if not text_ele:
            return None
        try:
            text_val = text_ele.text
            return text_val
        except:
            return None

    def get_text_ele_list(self, textsXpath, timeout=10):
        ''' 获取元素的列表 '''
        text_ele_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            textsXpath,
            timeout=timeout
        )
        if not text_ele_list:
            return None
        return text_ele_list

if __name__ == '__main__':
    qf = QunarFlight()
    cityName1 = u'成都'
    cityName2 = u'北京'
    outset_date = time.strftime("%Y-%m-%d", time.localtime(time.time() + (3600 * 24 * 7)))
    qf.find_event(cityName1, cityName2, date1=outset_date)

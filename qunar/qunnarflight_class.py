# coding=utf-8
"""
writer: xqs42b
"""

import time
import json
import traceback
import ele_utils
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class QunarFlight(object):
    """
    去哪儿网机票数据查询
    """

    def __init__(self):
        self.driver = self.load_init_page()

    @staticmethod
    def load_init_page():
        """ 加载初始页面 """
        url = 'https://flight.qunar.com/'
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
            except Exception as error:
                print('load_init_page_error:', error)
                init_num += 1
                time.sleep(1)
                driver.refresh()
                continue
            return driver

    def find_event(self, city_name1, city_name2, date1=None):
        """ 入口 """
        if not self.operate_city_date(city_name1, city_name2, date1):
            return None
        return self.get_flight_data()

    def get_flight_data(self):
        """ 获取飞机票数据 """
        self.click_direct_flight_checkbox()
        flight_company_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[1]/span'
        flight_company_list = self.get_text_ele_list(flight_company_xpath)
        flight_number_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[2]/span[1]'
        flight_number_list = self.get_text_ele_list(flight_number_xpath)
        flight_type_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div/div/div[2]/span[2]'
        flight_type_list = self.get_text_ele_list(flight_type_xpath)
        set_out_date_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-lf"]\
            /h2'
        set_out_date_list = self.get_text_ele_list(set_out_date_xpath)
        set_out_airport_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/\
            div[@class="sep-lf"]/p/span[1]'
        set_out_airport_list = self.get_text_ele_list(set_out_airport_xpath)
        set_out_railway_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/\
            div[@class="sep-lf"]/p/span[2]'
        set_out_railway_list = self.get_text_ele_list(set_out_railway_xpath)
        time_cost_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/div[@class="sep-ct"]'
        time_cost_list = self.get_text_ele_list(time_cost_xpath)
        arrival_date_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/\
            div[@class="sep-rt"]/h2'
        arrival_date_list = self.get_text_ele_list(arrival_date_xpath)
        arrival_airport_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/\
            div[@class="sep-rt"]/p/span[1]'
        arrival_airport_list = self.get_text_ele_list(arrival_airport_xpath)
        arrival_railway_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div/div/div[2]/\
            div[@class="sep-rt"]/p/span[2]'
        arrival_railway_list = self.get_text_ele_list(arrival_railway_xpath)
        print('arrival_railway_list:', arrival_railway_list)
        discount_xpath = '//div[@class="content"]/div[3]/div[4]/div/div/div/div/div[2]/div/span'
        discount_list = self.get_text_ele_list(discount_xpath)
        price_list = self.get_price_list()
        flight_datas = list()
        data_num = len(price_list)
        try:
            for d in range(data_num):
                flight_data = dict()
                if flight_company_list:
                    flight_data['fligth_company'] = flight_company_list[d].text
                else:
                    flight_data['fligth_company'] = ''
                if flight_number_list:
                    flight_data['flight_number'] = flight_number_list[d].text
                else:
                    flight_data['flight_number'] = ''
                if flight_type_list:
                    flight_data['flight_type'] = flight_type_list[d].text
                else:
                    flight_data['flight_type'] = ''
                if set_out_date_list:
                    flight_data['set_out_date'] = set_out_date_list[d].text
                else:
                    flight_data['set_out_date'] = ''
                if set_out_airport_list:
                    flight_data['set_out_airport'] = set_out_airport_list[d].text
                else:
                    flight_data['set_out_airport'] = ''
                if set_out_railway_list:
                    flight_data['set_out_railway'] = set_out_railway_list[d].text
                else:
                    flight_data['set_out_railway'] = set_out_railway_list[d].text
                if time_cost_list:
                    flight_data['time_cost'] = time_cost_list[d].text
                else:
                    flight_data['time_cost'] = ''
                if arrival_date_list:
                    flight_data['arrival_date'] = arrival_date_list[d].text
                else:
                    flight_data['arrival_date'] = ''
                if arrival_airport_list:
                    flight_data['arrival_airport'] = arrival_airport_list[d].text
                else:
                    flight_data['arrival_airport'] = ''
                if arrival_railway_list:
                    flight_data['arrival_railway'] = arrival_railway_list[d].text
                else:
                    flight_data['arrival_railway'] = ''
                if discount_list:
                    flight_data['discount'] = discount_list[d].text
                else:
                    flight_data['discount'] = ''
                if price_list:
                    flight_data['price'] = price_list[d]
                else:
                    flight_data['price'] = ''

                flight_datas.append(flight_data)
        except Exception as error:
            print('get_flight_data_error:', error)
            traceback.print_exc()
            return None
        return flight_datas

    def get_price_list(self):
        """ 获取所有机票价格 """
        price_list = list()
        html_source = self.driver.page_source
        em_pattern = r'<em class="rel"><b .*?</b></em>'
        em_ele_list = re.findall(em_pattern, html_source)
        if not em_ele_list:
            return price_list
        del em_ele_list[0]
        for em_ele_str in em_ele_list:
            # 获取宽度值
            width_px_pattern = r'style="width:(\d*)?px;'
            width_px_obj = re.search(width_px_pattern, em_ele_str)
            if not width_px_obj:
                return price_list
            width_px = width_px_obj.group(1)
            if not (width_px.isdigit()):
                return price_list
            # 获取i标签里面的值
            i_ele_pattern = r'">(\d)</i>'
            i_ele_list = re.findall(i_ele_pattern, em_ele_str)
            if not i_ele_list:
                return price_list
            # 获取b标签里面的值
            b_ele_pattern = r'">(\d)</b>'
            b_ele_list = re.findall(b_ele_pattern, em_ele_str)
            if not b_ele_list:
                return price_list

            b_px_pattern = r'left:-(\d*)?px">\d*</b>'
            b_px_list = re.findall(b_px_pattern, em_ele_str)
            if not b_ele_list:
                return price_list
            px_num = len(i_ele_list)
            interval_val = (int(width_px)) / px_num

            current_px = '0'
            for n in range(px_num-1, -1, -1):
                current_px = int(current_px)
                current_px += interval_val
                current_px = str(current_px)
                if current_px not in b_px_list:
                    continue
                i_ele_list[n] = b_ele_list[b_px_list.index(current_px)]
            flight_price = ''.join(i_ele_list)
            price_list.append(flight_price)
        return price_list

    def click_direct_flight_checkbox(self):
        """ 勾选直飞框 """
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

    def operate_city_date(self, city_name1, city_name2, date1):
        """ 城市,时间操作 """
        fromcity_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[2]/\
            div[1]/div[1]/input'
        if not self.send_city_name(city_name1, fromcity_xpath):
            return False

        if not self.sends_date(date1):
            return False

        if self.is_date_frame:
            print('日期弹框已经弹出来了！')
            if not self.click_date_btn():
                return False

        tocity_xpath = '//div[@id="js_flighttype_tab_domestic"]/form/div[2]/\
            div[2]/div/input'
        if not self.send_city_name(city_name2, tocity_xpath):
            return False

        self.click_city_frame_close_btn()
        if not self.click_flight_search_btn():
            return False
        return True

    def is_date_frame(self):
        """是否有日期弹框"""

        date_frame_xpath = '//div[@class="t"]'
        text_ele_list = self.get_text_ele_list(date_frame_xpath, timeout=2)
        if not text_ele_list:
            return False
        if len(text_ele_list) > 0:
            return True
        return False

    def click_city_frame_close_btn(self):
        """关闭热门城市选择按钮"""

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
        """点击机票搜索按钮"""

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

    def send_city_name(self, city_name, city_xpath):
        """
        输入城市名
        :param city_name: 城市名称
        :param city_xpath: 城市的xpath
        :return:
        """
        time.sleep(1)
        city_name_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            city_xpath)
        if not city_name_ele:
            return False
        try:
            city_name_ele.clear()
            city_name_ele.send_keys(city_name)
        except Exception as error:
            print('send_city_name_error:', error)
            return False
        return True

    def click_date_btn(self):
        """点击日历弹框按钮"""
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
        except Exception as error:
            print('click_date_btn_error:', error)
            return False
        return True

    def sends_date(self, fromdate):
        """输入时间"""
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
        except Exception as error:
            print('sends_date_error:', error)
            return False
        return True

    def get_text(self, text_xpath):
        """获取元素里面的text值"""
        text_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            text_xpath
        )
        if not text_ele:
            return None
        try:
            text_val = text_ele.text
            return text_val
        except Exception as error:
            print('get_text_error:', error)
            return None

    def get_text_ele_list(self, texts_xpath, timeout=3):
        """
        :param texts_xpath: 文本xpath
        :param timeout: 请求超时
        """
        text_ele_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            texts_xpath,
            timeout=timeout
        )
        if not text_ele_list:
            return None
        return text_ele_list


if __name__ == '__main__':
    qf = QunarFlight()
    send_city_name1 = u'成都'
    send_city_name2 = u'北京'
    outset_date = time.strftime(
        "%Y-%m-%d",
        time.localtime(time.time() + (3600 * 24 * 7)))
    datas = qf.find_event(send_city_name1, send_city_name2, date1=outset_date)
    print(json.dumps(datas))

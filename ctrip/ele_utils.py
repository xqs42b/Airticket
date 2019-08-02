# encoding=utf8

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec_obj


def get_element_for_wait(driver, by, by_s, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(ec_obj.presence_of_element_located((by, by_s)))
        ele = driver.find_element(by, by_s)
        return ele
    except Exception as error:
        print(error)
    return None


def get_include_hide_element_for_wait(driver, by, by_s, timeout=5):
    try:
        ele = WebDriverWait(driver, timeout).until(
            ec_obj.visibility_of_element_located((by, by_s))
        )
        return ele
    except Exception as error:
        print(error)
    return None


def get_include_hide_elements_for_wait(driver, by, by_s, timeout=5):
    try:
        ele = WebDriverWait(driver, timeout).until(
            ec_obj.visibility_of_all_elements_located((by, by_s))
        )
        return ele
    except Exception as error:
        print(error)
    return None
    

def get_elements_for_wait(driver, by, by_s, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(ec_obj.presence_of_element_located((by, by_s)))
        ele = driver.find_elements(by, by_s)
        return ele
    except Exception as error:
        print(error)
    return None

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By

from time import sleep


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('http://192.168.1.1')
    sleep(2)
    password = driver.find_element_by_id('focus_password')
    password.send_keys('admin')
    sleep(1)
    submit = driver.find_elements_by_tag_name('input')[2]
    submit.click()
    sleep(2)
    macvlan = driver.find_element_by_partial_link_text('虚拟WAN')
    macvlan.click()
    try:
        element = WebDriverWait(driver, 20).until(ES.presence_of_element_located((By.ID, 'cbi-macvlan_rediag-config-action')))
        reset = driver.find_element_by_id('cbi-macvlan_rediag-config-action')
        reset.click()
    except Exception as e:
        print(e)

    sleep(5)
    driver.close()

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import requests
import json
import logging
from douban.spiders.doubanmovie import DoubanmovieSpider
import scrapydo
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
from datetime import datetime
import os
from douban.util import VPNDial
scrapydo.setup()


def resetip():
    """change the ip of Openwrt Router through the web, not used in the version """
    driver = webdriver.PhantomJS()
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
        element = WebDriverWait(driver, 20).until(
            ES.presence_of_element_located((By.ID, 'cbi-macvlan_rediag-config-action')))
        reset = driver.find_element_by_id('cbi-macvlan_rediag-config-action')
        reset.click()
    except Exception as e:
        print(e)

    sleep(5)
    driver.close()


if __name__ == '__main__':

    printer_status = True  # whether or not print the info of spider start and stop time.

    # clean the content in the status.txt;check the content of status.txt before the next loop of crawl,
    # if the content is equal to 'exit' , the script will end,
    # else continue to run
    with open('status.txt', 'w') as file:
        pass

    VPN = VPNDial('txtz', '111')
    VPN.connect()
    while VPN.getstatus() == 1:
        sleep(3)
        VPN.connect()

    logging.basicConfig(
        level=logging.INFO, # set the log level to INFO level
        format='%(levelname)s :%(asctime)s: %(message)s',
        filename='crawl-%s.log' % datetime.now().strftime('%Y%m%d'),
    )

    while True:
        if printer_status:
            print('the spider started at %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logging.info('the spider started')
        scrapydo.default_settings.update({
                                          'CONCURRENT_REQUESTS': 100, # the num of concurrent_requests
                                          'CONCURRENT_ITEMS': 500, # the num of CONCURRENT_ITEMS
                                          })
        scrapydo.run_spider(spider_cls=DoubanmovieSpider)
        if printer_status:
            print('the spider stopped at %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logging.info('the spider stopped normally')

        # disconnect the pptp vpn and wait for the change of ip
        VPN.disconnect()
        while VPN.getstatus() == 1:
            VPN.connect()
            sleep(3)

        if os.path.exists('status.txt'):
            with open('status.txt') as file:
                if file.readline().strip() == 'exit':
                    logging.info('the crawl exited gracefully')
                    VPN.disconnect()
                    sleep(5)
                    break






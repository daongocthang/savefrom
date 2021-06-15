import os
import time
from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import BrowserFactory


class Action(Enum):
    SHOW = 'show'
    WRITE = 'write'


class SaveFrom:

    def __init__(self):
        self.br = BrowserFactory.create_browser()
        self.br.get('https://en.savefrom.net/')
        time.sleep(5)

    def get_link(self, url, timeout=100):
        search_box = self.br.find_element_by_name('sf_url')
        search_box.clear()
        search_box.send_keys(url)
        search_box.submit()

        wait = WebDriverWait(self.br, timeout)
        # elem = self.br.find_element_by_xpath('//a[contains(text(),"Download")]')
        elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@title,"video format")]')))
        return elem.get_attribute('href')

    def close(self):
        self.br.close()


if __name__ == '__main__':
    sf = SaveFrom()
    data_links = []

    f = open('watchlist.txt', 'r')
    for url in f:
        try:
            data_links.append(sf.get_link(url))
        except:
            pass
    f.close()

    with open('data_links.txt', 'w') as f:
        for s in data_links:
            f.write(s)
            f.write('\n')

    sf.close()

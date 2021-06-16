import argparse
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser import BrowserFactory


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
    parser = argparse.ArgumentParser()
    parser.add_argument('address', help='the default is a URL')
    parser.add_argument('-i', '--import', dest='im', action='store_true',
                        help='define the address is a file path')
    parser.add_argument('-o', '--output', metavar='', default=os.getcwd(),
                        help='where to store the result (default: current directory)')

    args = parser.parse_args()

    assert os.path.exists(args.output), '{} Not Exist'.format(args.output)
    dest = os.path.join(args.output, 'data-links.txt')

    res = []
    sf = SaveFrom()
    if args.im:
        assert os.path.exists(args.address), 'Not found {}'.format(args.address)
        with open(args.address, 'r') as f:
            for u in f:
                try:
                    res.append(sf.get_link(u))
                except:
                    pass
    else:
        try:
            res = [sf.get_link(args.address)]
        except:
            pass

    with open(dest, 'w') as f:
        for line in res:
            f.write(line)
            f.write('\n')

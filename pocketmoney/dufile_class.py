# coding=utf-8

import config
import ocr_text_baidu
import image_noice_reduce
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from PIL import Image
import time
from bs4 import BeautifulSoup
import requests
import os
import base64


class DuFile:

    def run(self, url):
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument("--proxy-server=http://125.59.157.236:80")
        # driver = webdriver.Chrome(chrome_options=chromeOptions)
        # driver = self.get_webdriver()
        driver = webdriver.Chrome()
        driver.maximize_window()


        # self.driver.get("http://dufile.com/file/3a3637a24a3daf43.html")
        driver.get(url)

        driver.implicitly_wait(60)

        normal_download_btn = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "slow_button")))
        normal_download_btn.click()

        txt_vcode = WebDriverWait(driver, 35).until(expected_conditions.visibility_of_element_located((By.ID, "code")))
        # txt_vcode = driver.find_element_by_id("code")
        vcode = driver.find_element_by_id("vcode_img")
        btn_vcode = driver.find_element_by_name("Submit")

        ocr_result = self.get_vcode(driver=driver)
        run_result = 0
        is_not_valid = True
        while is_not_valid:
            for r in ocr_result['words_result']:
                print(r['words'])
                if '-' in r['words']:
                    numbers = r['words'].split('-')
                    run_result = int(numbers[0]) - int(numbers[1])
                    is_not_valid = False
                elif '+' in r['words']:
                    numbers = r['words'].split('+')
                    run_result = int(numbers[0]) + int(numbers[1])
                    is_not_valid = False
                else:
                    ocr_result = self.get_vcode(driver=driver, is_refresh=True)

        print(run_result)
        txt_vcode.send_keys(run_result)
        btn_vcode.click()

        download_link = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "downbtn")))
        download_link.click()

        time.sleep(10)

        iframes = driver.find_elements_by_tag_name('iframe')
        for iframe in iframes:
            h = iframe.size["height"]
            w = iframe.size["width"]
            if h == 316 and w == 352:
                driver.switch_to.frame(iframe)
                break
            else:
                continue

        # print(driver.page_source)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        d_link = soup.find('a', id="downs")
        print(d_link['href'])
        self.download_file(d_link['href'])
        self.close_window(driver)

    def get_vcode(self, driver, is_refresh=False):
        if is_refresh:
            driver.refresh()

        vcode = driver.find_element_by_id("vcode_img")
        location = vcode.location
        size = vcode.size
        driver.get_screenshot_as_file("%s/full.png" % config.TEMP_IMAGE_PATH)
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        i = Image.open("%s/full.png" % config.TEMP_IMAGE_PATH)  # 打开截图
        frame1 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame1.save("%s/vcode.png" % config.TEMP_IMAGE_PATH)

        image_noice_reduce.main("%s/vcode.png" % config.TEMP_IMAGE_PATH)
        ocr_result = ocr_text_baidu.main()

        return ocr_result

        # i = Image.open("%s/image_after_reduce.jpg" % config.TEMP_IMAGE_PATH)  # 打开截图
        # i = i.convert('L')
        # i.save("%s/image_after_reduce.jpg" % config.TEMP_IMAGE_PATH)

    def download_file(self, url):

        # ip_port = '123.134.227.114:4945'  # 从api中提取出来的代理IP:PORT
        ip_port = requests.get("http://api.qingtingip.com/ip?app_key=4d31063caf1a3e19434ddd7e980a04e6&num=1&ptc=socks5&fmt=text&port=0&mr=2").text
        username = 'samhocngz@163.com'
        password = 'Go4Samho123'

        headers = {
            'Proxy-Authorization': 'Basic %s' % (self.base_code(username, password))
        }

        proxy = {
            'http': 'socks5://{}'.format(ip_port),
            'https': 'socks5://{}'.format(ip_port)
        }

        # download_obj = requests.get(url, proxies=proxy, headers=headers)
        download_obj = requests.get(url)
        file_name = url.split('?')[0].split('/')[4]

        if os.path.exists("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name)):
            os.remove("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name))

        with open("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name), 'wb') as download_real:
            download_real.write(download_obj.content)

    def base_code(self, username, password):
        str = '%s:%s' % (username, password)
        encodestr = base64.b64encode(str.encode('utf-8'))
        return '%s' % encodestr.decode()

    def close_window(self, driver):
        driver.close()


if __name__ == "__main__":
    dufile = DuFile()
    dufile.run("http://dufile.com/file/e02b3dd607799732.html")
    # dufile.download_file("http://ss3.sufile.net:3637/down/Linux-101-Hacks.pdf?key=lEP%2BAFfsgQIFmMvfneh%2BCUee2TytOG0DzoLSDQGcD1YjLGVKqKsKsLLGKfl4GGpl5kQdiFhd7PSbY3sn%2FbDRdqzGMWmwm8Jk24aMrQHDqBoYUGuFSuQMo5uGtGFjeeVhg%2FFDKKyTLlpliXY4H%2Fu2rEeerNLoTWQN")

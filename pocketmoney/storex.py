# coding=utf-8

import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from bs4 import BeautifulSoup
import os
import base64
import random


class Storex:

    def run(self, url):

        file_name = url.split("/")[-1]
        # clear the existed file in download folder.
        if os.path.exists("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name)):
            os.remove("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name))

        ### For Chrome Browser
        chromeoptions = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': config.TEMP_DOWNLOAD_PATH}
        chromeoptions.add_experimental_option('prefs', prefs)
        chrome_driver_path = config.basedir + os.sep + "res" + os.sep + "chromedriver_mac"
        driver = webdriver.Chrome(chrome_driver_path, options=chromeoptions)

        ### For Firefox Browser
        # fp = webdriver.FirefoxProfile()
        # fp.set_preference("browser.download.folderList", 2)
        # fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        # fp.set_preference("browser.download.manager.showWhenStarting", False)
        # fp.set_preference("browser.download.dir", config.TEMP_DOWNLOAD_PATH)
        # fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        # driver = webdriver.Firefox(firefox_profile=fp)

        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(20)

        # normal_download_btn = driver.find_element_by_id("method_free")
        normal_download_btn = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "method_free")))
        driver.save_screenshot(config.basedir + os.sep + "res" + os.sep + "test.jpg")
        agree_div = driver.find_elements_by_id("gdpr-cookie-notice")
        btn = agree_div[0].find_elements_by_xpath("./input")
        btn[0].click()

        # if agree_div.is_displayed():
        #     cookie_agree_btn = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='gdpr-cookie-notice']/input")))
        #     print(cookie_agree_btn.text)
        #     cookie_agree_btn.click()
        cur_cookies = driver.get_cookies()
        print(cur_cookies)
        normal_download_btn.location_once_scrolled_into_view
        normal_download_btn.click()

        txt_wait = WebDriverWait(driver, 125).until(expected_conditions.invisibility_of_element_located((By.ID, "countdown")))
        txt_code = driver.find_element_by_xpath("//input[@name='code']")
        btn_vcode = driver.find_element_by_xpath("//button[@id='downloadbtn']/span[2]")

        # Get the verify code
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        span_code = soup.find("div", id="commonId").find_all('span', style=True)
        v_code = {}
        k_code = []
        for s in span_code:
            if "padding-left" in s["style"]:
                # print(s.text)
                key = s["style"].split(";")[1].split(":")[1][:-2]
                k_code.append(int(key))
                v_code[key] = s.text
                # print(key)
            else:
                continue
        t_code = ""
        k_code.sort()
        for i in k_code:
            t_code = t_code + str(v_code[str(i)])
        print(t_code)

        # Try to download file.
        txt_code.send_keys(t_code)
        btn_vcode.location_once_scrolled_into_view
        btn_vcode.click()
        # 等待下载完成
        while not os.path.exists("%s/%s" % (config.TEMP_DOWNLOAD_PATH, file_name)):
            time.sleep(10)

        self.close_window(driver)

    def base_code(self, username, password):
        str = '%s:%s' % (username, password)
        encodestr = base64.b64encode(str.encode('utf-8'))
        return '%s' % encodestr.decode()

    def close_window(self, driver):
        driver.close()


if __name__ == "__main__":

    for i in range(1):
        storex = Storex()
        download_url = config.STOREX_DOWNLOAD_LIST[random.randint(1, len(config.STOREX_DOWNLOAD_LIST))-1]
        print(download_url)
        storex.run(download_url)
        print("Start to sleep .....")
        # time.sleep(600)

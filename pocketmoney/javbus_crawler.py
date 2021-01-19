# coding=utf-8
import config
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from pynput.keyboard import Key, Controller
import clipboard
import json
import sys
from bs4 import BeautifulSoup
import requests


class JavBusCrawler:

    def download(self, url):
        print("Download: ", url)
        try:
            html = requests.get(url).text
        except requests.exception as e:
            print("Download error: ", e.reason)
            html = None
        return html

    def get_list_by_name(self, name, is_fuzzy=False):
        with open(config.basedir + os.sep + "res" + os.sep + "javbus_actors.json", "r") as f:
            actor_link_list = []
            actors = json.loads(f.readline())
            for actor in actors["movies"]:
                if is_fuzzy:
                    if name in actor["Actor Name"]:
                        # print("%s, %s" % (actor["Actor Name"], actor["Link"]))
                        actor_link_list.append(actor)
                else:
                    if name == actor["Actor Name"]:
                        # print("%s, %s" % (actor["Actor Name"], actor["Link"]))
                        actor_link_list.append(actor)

        return actor_link_list

    def get_movies_by_url(self, url):

        MOVIES_PER_PAGE = 30
        html = self.download(url)
        soup = BeautifulSoup(html, 'html.parser')
        total_movie = soup.find(id="resultshowmag").text.strip()[5:]
        if int(total_movie) % MOVIES_PER_PAGE == 0:
            if int(total_movie) <= MOVIES_PER_PAGE:
                pages = 1
            else:
                pages = int(total_movie) // MOVIES_PER_PAGE
        else:
            pages = int(total_movie) // MOVIES_PER_PAGE + 1

        for page in range(1, pages+1):
            movies_url = url + "/" + str(page)
            movies_soup = BeautifulSoup(self.download(movies_url), 'html.parser')
            movies_a = movies_soup.find_all("a", class_="movie-box")
            for a in movies_a:
                self.get_link_by_url(a["href"])

    def get_link_by_url(self, url, is_chrome=True):

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
        # is_chrome = False

        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(20)

        fan_number = driver.find_element_by_xpath("/html/body/div[5]/div[1]/div[2]/p[1]/span[2]").text


        # Copy the select link with Robot Framework.
        keyboard = Controller()
        if is_chrome:
            latest_link = driver.find_element_by_xpath("//table[@id='magnet-table']/tr/td/a")
            ActionChains(driver).context_click(latest_link).perform()
            for i in range(4):
                keyboard.press(Key.down)
            keyboard.press(Key.enter)
            time.sleep(1)
            link = clipboard.paste()
        else:
            for i in range(15):
                keyboard.press(Key.down)
            time.sleep(5)
            latest_link = driver.find_element_by_xpath("//table[@id='magnet-table']/tr/td/a")
            ActionChains(driver).context_click(latest_link).perform()
            for i in range(6):
                keyboard.press(Key.down)
            keyboard.press(Key.enter)
            time.sleep(1)
            link = clipboard.paste()

        print("Movie Name: %s, Download Link: %s" %(fan_number, link))
        driver.close()

    def main(self, name, is_fuzzy=False):

        if is_fuzzy:
            actor_links = self.get_list_by_name(name, is_fuzzy=True)
            if actor_links is None:
                print("There is noting found with name %s" % name)
                sys.exit(1)
            else:
                print("There are some actors found:")
                for actor in actor_links:
                    print("Actor name: %s, link: %s" % (actor["Actor Name"], actor["Link"]))
                sys.exit(2)
        else:
            actor_links = self.get_list_by_name(name)
            if actor_links is None:
                print("There is noting found with name %s" % name)
                sys.exit(1)
            else:
                print("There is a actor found, link is %s" % actor_links[0]["Link"])
                self.get_movies_by_url(actor_links[0]["Link"])


if __name__ == "__main__":
    crawler = JavBusCrawler()
    crawler.main("伊藤さらら", is_fuzzy=False)


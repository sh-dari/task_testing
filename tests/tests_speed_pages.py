import pychrome
import keyboard
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support.ui import WebDriverWait


class TestSpeed(unittest.TestCase):
    def setUp(self):
        def clear_cache():
            self.driver.get('chrome://settings/clearBrowserData')
            keyboard.send("Enter")
        self.options = chrome_options()
        self.options.add_argument('chrome')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--window-size=1650,900')
        self.driver = webdriver.Chrome(
            executable_path=r"C:\chromedriver\chromedriver.exe",
            options=self.options
        )
        clear_cache()
        self.driver.delete_all_cookies()
        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.file = open('result.txt', 'a+')

    def test_homepage(self):
        def page_load_data(driver):
            navigationStart = driver.execute_script(
                "return window.performance.timing.navigationStart"
            )
            responseStart = driver.execute_script(
                "return window.performance.timing.responseStart"
            )
            domComplete = driver.execute_script(
                "return window.performance.timing.domComplete"
            )
            loadEventStart = driver.execute_script(
                "return window.performance.timing.loadEventStart"
            )
            domainLookupEnd = driver.execute_script(
                "return window.performance.timing.domainLookupEnd"
            )
            domainLookupStart = driver.execute_script(
                "return window.performance.timing.domainLookupStart"
            )
            connectStart = driver.execute_script(
                "return window.performance.timing.connectStart"
            )
            connectEnd = driver.execute_script(
                "return window.performance.timing.connectEnd"
            )
            self.file.write(str(domComplete - responseStart) + "\n")
            self.file.write(
                "Time to First Byte: " + str(responseStart - navigationStart)
                + "\n")
            self.file.write(
                "Page load time: " + str(loadEventStart - navigationStart)
                + "\n")
            self.file.write(
                "DNS lookup: " + str(domainLookupEnd - domainLookupStart)
                + "\n")
            self.file.write("TCP: " + str(connectEnd - connectStart) + "\n")
            self.file.close()
        self.file.write("\nTEST 1\n")
        driver = self.driver
        browser = self.browser
        url = "https://sbis.ru/ofd"

        tabs = browser.list_tab()
        if not tabs:
            tab = browser.new_tab()
        else:
            tab = tabs[0]

        tab.start()

        tab.Network.enable(_timeout=20)
        # tab.set_listener("Network.requestWillBeSent", output_on_start)
        # tab.set_listener("Network.responseReceived", output_on_end)
        tab.Network.clearBrowserCookies()
        driver.get(url)
        # tab.Network.setCacheDisabled(cacheDisabled=True)
        # tab.Page.navigate(url="https://sbis.ru/ofd", _timeout=5)
        page_load_data(driver)
        tab.wait(5)
        tab.stop()

        browser.close_tab(tab)

    def test_stack_panels(self):
        self.file.write("\nTEST 2 \n")
        xpaths = ['//*[@id="wasaby-content"]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[5]/span/span/span',
                  '//*[@id="wasaby-content"]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div[6]/div',
                  '//*[@id="wasaby-content"]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/a[3]/span[3]',
                  '//*[@id="popup"]/div/div/div[2]/div/div[2]/div/div/div/table/tr/td[1]/div[1]/div[1]/a']
        driver = self.driver
        browser = self.browser
        url = r"https://online.sbis.ru/auth/?ret=%2Fauth"

        def onLoad(start):
            now = time.time()
            return str(now - start)

        tabs = browser.list_tab()
        if not tabs:
            tab = browser.new_tab()
        else:
            tab = tabs[0]

        tab.start()

        # tab.Network.enable(_timeout=20)
        tab.Network.clearBrowserCookies()
        # tab.Network.setCacheDisabled(cacheDisabled=True)
        driver.get(url)
        tab.wait(3)
        for i in range(len(xpaths)):
            elem = driver.find_element(By.XPATH, xpaths[i])
            elem.click()
            tab.wait(3)
        card = driver.find_element(
            By.XPATH,
            '//*[@id="91468"]'
        )
        start = time.time()
        card.click()
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState')
            == 'complete'
        )
        self.file.write("Card opening speed: " + onLoad(start) + "\n")
        self.file.write("---------------------------------------------\n")
        self.file.close()
        tab.wait(3)
        tab.stop()
        browser.close_tab(tab)


if __name__ == '__main__':
    unittest.main()

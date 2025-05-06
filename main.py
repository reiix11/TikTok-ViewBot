from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.common.by   import By
from selenium.webdriver.support     import expected_conditions as EC
from loguru                         import logger
from time                           import sleep

import undetected_chromedriver as uc
import os, platform

class Zefoy:
    def __init__(self):
        self.chrome_options = uc.ChromeOptions()
        self.driver         = uc.Chrome(options=self.chrome_options)
        self.driver.set_window_size(600, 900)

        self.xpath = {
            'views'          : '/html/body/div[6]/div/div[2]/div[1]/div/div[6]/div/button',

            'captcha_box'    : '//*[@id="captchatoken"]',
            'captcha_submit' : '/html/body/div[5]/div[2]/form/div/div/div/div/button',
        }

    def clear(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def captcha(self, captcha_code):
        try:
            captcha_input = self.driver.find_element(By.XPATH, self.xpath['captcha_box'])
            captcha_input.clear()
            captcha_input.send_keys(captcha_code)

            submit_captcha = self.driver.find_element(By.XPATH, self.xpath['captcha_submit'])
            submit_captcha.click()

            logger.success('captcha submitted\n')

        except Exception as e:
            logger.error(f'captcha error: {e}')

    def worker(self, link, captcha_code):
        try:
            self.clear()
            self.captcha(captcha_code)

            click_views = self.driver.find_element(By.XPATH, self.xpath['views'])
            click_views.click()
            sleep(3)

            enter_input = self.driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
            enter_input.send_keys(link)
            sleep(10)

            while True:
                try:
                    search1 = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div/form/div/div/button'))
                    )
                    search1.click()
                    sleep(10)

                    search2 = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div/form/div/div/button'))
                    )
                    search2.click()
                    sleep(10)

                    send = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button'))
                    )
                    send.click()
                    sleep(10)
                    logger.success('500 views sent')

                except Exception as e:
                    pass

        except Exception as e:
            pass

    def main(self):
        self.clear()
        self.driver.get('https://zefoy.com/')

        captcha_code = input('? - enter captcha code >>> ')
        link         = input('? - enter video link   >>> ')
        self.worker(link, captcha_code)

if __name__ == '__main__':
    Zefoy().main()

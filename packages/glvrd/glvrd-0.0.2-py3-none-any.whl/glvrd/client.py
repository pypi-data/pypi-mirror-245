import time
from dataclasses import dataclass, field
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from pageo import BasePage, XPATHLocator
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class EstimationResult:
    estimate: Optional[float] = None
    errors: dict[str, str] = field(default_factory=lambda: {})

class IndexPage(BasePage):
    base_url = 'https://glvrd.ru/'

    empty_input_field = XPATHLocator('//*[@id="glaveditor-id"]/div[1]')
    full_input_field = XPATHLocator('//*[@id="glaveditor-id"]/div[1]/p', is_many=True)
    estimate = XPATHLocator('//*[@id="app"]/div/div[3]/div[1]/div[2]/div[3]/div[1]/span[1]')
    highlighted_error_name = XPATHLocator('//*[@id="app"]/div/div[3]/div[2]/div/div/div/div/h1')
    clarity_screen_on = XPATHLocator('//*[@id="app"]/div/div[3]/div[1]/div[1]/span[1]')
    readability_screen_on = XPATHLocator('//*[@id="app"]/div/div[3]/div[1]/div[1]/span[2]')


class GlvrdClient:
    def __init__(self):
        self.driver = self.get_driver()
        self.page = self.get_page_object(self.driver)

    def __del__(self):
        self.driver.quit()

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service=ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    def get_page_object(self, driver):
        return IndexPage(driver=driver)

    def estimate_something(self, text, sleep_before_result=4):
        result = EstimationResult()

        self.page.empty_input_field.clear()
        self.page.empty_input_field.send_keys(text)

        time.sleep(sleep_before_result)

        result.estimate = float(self.page.estimate.text.replace(',', '.'))

        action = webdriver.ActionChains(self.driver)

        for text_block in self.page.full_input_field:
            for highlighted_text_element in text_block.find_elements(By.XPATH, ".//em"):
                highlighted_text = highlighted_text_element.text
                action.move_to_element(highlighted_text_element).perform()
                error_name = self.page.highlighted_error_name.text
                if result.errors.get(error_name) is None:
                    result.errors[error_name] = []
                result.errors[error_name].append(highlighted_text)

        return result

    def estimate_clarity(self, text, sleep_before_result=4):
        self.page.clarity_screen_on.click()
        return self.estimate_something(text, sleep_before_result=sleep_before_result)

    def estimate_readability(self, text, sleep_before_result=4):
        self.page.readability_screen_on.click()
        return self.estimate_something(text, sleep_before_result=sleep_before_result)

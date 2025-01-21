import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import (
    ChromeDriverManager,
)
from typing import List
import os
import time


class ChatGPTScraper:
    def __init__(self, subprocess_path: str, subprocess_port: int):
        self.url = "https://chat.openai.com/"
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{subprocess_port}"
        )
        self.driver = self._initialize_driver(subprocess_path)
        self.driver.get(self.url)

    def _initialize_driver(self, subprocess_path):
        self.open_subprocess(subprocess_path)
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )

    def open_subprocess(self, subprocess_path: str):
        subprocess.Popen(subprocess_path)

    def close_subprocess(self):
        self.driver.quit()
        subprocess.Popen("taskkill /f /im chrome.exe")  # TODO: control exceptions

    def search_chatgpt(self, url: str, query: str) -> List[str]:
        url = self.url if url is None else url
        results = None
        wait = WebDriverWait(self.driver, 10)
        try:
            # if page not equal with current page, change page
            if self.driver.current_url != url:
                self.driver.get(url)

            search_box = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "p.placeholder"))
            )
            search_box.click()
            search_box.send_keys(query)

            send_btn = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button[data-testid='send-button']",
                    )
                )
            )
            send_btn.click()

            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "button[data-testid='stop-button']")
                )
            )

            responses = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div > div > div > div > article > div > div",
            )
            last_response = responses[-1]
            results = last_response.text
        except Exception as e:
            print(f"Error during ChatGPT search: {e}")

        return results, self.driver.current_url


if __name__ == "__main__":
    WINDOW_CHROME_SUBPROCESS_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"'
    SUBPROCESS_PORT = 9222

    # Example usage
    CHROME_SUBPROCESS_PATH = os.getenv(
        "CHROME_SUBPROCESS_PATH", WINDOW_CHROME_SUBPROCESS_PATH
    )
    subprocess_port = os.getenv("SUBPROCESS_PORT", SUBPROCESS_PORT)
    scraper = ChatGPTScraper(
        subprocess_path=CHROME_SUBPROCESS_PATH, subprocess_port=SUBPROCESS_PORT
    )
    print(scraper.search_chatgpt(None, "What is the capital of France?"))

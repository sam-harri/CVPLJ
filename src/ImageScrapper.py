from typing import Set, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ImageScraper:
    def __init__(self):
        self.urls: Set[str] = set()
        self.driver: WebDriver = webdriver.Chrome()

    def get_image_urls(self, search_param: str) -> Set[str]:
        # Set search URL
        search_url: str = f"https://www.google.com/search?q={search_param.replace(' ', '+')}&tbm=isch"
        self.driver.get(search_url)
        time.sleep(2)  # Initial wait for page to load

        SCROLL_PAUSE_TIME: int = 2

        # Initialize previous height
        last_height: int = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait until new images are loaded
            time.sleep(SCROLL_PAUSE_TIME)
            new_height: int = self.driver.execute_script("return document.body.scrollHeight")

            # Parse the current page
            soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Collect image URLs
            for img in soup.find_all('img'):
                src: str = img.get('src')
                if src:
                    self.urls.add(src)

            # Check for the "More results" span
            load_more_span = soup.find('span', string='More results')
            if load_more_span:
                span_class: str = load_more_span['class'][0]
                try:
                    # Click the span element based on its class
                    load_more_button = self.driver.find_element(By.CLASS_NAME, span_class)
                    self.driver.execute_script("arguments[0].click();", load_more_button)

                    # Wait until new images are loaded
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
                    )
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking 'More results' span: {e}")
                    break

            # Check if the scroll height has changed
            if new_height == last_height:
                print("No more scrolling possible.")
                break
            last_height = new_height

        return self.urls

    def scrape_images(self, search_params: List[str]) -> Set[str]:
        for param in search_params:
            self.get_image_urls(param)

        # Close the browser
        self.driver.quit()

        return self.urls

    def save_urls_to_file(self, file_path: str):
        with open(file_path, 'w') as f:
            for url in self.urls:
                f.write(f"{url}\n")

# Example usage
imgscaper = ImageScraper()
search_params = ["USAPL Powerlifting Squat", "Powerlifting Squat Sideview", "Powerlifting Squat Competition"]
collected_urls = imgscaper.scrape_images(search_params)
imgscaper.save_urls_to_file('image_urls.txt')

print(f"Collected {len(collected_urls)} image URLs.")

from typing import Set
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_image_urls(search_param: str) -> Set[str]:
    # Initialize WebDriver
    driver: WebDriver = webdriver.Chrome()
    
    # Record start time
    start_time = time.time()

    # Set search URL
    search_url: str = f"https://www.google.com/search?q={search_param.replace(' ', '+')}&tbm=isch"
    driver.get(search_url)
    time.sleep(2)  # Initial wait for page to load

    # Set to store image URLs
    urls: Set[str] = set()
    SCROLL_PAUSE_TIME: int = 2

    # Initialize previous height
    last_height: int = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait until new images are loaded
        WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
        )

        # Parse the current page
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')

        # Collect image URLs
        for img in soup.find_all('img'):
            src: str = img.get('src')
            if src:
                urls.add(src)

        # Check for the "More results" span
        load_more_span = soup.find('span', string='More results')
        if load_more_span:
            span_class: str = load_more_span['class'][0]
            try:
                # Click the span element based on its class
                load_more_button = driver.find_element(By.CLASS_NAME, span_class)
                driver.execute_script("arguments[0].click();", load_more_button)

                # Wait until new images are loaded
                WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
                )
                time.sleep(2)
            except Exception as e:
                print(f"Error clicking 'More results' span: {e}")
                break

        # Check if the scroll height has changed
        new_height: int = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more scrolling possible.")
            break
        last_height = new_height

    # Close the browser
    driver.quit()

    # Record end time
    end_time = time.time()
    duration = end_time - start_time

    print(f"Collected {len(urls)} image URLs in {duration:.2f} seconds with search string {search_param}.")

    return urls

get_image_urls("USAPL powerlifting squat")
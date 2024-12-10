import os
import random
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Function to introduce a random delay between actions
def delay(min_delay=3, max_delay=5):
    """
    Introduces a random delay to mimic human behavior.
    Args:
        min_delay (int): Minimum delay in seconds.
        max_delay (int): Maximum delay in seconds.
    """
    time.sleep(random.randint(min_delay, max_delay))

# Function to read URLs from an Excel file
def read_sheet(file_path='urls.xlsx'):
    """
    Reads URLs from an Excel file and returns them as a list.
    Args:
        file_path (str): Path to the Excel file containing URLs.
    Returns:
        list: List of URLs from the Excel file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file '{file_path}' not found.")
    df = pd.read_excel(file_path)
    urls = df.iloc[:, 0].to_list()
    return urls

# Function to configure Chrome WebDriver options
def configure_chrome_options():
    """
    Configures and returns Chrome WebDriver options.
    Returns:
        Options: Configured Chrome WebDriver options.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return options

# Function to download images from a webpage
def download_images(driver, output_dir):
    """
    Downloads images from a webpage.
    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
        output_dir (str): Directory to save downloaded images.
    """
    img_urls = set()
    images = driver.find_elements(By.XPATH, '//div[@class="image-galleria_wrap"]//img')
    for idx, img in enumerate(images, start=1):
        url = img.get_attribute('hd-url')
        if url and url not in img_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                output_file = os.path.join(output_dir, f'{idx}.jpg')
                with open(output_file, "wb") as file:
                    file.write(response.content)
                img_urls.add(url)
                print(f'Saved the image; {url} in {output_dir}')
            except requests.RequestException as e:
                print(f"Error downloading image {url}: {e}")

# Main function to process URLs and download images
def main(urls, driver):
    """
    Main function to scrape data from the URLs and download images.
    Args:
        urls (list): List of URLs to scrape.
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    for url in urls:
        try:
            driver.get(url)
            delay()
            # Extract title and VIN
            title = driver.find_element(By.XPATH, '//div[@class="title-and-highlights"]/h1').text
            vin = driver.find_element(By.XPATH, '//div[@ng-if="ukVinNumber"]').text.replace('VIN:', '').replace('*', '').strip()
            output_dir = f"{title}_{vin}"

            if not os.path.exists(output_dir):
                print(f"Creating folder to save images: {output_dir}")
                os.makedirs(output_dir)

            download_images(driver, output_dir)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

# Entry point of the script
if __name__ == '__main__':
    try:
        # Set up WebDriver
        driver = webdriver.Chrome(options=configure_chrome_options())

        # Read URLs from the Excel sheet
        urls = read_sheet()

        # Start processing URLs
        main(urls, driver)
    finally:
        # Ensure the WebDriver is properly closed
        if 'driver' in locals():
            driver.quit()
            print('Closed the Web Browser..')

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
import os
import time

# Get the ChromeDriver path from the environment variable
chrome_driver_path = os.getenv('CHROMEDRIVER_PATH')

# Initialize the ChromeOptions
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Set up the service and driver
service = Service(chrome_driver_path)

# Initialize the Chrome WebDriver with options and service
driver = webdriver.Chrome(options=options, service=service)

# Set the page load timeout
driver.set_page_load_timeout(300)  # Timeout in seconds

website_url = 'https://www.bayt.com/en/international/jobs/'
driver.get(website_url)

try:
    # Wait for the "Past 24 hours" filter to be visible
    past_24_hours = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, '//a[@data-automation-id="Past-24-hours"]'))
    )

    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", past_24_hours)
    time.sleep(1)  # Wait for the scroll to complete

    # Click the element using JavaScript
    driver.execute_script("arguments[0].click();", past_24_hours)
except Exception as e:
    print("Error clicking 'Past 24 hours':", e)
    driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging
    driver.quit()
    exit()

 # Wait for the job elements to be present

while True:
        jobs = WebDriverWait(driver, 100).until(
                            EC.visibility_of_all_elements_located((By.XPATH, '//a[@data-js-aid="jobID"]'))
                    )

        for job in jobs:
             print(job.text)

        next_button = WebDriverWait(driver, 100).until(
                     EC.visibility_of_element_located((By.CSS_SELECTOR, ".pagination-next a"))
             )
                # Click the "Next" button
        driver.execute_script("arguments[0].click();",next_button)

        time.sleep(5)  # Adjust sleep time as needed


driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from etl.extractor import Extractor
from etl.transformer import Transformer
from etl.csv_loader import CSVLoader

def main():
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


    extractor = Extractor(driver)
    transformer = Transformer()
    loader = CSVLoader('data/jobs_data.csv')

    # Extract:
    job_data = []
    job_data = extractor.extract_job_data(website_url)

    # Transform:
    transformed_data = []  # Initialize it here to ensure it's always available
    for job in job_data:
        transformed_job = transformer.transform(job)
        print(transformed_job)
        transformed_data.append(transformed_job)

    #print(transformed_data)

    # Load:
    valid_data = [record for record in transformed_data if record]  # Filter out empty dictionaries
    loader.load(valid_data)

if __name__ == "__main__":
    main()

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


class Extractor:
    def __init__(self, driver):
        self.driver = driver

    def extract_job_data(self, url):
        self.driver.get(url)
        all_jobs = []

        try:
            # Wait for the "Past 24 hours" filter to be visible
            past_24_hours = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.XPATH, '//a[@data-automation-id="Past-24-hours"]'))
            )

            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", past_24_hours)
            time.sleep(1)  # Wait for the scroll to complete

            # Click the element using JavaScript
            self.driver.execute_script("arguments[0].click();", past_24_hours)
        except Exception as e:
            print("Error clicking 'Past 24 hours':", e)
            self.driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging
            self.driver.quit()
            exit()

        cookie_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))  # Adjust XPath as needed
        )
        cookie_button.click()

        while True:
            jobs = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//a[@data-js-aid="jobID"]'))
            )

            for i in range(len(jobs)):  # len(jobs)):
                job = WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//a[@data-js-aid="jobID"]'))
                )

                # Click the job post
                self.driver.execute_script("arguments[0].click();", job[i])

                location = WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//div//a[@class = "t-mute"]//span'))
                )
                company_name = WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@class="t-nowrap t-small p10l"]//b'))
                )
                employment_info = self.driver.find_elements(By.XPATH, '//div[@class="t-small u-stretch"]')

                job_url = self.driver.current_url

                try:
                    salary_element = self.driver.find_element(By.XPATH,
                                                              '//i[@class="icon t-small is-salary"]/following-sibling::div')
                    salary = salary_element.text.strip()
                except NoSuchElementException:
                    salary = None

                # Safely access elements in employment_info
                if len(employment_info) >= 2:
                    company_info = employment_info[-1].text
                    employment_type = employment_info[-2].text
                elif len(employment_info) == 1:
                    company_info = employment_info[0].text
                    employment_type = None  # Or provide some default value
                else:
                    company_info = None
                    employment_type = None

                job_details = {
                    'job_title': job[i].text,
                    'country': location[1].text if len(location) > 1 else location[0].text if len(location) > 0 else 'Unknown',
                    'city': location[0].text if len(location) > 1 else None,
                    'salary': salary,
                    'company': company_name.text,
                    'company_info': company_info,
                    'employment_type': employment_type,
                    'job_url': job_url
                }
                all_jobs.append(job_details)
                print(job_details)


                # Close the job view
                WebDriverWait(self.driver, 100).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "icon.is-times.has-pointer.t-mute.m0"))
                ).click()
            #break
        #self.driver.quit()
        #return all_jobs




            try:
                next_button = WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".pagination-next a"))
                )
                # Move to the next page
                self.driver.execute_script("arguments[0].click();", next_button)

                time.sleep(3)

            except Exception as e:
                print("No more pages available", e)
                break  # Exit the loop when no more pages are available

        self.driver.quit()
        return all_jobs




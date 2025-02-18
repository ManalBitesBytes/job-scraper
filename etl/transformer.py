import re


class Transformer:
    def __init__(self):
        pass

    def parse_job_id(self, job_url):
        """Extracts the jobId from the URL."""
        if not job_url or not isinstance(job_url, str):
            return None  # Skip if the URL is invalid or None

        # Use regular expression to find the jobId pattern in the URL string
        match = re.search(r'jobId=(\d+)', job_url)
        if match:
            print(match.group(1))
            return match.group(1)  # Return the jobId if found
        return None  # Return None if no jobId is found

    def parse_company_info(self, company_info):
        """Splits company_info into company size and industry."""
        if company_info:
            parts = company_info.split(' · ')
            if len(parts) == 2:
                company_size = parts[0]
                industry = parts[1]
                print(company_size, industry)
                return company_size, industry
        return None, None

    def parse_employment_type(self, employment_type):
        """Categorizes the employment type."""
        employment_type = employment_type.lower()
        if 'full time' in employment_type:
                return 'Full Time'
        elif 'contract' in employment_type:
                return 'Contractor'
        elif 'part time' in employment_type:
                return 'Part Time'
        elif 'temporary' in employment_type:
                return 'Temporary'

    def clean_job_title(self, job_title):
        """Cleans the job title by removing any '-' and text after it."""
        if job_title:
            # Check if there's a dash in the title and split if found
            if "-" in job_title:
                cleaned_title = job_title.split('-')[0]
            else:
                cleaned_title = job_title

            print(f"Cleaned job title: {cleaned_title}")  # Debug print
            return cleaned_title
        return None

    def process_salary(self, salary):
        if salary:
            if ' - ' in salary:  # Salary is a range
                salary_min, salary_max = map(lambda x: float(x.replace('$', '').replace(',', '')),
                                             salary.split(' - '))
                return salary_min, salary_max
            else:  # Single salary amount (not a range)
                salary_value = float(salary.replace('$', '').replace(',', ''))
                return salary_value, salary_value
        return None, None  # In case salary is None or invalid

    def transform(self, record):
        if not record.get('job_title'):  # Skip records with no job title
            return None
        """Applies all transformations and returns a cleaned dictionary."""
        job_url = record.get('job_url')
        job_id = self.parse_job_id(job_url)
        job_title = record.get('job_title')
        job_title = self.clean_job_title(job_title)

        company_info = record.get('company_info')
        company_size, industry = self.parse_company_info(company_info)

        employment_type = record.get('employment_type')
        employment_type = self.parse_employment_type(employment_type)

        # Process salary
        salary_max, salary_min = self.process_salary(record.get('salary'))

        transformed_data = {
            'job_title': job_title,
            'country': record.get('Country'),
            'city': record.get('city'),
            'salary_max': salary_max,
            'salary_min': salary_min,
            'company': record.get('company'),
            'company_size': company_size,
            'industry': industry,
            'employment_type': employment_type,
            'job_url': job_url,
            'job_id': job_id
        }
        return transformed_data

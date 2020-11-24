# Use requests and lxml packages to extract information from http://econpy.pythonanywhere.com/ex/001.html
# And save the data into a local CSV file
from lxml import html
from bs4 import BeautifulSoup
import requests
import csv
import time
import random
from datetime import date, timedelta
import re


class Indeed:
    def __init__(self, start_url, file_name):
        self.start_url = start_url
        self.current_last_key = ' '  # The job_id of last job scraped in current page
        self.previous_page_keys = []  # The job_id of last job scraped in previous page
        self.file_name = file_name

    def get_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def parse_page(self, page):
        soup = BeautifulSoup(page, 'lxml', multi_valued_attributes=None)
        titles = soup.find_all('h2', class_="title")
        print(len(titles))
        job_info = []
        for title in titles:
            # if title.parent.find(class_='date ').string in ['Just posted', 'Today']:
            job = title.parent
            job_info.append(self.extract_job_info(job))
        # Save the scraped list into CSV row by row.
        return job_info

    def extract_job_content(self, url):
        soup = BeautifulSoup(self.get_page(url), 'lxml',
                             multi_valued_attributes=None)
        job_content = soup.find('div', id="jobDescriptionText").text
        return job_content

    def extract_job_info(self, job):
        # job_url = 'https://www.indeed.com' + \
        #     job.find('h2', class_='title').a['href']

        try:
            job_id = self.get_id(job)  # job.find('h2', class_='title').a['id']
        except:
            job_id = 'NA'

        # try:
        #     job_url = 'https://www.indeed.com' + \
        #         job.find('h2', class_='title').a['href']
        # except:
        #     job_url = 'NA'

        if job_id != 'NA':
            job_url = f'https://www.indeed.com/viewjob?&jk={job_id}'
        try:
            title = job.find('a', attrs={
                'data-tn-element': 'jobTitle'}).text.strip()
        except:
            title = 'NA'
        try:
            job_is_new = job.find(class_='new').text.strip()
        except:
            job_is_new = "NA"
        try:
            company = job.find(class_='company').text.strip()
        except:
            company = "NA"
        # company rating out of 5
        try:
            company_rating = job.find(class_='ratingsContent').text.strip()
        except:
            company_rating = '-1'
        try:
            location = job.find(
                class_='location accessible-contrast-color-location').text.strip()
        except:
            location = 'NA'
        # Remote work is available.
        try:
            job_is_remote = job.find(class_='remote').text.strip()
        except:
            job_is_remote = 'NA'
        # Extract salary infomation
        try:
            salary = job.find(class_='salaryText').text.strip()
        except:
            salary = 'NA'
        try:
            job_post_date = job.find(class_='date ').text
            job_post_date = self.str_to_date(job_post_date)
        except:
            job_post_date = "NA"
        job_content = self.extract_job_content(job_url)
        job_info = {
            'job_id': job_id,
            'job_url': job_url,
            'title': title,
            'job_is_new': job_is_new,
            'company': company,
            'company_rating': company_rating,
            'location': location,
            'job_is_remote': job_is_remote,
            'salary': salary,
            'job_post_date': job_post_date,
            'job_content': job_content}
        print({
            'job_id': job_id,
            # 'job_url': job_url,
            # 'title': title,
            # 'job_is_new': job_is_new,
            # 'company': company,
            # 'company_rating': company_rating,
            # 'location': location,
            # 'job_is_remote': job_is_remote,
            # 'salary': salary,
            'job_post_date': job_post_date,
            # 'job_content': job_content
        })
        return job_info

    def get_id(self, job):
        job_id = job.find(
            'a', attrs={"title": "Save this job to my.indeed"})['id']
        return job_id.split('_')[1]

    def str_to_date(self, str):
        if str in ['Just posted', 'Today']:
            today = date.today()
            return today
        else:
            num_day_ago = re.findall('^(\d+).*?ago', str, re.S)
            return date.today()-timedelta(int(num_day_ago[0]))

    def scrape_page(self, page_start_num):
        url = self.start_url + str(page_start_num)
        html = self.get_page(url)
        print(url)
        job_info = self.parse_page(page=html)
        return job_info

    def write_to_csv(self, data):
        with open(self.file_name, 'w', newline='', encoding='utf8') as csv_file:
            fieldnames = ['job_id',
                          'job_url',
                          'title',
                          'job_is_new',
                          'company',
                          'company_rating',
                          'location',
                          'job_is_remote',
                          'salary',
                          'job_post_date',
                          'job_content']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerows(data)

    def init_csv_file(self):
        with open(self.file_name, 'w', newline='', encoding='utf8') as csv_file:
            fieldnames = ['job_id',
                          'job_url',
                          'title',
                          'job_is_new',
                          'company',
                          'company_rating',
                          'location',
                          'job_is_remote',
                          'salary',
                          'job_post_date',
                          'job_content']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def main(self):
        self.init_csv_file()
        for i in range(0, 110, 10):
            # if the last job_id is already in saved saved_job_ids list, skip the saving part and break.
            jobs = self.scrape_page(i)
            self.current_last_key = jobs[len(jobs)-1]['job_id']
            if self.current_last_key in self.previous_page_keys:
                break
            else:
                print('-'*20 + f"Job post number {i} started:" + '---'*20)
                # write scrape jobs from current page to local csv file
                self.write_to_csv(jobs)
                # update the job_id of the just scraped page
                for job in jobs:
                    self.previous_page_keys.append(job['job_id'])
                time.sleep(random.uniform(0, 3))


start_url = 'https://www.indeed.com/jobs?q=python+%22machine+learning%22&sort=date&radius=25&start='
indeed = Indeed(start_url, './indeed_data_jobs.csv')
indeed.main()

# Use requests and lxml packages to extract information from http://econpy.pythonanywhere.com/ex/001.html
# And save the data into a local CSV file
from lxml import html
from bs4 import BeautifulSoup
import requests
import csv
import pymysql
import os
import time
from datetime import date, timedelta
import re


def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_result(page):
    soup = BeautifulSoup(page, 'lxml', multi_valued_attributes=None)
    titles = soup.find_all('h2', class_="title")
    print(len(titles))
    global total
    total += len(titles)
    jobs = []
    for title in titles:
        # if title.parent.find(class_='date ').string in ['Just posted', 'Today']:
        job = title.parent
        try:
            job_url = 'https://www.indeed.com' + \
                job.find('h2', class_='title').a['href']
        except:
            job_url = 'NA'
        try:
            job_is_new = job.find(class_='new').text
        except:
            job_is_new = "NA"
        try:
            company = job.find(class_='company').text
        except:
            company = "NA"
        # company rating out of 5
        try:
            company_rating = job.find(class_='ratingsContent').text
        except:
            company_rating = '-1'
        try:
            location = job.find(
                class_='location accessible-contrast-color-location').text
        except:
            location = 'NA'
        # Remote work is available.
        try:
            job_is_remote = job.find(class_='remote').string
        except:
            job_is_remote = 'NA'
        # Extract salary infomation
        try:
            salary = job.find(class_='salaryText').string
        except:
            salary = 'NA'
        try:
            job_post_date = job.find(class_='date ').string
            job_post_date = str_to_date(job_post_date)
        except:
            job_post_date = "NA"
        # collect the job details into tuple and append the the job list.
        jobs.append((job_url, job_is_new, company, company_rating,
                     location, job_is_remote, salary, job_post_date))
    return jobs


def extract_loc(text):
    x = re.findall(r".+?\W([A-Z]{1}.+?[A-Z]{2})", text, re.S)
    if x is None:
        return text
    else:
        return x[0]


def str_to_date(str):
    if str in ['Just posted', 'Today']:
        today = date.today()
        return today
    else:
        num_day_ago = re.findall('^(\d+).*?ago', str, re.S)
        return date.today()-timedelta(int(num_day_ago[0]))


def save_to_cloud_sql(db, job_record):
    cursor = db.cursor()
    sql = """INSERT INTO jobs(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    recordTuple = job_record
    cursor.executemany(sql, recordTuple)


def scrape_page(html):
    if html:
        items = parse_result(page=html)  # 解析过滤我们想要的信息
        save_to_cloud_sql(db, items)
    else:
        print("no html page returned")


# db_user = os.environ.get("DB_USER")
# db_pass = os.environ.get("DB_PASS")
# db_name = os.environ.get("DB_NAME")
# db_host = os.environ.get("DB_HOST")
# db = pymysql.connect(db_host, db_user, db_pass, db_name)
START_LINK = 'https://www.indeed.com/jobs?q=python+%22machine+learning%22&sort=date&radius=25&start='
total = 0
for i in range(23500, 2000000000, 50):
    url = START_LINK + str(i)
    print('-'*20 + f"Job post page number {i} started:" + '---'*20)
    html = get_page(url)
    if html:
        db = pymysql.connect("34.72.236.137", "root",
                             "Zhui85feng", "jobs_indeed")
        scrape_page(html)
        print(f'{total} jobs have been scraped!')
        # Save the data for scraped page.
        time.sleep(1)
        db.commit()
        db.close()
    else:
        break

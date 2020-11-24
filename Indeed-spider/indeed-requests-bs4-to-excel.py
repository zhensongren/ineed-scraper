# Use requests and lxml packages to extract information from http://econpy.pythonanywhere.com/ex/001.html
# And save the data into a local CSV file
from lxml import html
from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

def get_page(url):
    page = requests.get(url)
    return page

def get_info(page):
    soup = BeautifulSoup(page.text, 'lxml', multi_valued_attributes=None)
    titles = soup.find_all('h2', class_="title")
    print(len(titles))

    for title in titles:
        job = title.parent
        job_url = 'https://www.indeed.com' + job.find('h2', class_='title').a['href']
        job_is_new = job.find(class_='new').text
        company = job.find(class_='company').text
        #company rating out of 5
        try:
            company_rating = job.find(class_='ratingsContent').text
        except:
            company_rating = '-1'
        location = job.find(class_ = 'location accessible-contrast-color-location').text
        #Remote work is available.
        try:
            job_is_remote = job.find(class_='remote').string
        except:
            job_is_remote = 'NA'
        # Extract salary infomation
        try:
            salary = job.find(class_='salaryText').string
        except:
            salary = 'NA'
        job_post_date = job.find(class_='date ').string
        print(job_post_date)
        ws.append([job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date])

wb = Workbook()
ws = wb.active

START_LINK = 'https://www.indeed.com/jobs?q=title%3A((data+engineer)+or+(data+scientist))&radius=25&sort=date&limit=50&start='
   
for i in range(15, 20, 15):
    print('-'*20+ f"Job post number {i} started:" + '---'*20)
    link = START_LINK + str(i)
    r = get_page(link)
    get_info(r)

wb.save("indeed_jobs.xlsx")




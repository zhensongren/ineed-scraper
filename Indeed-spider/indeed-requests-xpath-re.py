# Use requests and lxml packages to extract information from http://econpy.pythonanywhere.com/ex/001.html
# And save the data into a local CSV file
import re, json
from lxml import html
from bs4 import BeautifulSoup
import requests
import csv
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
	'Referer': 'https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start=10',
	'Cookie': '_ga=GA1.2.1222789966.1535530525; pgv_pvi=8193187840; pgv_si=s2985358336; PHPSESSID=22e3m8aknd19s1gqkh0i9eisk0; Hm_lvt_0bd5902d44e80b78cb1cd01ca0e85f4a=1536726429,1536908218,1537154694,1537166987; Hm_lpvt_0bd5902d44e80b78cb1cd01ca0e85f4a=1537167106'
}
START_LINK = 'https://www.indeed.com/jobs?q=title%3A((data+engineer)+or+(data+scientist))&radius=25&sort=date&limit=50&start='

def get_page(url=START_LINK):
    page = requests.get(url, headers=HEADERS)
    return page

def get_info(page):
    items = parse_result(page.text)
    for item in items:
        print('开始写入数据 ====> ' + str(item))
        with open('book.txt', 'a', encoding='UTF-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    path = {}
    path['job_post_date'] = "//*[@class='date ']/text()"
    path['job_is_new'] = "//span[contains(text(), 'new') and @class='new']"
    path['job_post_link'] = "//*[contains(@id,'jl_') or @data-tn-element='jobTitle' or class='jobtitle turnstileLink ']/@href"
    path['company'] = "//*[@class='company']"
    path['rating'] = "//*[contains(@class, 'ratingsContent')]"
    path['location'] = "//*[contains(@class, 'location')]"
    path['salary'] = "//*[contains(text(), '$') and contains(@class, 'salary')]"
    path['job_is_remote'] = "//span[contains(text(), 'Remote') and @class='remote']/text()"

    
    tree = html.fromstring(page.content)
    job_url = tree.xpath(path['job_post_link'])
    job_post_date = tree.xpath(path['job_post_date'])
    job_is_remote = tree.xpath(path['job_is_remote'])

    # print( 'number of pages: ', len(job_url))
    # print( 'job_post_date: ', job_post_date)

    # Save the scraped list into CSV row by row.
    # with open('employee_file2.csv', mode='w') as csv_file:

        
    #     fieldnames = ['job_post_date', 'job_url', 'job_is_remote']
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for i in range(len(job_post_date)):
    #         writer.writerow({'job_post_date': job_post_date[i], 'job_url': job_url[i], 'job_is_remote': job_is_remote[i]})

def parse_result(html):
    # pattern = re.compile(
    #     '<h2 class="title">.*?href="(.*?)".*?<span class="new">(.*?)</span>.*?class="company">.*?(.*?)</a>.*?class="ratingsContent">(\d+).*?class="location accessible-contrast-color-location">(.*?)</div>.*?class="salaryText">(.*?)</span>.*?class="date ">(.*?)</span>',
    #     re.S)
    print('start to parse result')
    # pattern = re.compile('<h2 class="title">.*?href="(.*?)"', re.S)
    items = re.findall('class="ratingsContent">(\d+).*?class="location accessible', html, re.S)

    for item in items:
        yield {
            'job_url': item[0]
            # ,
            # 'job_is_new': item[1],
            # 'company': item[2],
            # 'company_rating': item[3],
            # 'location': item[4],
            # 'job_is_remote': item[5],
            # 'salary': item[6],
            # 'job_post_date': item[7]
        }
    print('got the data')

for i in range(0,30, 15):
    print(f"Job post number {i} started:")
    link = START_LINK + str(i)
    get_info(get_page(url=link))
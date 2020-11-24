# Connect to Cloud sql and test dummy data.
import pymysql

db = pymysql.connect("34.72.236.137", "root", "Zhui85feng", "jobs_indeed")
cursor = db.cursor()

# Test dummy data
job_url = 'test'
job_is_new = 'test'
company = 'test'
company_rating = 'test'
location = 'test'
job_is_remote = 'test'
salary = 'test'
job_post_date = 'test'

# # Creat table
sql = """create table if not exists jobs (
                           id int(100) unsigned NOT NULL AUTO_INCREMENT,
                           job_url text not null,
                           job_is_new char(200) not null,
                           company char(200) not null,
                           company_rating char(200) not null,
                           location char(200) not null,
                           job_is_remote char(200) not null,
                           salary char(200) not null,
                           job_post_date char(200) not null,
                           PRIMARY KEY (id))"""

cursor.execute(sql)

# Insert with pre-defined sql query and record tuple.
sql = """INSERT INTO jobs(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
recordTuple = (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date)
cursor.execute(sql, recordTuple)                          


# Insert record values directly
cursor.execute("""
INSERT INTO jobs(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date) \
                    VALUES ("1","1","1","1","1","1","1","1")""")  


# Insert with place holder and sql command together.     
cursor.execute("""
INSERT INTO jobs(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date) \
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
                    %
                    (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date))   

# Insert many rows with pre-defined sql query and record tuples.
sql = """INSERT INTO jobs(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
recordTuples = [(job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date),
               (job_url, job_is_new, company, company_rating, location, job_is_remote, salary, job_post_date)
               ]
cursor.executemany(sql, recordTuples)

db.commit()
db.close()
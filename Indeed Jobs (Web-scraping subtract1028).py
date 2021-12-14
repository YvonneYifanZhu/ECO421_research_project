import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract(page):
    url = f'https://ca.indeed.com/jobs?q=Finance&l=Ontario&start={page}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        if_new = item.find('span').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()

        try:
            salary = item.find('div', class_="salary-snippet").text.strip()
        except:
            salary = 'not being posted'

        summary = item.find('div', class_='job-snippet').text.strip()
        posted_date = item.find('span', class_='date').text.strip()

        job = {'new': if_new,
                'company': company,
                'location': location,
                'salary': salary,
                'summary': summary,
                'posted_date': posted_date
        }

        joblist.append(job)
    return


def get_job_title(soup):

    for tage in soup.select(".resultContent span[title]"):
         title = tage.text
         job_title.append(title)

    return


def get_dataframe(df1, df2):

    df1_df = pd.DataFrame(df1)
    df2_df = pd.DataFrame(df2)
    df12 = df1_df.join(df2_df)

    return df12


job_title = []
joblist = []

for num_i in range(400, 420):
    soup_i = extract(num_i)
    transform(soup_i)
    get_job_title(soup_i)
    merged_i = get_dataframe(job_title, joblist)


# the path should be changed to your own, and the name of the csv.file
merged_i.to_csv('/Users/yvonne_zhu/Desktop/ECO421_research project/Data/test.csv')

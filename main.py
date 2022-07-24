import os
import json
from typing import List, Dict, Any

import pandas as pd
import requests
from bs4 import BeautifulSoup

total_pages = []
url = 'https://id.indeed.com/jobs?q=web%20developer&l=Indonesia&from: searchOnHP'
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
site = 'https://id.indeed.com/'


def get_total_pages(query, location):
    paramms = {'q': query, 'l': location, 'from': 'searchOnHP'}

    req = requests.get(url, params=paramms, headers=head)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(req.text)
        outfile.close()

    sp1 = BeautifulSoup(req.text, 'html.parser')
    pagination = sp1.find('ul', 'pagination-list')
    pages = pagination.find_all('li')

    for i in pages:
        total_pages.append(i.text)

    total = int(max(total_pages))
    return total


def get_all_items(query, location, start, page):
    paramms = {'q': query, 'l': location, 'start': start, 'from': 'searchOnHP'}

    req = requests.get(url, params=paramms, headers=head)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(req.text)
        outfile.close()

    sp2 = BeautifulSoup(req.text, 'html.parser')
    content = sp2.find_all('div', 'job_seen_beacon')

    job_list = []

    for item in content:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName').text
        location = item.find('div', 'companyLocation').text

        data_dict = {
            'Title': title,
            'Company': company,
            'location': location
        }
        job_list.append(data_dict)

    # writing json file
    try:
        os.mkdir('json_file')
    except FileExistsError:
        pass

    with open(f'json_file/{query} in {location} page {page}.json', 'w+') as json_data:
        json.dump(job_list, json_data)
    print('Json created')
    return job_list

def document(dataFrame, filename):

    try:
        os.mkdir('data')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data/{filename}.csv', index=False)
    df.to_excel(f'data/{filename}.xlsx', index=False)
    print('Data created succes')

def run():
    query = input('Enter your jobs : ')
    location = input('Enter your location : ')

    total = get_total_pages(query, location)
    count = 0
    final = []

    for page in range(total):
        page += 1
        count += 10
        final += get_all_items(query, location, count, page)

    # formating data
    try:
        os.mkdir('final')
    except FileExistsError:
        pass
    with open('final/{}.json'.format(query), 'w+') as final_data:
        json.dump(final, final_data)
    print('Data json succesfuly')

    document(final, query)




if __name__ == '__main__':
    print(run())

import json
import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime

start = datetime.datetime.now()

url = "https://v-tylu.work/en"
page = 1
response = requests.get(url, params={"transaction_type": "offering-with-online-payment", "page": page})

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("h2", {"class": "home-list-title"})

jobs = []
result = []

while len(titles) > 0:
    for title in titles:
        job_id = re.findall(r"\d+", title.find_next("a").get("href"))[0]
        jobs.append(job_id)

    json_body = {"ids": jobs, "language": "uk"}

    listings_url = "https://listing-service.v-tylu.com/work/listings"
    listings_response = requests.post(listings_url, json=json_body)

    result += json.loads(listings_response.text)

    page += 1
    response = requests.get(url, params={"transaction_type": "offering-with-online-payment", "page": page})
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all("h2", {"class": "home-list-title"})


with open("resumes.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    count = 0
    for r in result:
        if count == 0:
            writer.writerow(r.keys())
            count += 1
        writer.writerow(r.values())

print(datetime.datetime.now() - start)

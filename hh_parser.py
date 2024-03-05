import json

import requests
from bs4 import BeautifulSoup

url = "https://spb.hh.ru/search/vacancy?text=python,django,flask&area=1&area=2"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Content-Type": "text/html; charset=utf-8",
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text.replace("\u202f", " ").replace("\xa0", " "), 'lxml')

vacancies = soup.find_all("div", attrs={
    'class': "serp-item serp-item_link"
})
data = []
for vacancy in vacancies:
    try:
        fork_salary = vacancy.find('span', attrs={"class": "bloko-header-section-2"}).text
    except AttributeError:
        fork_salary = None
    data.append({
        'link': vacancy.find('a', attrs={"class": "bloko-link"})['href'],
        'fork_salary': fork_salary,
        'company_name': vacancy.find('a', attrs={"class": "bloko-link bloko-link_kind-tertiary"}).text,
        'city': vacancy.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"}).text,
    })

with open("data.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(data, indent=4, ensure_ascii=False))
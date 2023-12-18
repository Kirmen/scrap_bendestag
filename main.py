from typing import List

import requests
from bs4 import BeautifulSoup
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.19987.120'
}


def find_hrefs() -> None:
    hrefs = []
    for i in range(0, 745, 12):
        url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'
        q = requests.get(url, headers=headers)
        res = q.content

        soup = BeautifulSoup(res, 'lxml')
        divs = soup.find_all('div', class_='col-xs-4')
        for y in divs:
            a = y.find('a')
            href = a.get('href')
            hrefs.append(href)

    with open('list_of_the_members.txt', 'a') as file:
        for member in hrefs:
            file.write(f'{member}\n')


def to_json(all_members: List):
    with open('data.json', 'w') as file:
        json.dump(all_members, file, indent=4)


def scrap_all_members_to_file():
    with open('list_of_the_members.txt', 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    all_members1 = []
    c=1
    for line in lines:
        q = requests.get(line, headers=headers)
        # print(q)
        res = q.content

        soup = BeautifulSoup(res, 'lxml')
        person = soup.find('div', class_='bt-biografie-name').find('h3').text
        person_name_party = person.split(',')
        person_name = person_name_party[0].strip()
        person_party = person_name_party[1].strip()
        soc_networks = soup.find(class_='bt-linkliste').find_all(class_='bt-link-extern')
        social_networks = []
        for i in soc_networks:
            social_networks.append(i.get('href'))

        data = {
            'name': person_name,
            'party': person_party,
            'social networks': social_networks
        }
        all_members1.append(data)
        # print(c)
        c+=1

    to_json(all_members=all_members1)


def main():
    find_hrefs()
    scrap_all_members_to_file()




if __name__ == '__main__':
    main()

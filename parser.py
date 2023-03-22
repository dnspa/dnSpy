import requests
from bs4 import BeautifulSoup


class ObjktParser(object):
    def __init__(self):
        self.page = 0
        self.counter = 0
        self.limit = int(input('Количество профилей: '))
        self.minimal = int(input('Минимальный баланс кошелька: '))
        self.filtering = int(input(
            'Укажите фильтр (1 - Newest | 2 - Recently Listed | 3 - Price: High to Low | 4 - Price: Low to High): '))

        if self.filtering == 1:
            self.filtering = "sort=timestamp:desc"
        elif self.filtering == 2:
            self.filtering = "sort=last_listed:desc"
        elif self.filtering == 3:
            self.filtering = "sort=lowest_ask:desc"
        elif self.filtering == 4:
            self.filtering = "sort=lowest_ask:asc"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36 '}

        self.work()

    def work(self):
        print('Начинаю работу...')
        profiles = []
        with open('result.txt', 'w', encoding='utf-8') as output:
            while self.counter < self.limit:
                self.page += 1
                url = f"https://objkt.com/explore/tokens/{self.page}?{self.filtering}"
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                for profile in soup.select(
                        "app-objkt-gallery-element div div:nth-of-type(1) div:nth-of-type(3) app-info-popover span a"):
                    href = profile.get('href')
                    if href not in profiles:
                        profiles.append(href)
                        response = requests.get(f"https://api.tzkt.io/v1/accounts/{href[26:]}", headers=self.headers)
                        accounts = response.json()
                        balance = accounts['balance']
                        metadata = accounts.get('metadata')
                        if metadata and metadata.get('twitter') and balance > (self.minimal * 1000000):
                            twitter = f"https://twitter.com/{metadata['twitter']}"
                            output.write(f'{href} | {balance / 1000000} | {twitter}\n')
                            print(f'[{self.counter} / {self.limit}] {href} | {balance / 1000000} | {twitter}')
                            self.counter += 1


if __name__ == "__main__":
    parser = ObjktParser()

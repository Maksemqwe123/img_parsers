from bs4 import BeautifulSoup
import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72',
}

items_restaurant = []
urls_restaurant = []
spend_genre = []
address_restaurant = []


class ParserRestaurant:
    def __init__(self, name: list):
        self.name = name
        self.items_restaurant = items_restaurant
        self.urls_restaurant = urls_restaurant
        self.address_restaurant = address_restaurant

        self._get_html()

    def _get_html(self):
        url = f'https://www.relax.by/cat/ent/restorans/{self.name[0]}/'

        response = requests.get(url=url, headers=headers)

        try:
            assert response.status_code == 200
            html_source = response.text
            self._get_info(html_source)
        except AssertionError as e:
            print(f'ERROR: {repr(e)}')
            print(response.status_code)

    def _get_info(self, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')

        restaurants = pages_info.find_all('a', class_='Place__headerLink Place__title Link')
        for name in restaurants:
            self.urls_restaurant.append(name.get('href'))
            self.items_restaurant.append(name.text)

        restaurants_address = pages_info.find_all('span', class_='Place__address Place__contentSub Place__address--clickable Place__address--hasNotDistance Link')
        for address in restaurants_address:
            self.address_restaurant.append(address.text)

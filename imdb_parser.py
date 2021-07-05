# imdb parser

import datetime
import requests
from bs4 import BeautifulSoup

current_year = datetime.datetime.now().year

imdb_link = 'https://www.imdb.com'
imdb_search_link = 'https://www.imdb.com/find?'


class Actor(object):
    def __init__(self, link, name='default'):
        self.fulfilled = False
        self.link = link
        self.name = name
        self.birth = None
        self.death = None
        self.age = None
        self.movies = []

    def fillData(self):
        if self.fulfilled is True:
            return self

        actor_html = requests.get(self.link).text
        soup = BeautifulSoup(actor_html, 'html.parser')
        self.name = soup.find('span', class_='itemprop').text
        self.birth = soup.find('div', id='name-born-info').find('time').get('datetime')

        try:
            self.death = soup.find('div', id='name-death-info').find('time').get('datetime')
        except Exception:
            self.death = 'Alive'
        movie_soup = soup.find('div', class_='filmo-category-section')
        movies_raw = movie_soup.find_all('b')

        for one_movie in movies_raw:
            movie_a_tags = one_movie.find('a')
            movie_name = movie_a_tags.text
            self.movies.append(movie_name)

        self.age = (current_year - int(self.birth[:4]) - 1)
        self.fulfilled = True
        return self


class Movie(object):
    def __init__(self, link, name='default'):
        self.fulfilled = False
        self.link = link
        self.name = name
        self.rating = None
        self.runtime = None
        self.genre = None
        self.date_released = None
        self.director = None
        self.writer = None
        self.leadlist = []
        self.cast = []
        self.budget = None
        self.storyline = None

    def __str__(self):
        return self.name

    def fillData(self):
        if self.fulfilled is True:
            return self

        movie_html = requests.get(self.link).text
        soup = BeautifulSoup(movie_html, 'html.parser')

        self.name = soup.find('h1').text
        self.date_released = soup.find('span', id='titleYear').text
        self.rating = soup.find("span", itemprop="ratingValue").text
        self.director = soup.find("div", class_="credit_summary_item").find("a").text
        self.writer = soup.find("div", class_="credit_summary_item").findNext("a").findNext("a").text
        self.genre = soup.find("div", class_="see-more inline canwrap").findNext("div",
                                                                                 class_="see-more inline canwrap").findNext(
            "a").text

        # budget bulunmasi

        for i in soup.find_all("h4"):
            if "Budget:" in i:
                self.budget = i.next_sibling.strip()

        # runtime bulunmasi
        for i in soup.findAll('time'):
            if i.has_attr('datetime'):
                self.runtime = i.text

        # filmin starlari
        leads = soup.find("div", class_="credit_summary_item").findNext("div", class_="credit_summary_item").findNext(
            "div", class_="credit_summary_item").find_all("a")
        leadlist = []
        for k in leads:
            leadlist.append(k.text)
        self.leadlist = leadlist[:-1]

        # cast olusturulmasinda actor objesi olarak tutmustuk onun yerine simdi isim bilgilerini tutuyoruz
        cast_soup = soup.find("table", class_="cast_list")
        cast_raw = cast_soup.find_all("tr", class_=["odd", "even"])
        casts = []
        for act in cast_raw:
            actors = act.find("td", class_="").find("a")
            act_name = actors.text
            # actor_object = Actor(act_name)
            casts.append(act_name)
            self.cast.append(act_name)

        storyline = soup.find("div", class_="inline canwrap").find("p").find("span").text
        self.storyline = storyline
        self.fulfilled = True
        return self


def search_imdb(any_name):
    any_name = any_name.replace(' ', '+')
    my_url = imdb_search_link + "q=" + any_name
    # get func requests objesi dönderir
    imdb = requests.get(my_url)
    imdb_html = imdb.text
    # BS objesi yaratırken ikinci parametre sabit
    soup = BeautifulSoup(imdb_html, 'html.parser')
    # table name tagine sahip ve class adı findList olan HTML içeriğinin altındaki kodlar için işlem yapmamızı sağlıyor
    find_table = soup.find('table', {"class": "findList"})
    # find table içindeki tr tagine sahip kodları bulup onun da altındaki td taginin result_text classına sahip ve onun altındaki linkleri ("a") sağlıyor
    first_search_result = find_table.find('tr').find('td', {"class": "result_text"}).find('a')
    # En son bulunan linkdeki href kısmının içindeki değeri bulunmasını sağlıyor
    first_search_result_link_raw = first_search_result.get('href')
    # href'in içindeki /title/............/ daki ........ ların indexini buluyor
    link_cutout_index = first_search_result_link_raw.find('/', 15)
    # ana link içerisindeki film için id kısmını çevirir
    first_search_result_link = first_search_result_link_raw[:link_cutout_index]
    # imdb ana sitesi ile istenen filmin id'si birleştirilir
    return imdb_link + first_search_result_link




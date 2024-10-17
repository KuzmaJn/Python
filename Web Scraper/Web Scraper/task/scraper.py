import requests
import string
import os
from bs4 import BeautifulSoup


def get_soup(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print("Invalid URL! Error {}" .format(e))
        return 0
    
    if r.status_code == 200:
        return BeautifulSoup(r.text, "html.parser")
    else:
        print('Status Code {}'.format(r.status_code))
        return 0


def remove_punctuation(input_string):
    # Make a translator object to replace punctuation with none
    translator = str.maketrans('', '', string.punctuation)

    return input_string.translate(translator).lower().replace(' ', '_')


def search_for_type(soup, article_type):
    lst = []
    for article in soup.find_all('article'):
        if article.find('span', {'data-test':'article.type'}).text == article_type:
            lst.append(article)

    return lst


def create_folders(n):
    for i in range(n):
        os.mkdir('Page_{}'.format(i+1))


def find_text(soup):
    try:
        text = soup.find('p', {'class':'article__teaser'}).text
    except AttributeError:
        text = 'The article is available only by paid subscription.'

    return text


def get_articles_from_page(page_number, article_type):
    os.chdir('Page_{}'.format(page_number))

    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={}'.format(page_number)
    soup = get_soup(url)
    suitable_articles = search_for_type(soup, article_type)

    for article in suitable_articles:
        a_tag = article.find('a', {'data-track-action':'view article'})
        text = remove_punctuation(a_tag.text)

        file = open(text + '.txt', 'wb')
        article_link = 'https://www.nature.com/nature{}'.format(a_tag['href'])
        soup = get_soup(article_link)
        file.write(find_text(soup).encode('UTF-8'))

        file.close()

    os.chdir('..')


def get_all_pages(n, a_type):
    create_folders(n)

    for i in range(n):
        get_articles_from_page(i + 1, a_type)


def main():
    number_of_pages = int(input())
    a_type = input()
    get_all_pages(number_of_pages, a_type)


if __name__ == '__main__':
    main()


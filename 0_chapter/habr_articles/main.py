import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import re


url = "https://habr.com/ru/articles/top/daily/"



def get_url_html(url_path: str) -> str:
    response = requests.get(
        url_path,
        headers={
            "User-Agent": UserAgent().google,
        },
    )
    return response.text


def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, "lxml")


def fetch_article_text(url_path: str) -> str:
    page = get_url_html(url_path)
    soup = get_soup(page)

    article_text = soup.find("div", id="post-content-body").text
    return article_text.strip()


def get_habr_posts(soup: BeautifulSoup) -> list:
    articles = soup.find_all("article", class_="tm-articles-list__item")
    aritcle_links =  [x.find("a", class_= "tm-title__link") for x in articles]

    articles_info = []

    for article in articles:
        link_element = article.find("a", class_="tm-title__link")
        article_views = article.find("span", class_="tm-icon-counter__value").text
        article_link = "https://habr.com/" + link_element.get("href")[1:]

        articles_info.append(
            {
                "title": link_element.text,
                "link": article_link,
                "views": article_views,
                "content": fetch_article_text(article_link)[:50],
            }
        )

    return articles_info





def main():
    html = get_url_html(url)
    soup = get_soup(html)
    habr_posts = get_habr_posts(soup)

    pprint(habr_posts[0])


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
from os import get_terminal_size


res = ''

n = int(input("Enter the number of pages you want to scrap from hacker news website: "))

for i in range(1, n+1):
    res += requests.get(f"https://news.ycombinator.com/news?p={i}").text


parsed_html = BeautifulSoup(res, 'html.parser')
links = parsed_html.select(".storylink")
subtext = parsed_html.select(".subtext")


def popular_news(links, subtext):
    news_list = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if vote:
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                news_list.append(
                    {'title': title, 'link': href, 'votes': points})
    return sorted(news_list, key=lambda k: k['votes'], reverse=True)


news_list = popular_news(links, subtext)
width = get_terminal_size().columns

for index, news in enumerate(news_list):
    print(f" [News - {index+1}] ".center(width, "_"))
    print(f"Title: {news['title']}.")
    print(f"Link: {news['link']}")
    print(f"Up votes: {news['votes']}")
    print('\n')

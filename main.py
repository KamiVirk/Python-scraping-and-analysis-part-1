import csv
from typing import Text
from bs4 import BeautifulSoup
import requests
import pandas as pd

month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10 ', '11', '12']
info_dict = {}
for m in range(len(month)):
    base_url = "https://www.goodreads.com/book/popular_by_date/2021/"

    to_scrap = base_url + str(month[m])

    source = requests.get(to_scrap)
    print(f"Site{month[m]}'s link status : {source.status_code}")

    page_content = source.text

    doc = BeautifulSoup(page_content, "lxml")

    links = []
    for a_tag in doc.find_all('a', class_="BookCover BookCover--bottom"):
        links.append(a_tag.get('href'))


    author = []
    for span_tag in doc.find_all('span', class_="ContributorLink__name"):
        author.append(span_tag.text)

    rating = []
    for span_r in doc.find_all('span', class_="AverageRating__ratingValue"):
        rating.append(span_r.text)

    rating_count = []
    for span_r_count in doc.find_all('span', class_='Text Text__body3 Text__subdued'):
        r_count = span_r_count.text
        rating_count.append(r_count.split()[0])

    description = []
    for p_tag in doc.find_all("span", class_="Formatted"):
        description.append(p_tag.text.strip())

    list = []
    title = []
    for i in range(len(links)):
        source_2 = requests.get(links[i])
        print(f"Book{i}'s link status : {source_2.status_code}")
        page_content_2 = source_2.text
        doc_2 = BeautifulSoup(page_content_2, 'lxml')
        for h_tag in doc_2.find_all('h1', class_="gr-h1 gr-h1--serif"):
            title_ = h_tag.text.strip()
        title.append(title_)
        try:
            detail_tag = doc_2.find_all('div', class_="clearFloats")
            isb_tag = detail_tag[1].find('span', class_="greyText")
            isbn_ = (isb_tag.text.strip().split(':')[1])
            isbn = isbn_.rstrip(isbn_[-1])
        except Exception as e:
            isbn = "NOT AVAILABLE"
        list.append(isbn)

    info_dict = {
        'title': title,
        'author': author,
        'ISBN': list,
        'rating': rating,
        'rating count': rating_count,
        'url': links
    }
    df = pd.DataFrame(info_dict)
    df.to_csv("File4.csv", mode='a', index=False, header=None)
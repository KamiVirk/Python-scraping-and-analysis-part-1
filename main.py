import csv
from typing import Text
from bs4 import BeautifulSoup
import requests
import pandas as pd

month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10 ', '11', '12']

for m in range(len(month)):
    base_url = "https://www.goodreads.com/book/popular_by_date/2021/"

    to_scrap = base_url + str(month[m])

    source = requests.get(to_scrap)
    print(source.status_code)

    page_content = source.text

    doc = BeautifulSoup(page_content, "lxml")

    links = []
    for a_tag in doc.find_all('a', class_="BookCover BookCover--bottom"):
        links.append(a_tag.get('href'))

    title = []
    for h_tag in doc.find_all('h3', class_="Text Text__title3 Text__umber"):
        title.append(h_tag.text)

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
    for i in range(len(links)):
        source_2 = requests.get(links[i])
        page_content_2 = source_2.text
        doc_2 = BeautifulSoup(page_content_2, 'lxml')
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
    'description': description,
    'url': links

}

info_df = pd.DataFrame(info_dict)
info_df.to_csv('file4.csv', index=None)


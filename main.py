from bs4 import BeautifulSoup
import requests
import csv

WEBSITE_URL = "https://www.audible.in/adblbestsellers?ref=a_hp_t1_navTop_pl1cg0c1r0&pf_rd_p=1b60255c-ac96-4bc2-a0c8-6e6d0e32515d&pf_rd_r=8D16V7W1Q88012DP2JFY"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


response = requests.get(WEBSITE_URL, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    with open('audible_bestsellers.csv', 'w') as file:
        header = ['Title', 'Summary', 'Author', 'Narrator']
        writer = csv.writer(file)
        writer.writerow(header)
        articles = soup.select("#product-list-a11y-skiplink-target > span > ul > div > li")
        count = 0
        for article in articles:
            title_element = article.find_all('a')
            title = title_element[1].text if title_element is not None and len(title_element) > 1 else None
            summary_element = article.find('li', class_="subtitle")
            summary = summary_element.text.replace("\n","") if summary_element is not None else None
            author = article.find('li', class_="authorLabel").find('a').text.replace("\n","")
            narrator = article.find('li', class_="narratorLabel").find('a').text.replace("\n","")
            writer.writerow([title, summary, author, narrator])

else:
    raise ConnectionError
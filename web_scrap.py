#pip install selenium beautifulsoup4 requests pandas tqdm
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.headless = True
chrome_browser = webdriver.Chrome(options=chrome_options)

news_list_url='https://game.udn.com/game/cate/122088'
chrome_browser.get(news_list_url)
SCROLL_PAUSE_TIME = 2
last_height = chrome_browser.execute_script("return document.body.scrollHeight")
while True:
    chrome_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = chrome_browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 取得完整的頁面 HTML
html = chrome_browser.page_source
chrome_browser.quit()

soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all("a", class_="story-list__link")

review_data = []  # 存放心得評測的資料

for article in articles:
    slot = article.get("data-slotname")  # 取得 data-slotname 屬性
    url = article.get("href")             # 取得連結網址
    title = article.get("title")          # 取得標題
    if url and title and slot:
        if slot == "list_心得評測":
            review_data.append({"url": url, "title": title})


# 轉換成 DataFrame
df_review = pd.DataFrame(review_data)
review_tuples = list(zip(df_review['url'], df_review['title']))

content_tag_re = re.compile(r"'content_tag':\s*\"([^\"]+)\"")

def scrape_single_game_news_article(index, url, title):
  with requests.Session() as rs:
      res = rs.get(url)
      soup = BeautifulSoup(res.text, 'html.parser')

      author_element = soup.find("h3", class_="name")
      author_name = author_element.get_text(strip=True) if author_element else "Unknown Author"

      author_desc_element = soup.find("div", class_="context-box__text")
      author_desc = author_desc_element.get_text(separator=" ", strip=True) if author_desc_element else ""

      paragraphs = [p for p in soup.find_all('p') if author_desc_element is None or p not in author_desc_element.find_all('p')]
      article_text = "\n".join([p.get_text(separator=" ", strip=True) for p in paragraphs if p.get_text(strip=True)])

      script_tag = soup.find("script", string=re.compile("dataLayer"))
      tag = ""
      if script_tag and script_tag.string:
          tag_match = content_tag_re.search(script_tag.string)
          tag = tag_match.group(1) if tag_match else ""


      publication_date=None
      if script_tag and script_tag.string:
        pub_date_match = re.search(r"'publication_date':\s*'([^']+)'", script_tag.string)
        publication_date = pub_date_match.group(1) if pub_date_match else None
      publication_date = pd.to_datetime(publication_date, errors='coerce')


      return (index, {
                "url": url,
                "title": title,
                "author": author_name,
                "author_description": author_desc,
                "publication_date": publication_date,
                "topics": tag,
                "content": article_text
            })

def scrape_udn_game_news_articles(url_list, max_workers=20):
    """ 多線程爬取 TechCrunch 文章，確保結果順序不亂 """
    articles = []
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, (url, title) in enumerate(url_list):
            futures.append(executor.submit(scrape_single_game_news_article, i, url, title))

        for future in tqdm(as_completed(futures), total=len(url_list), desc="爬取進度"):
            index, article = future.result()
            if article:
                articles.append((index, article))

    articles.sort(key=lambda x: x[0])
    return [article for _, article in articles]

article_data=scrape_udn_game_news_articles(review_tuples)

article_data= pd.DataFrame(article_data)
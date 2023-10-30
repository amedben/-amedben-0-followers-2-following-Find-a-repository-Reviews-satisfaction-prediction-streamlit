import requests
from bs4 import BeautifulSoup
import pandas as pd

global headers
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 12; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'}

def scrapeAmazonReviews(url, no_of_pages = 10):


  name = []
  ratings = []
  date = []
  review_header = []
  product_details = []
  review_data = []
  helpful = []

  assert (url.startswith('https://www.amazon.')), "Only Amazon pages can be scraped using this."

  assert (url.endswith('reviewerType=all_reviews')), "Not the right page. Please use the all reviews page as the URL."

  # scraping à travers les pages
  for i in range(1, no_of_pages + 1):
    URL = f"{url}&pageNumber={1}"
    page = requests.get(URL)

    # Si la page n'est pas trouvée Erreur 404
    assert (page.status_code != 404), "Error 404 : Page Not Found."

    # continuer à demander jusqu'à ce que la demande soit acceptée
    while page.status_code != 200:
      page = requests.get(URL)

    scrape = BeautifulSoup(page.content, "html.parser")

    # obtenir toutes les "review cards" dans une page
    cards = scrape.find_all('div', class_='a-section review aok-relative')
    # si aucune "card" n'est présente dans la page, terminer le scraping
    if len(cards) == 0:
      print('Reached end of reviews.')
      break

    # scraping à travers review cards
    for card in cards:
      # try except utilisé pour ajouter des valeurs None si la valeur sur un produit n'existe pas
      try:
        name.append(card.find('span', class_='a-profile-name').text)
      except:
        name.append(None)

      try:
        ratings.append(int(card.find('span', class_="a-icon-alt").text[0]))
      except:
        ratings.append(None)

      try:
        review_header.append(card.find('a', class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").findChild('span',class_='').text)
      except:
        review_header.append(None)

      try:
        date.append(card.find('span', class_="a-size-base a-color-secondary review-date").text[24:])
      except:
        date.append(None)

      try:
        product_details.append(card.find('a', attrs={'class':"a-size-mini a-link-normal a-color-secondary", 'data-hook':'format-strip'}).text)
      except:
        product_details.append(None)

      try:
        review_data.append(card.find('span', attrs={'class':"a-size-base review-text review-text-content", 'data-hook':'review-body'}).findChild('span').text)
      except:
        review_data.append(None)

      try:
        helpful.append(card.find('span', class_="a-size-base a-color-tertiary cr-vote-text").text)
      except:
        helpful.append(None)

  reviews = {
      'Name': name,
      'Ratings' : ratings,
      'Header' : review_header,
      'Date' : date,
      'Product_Details' : product_details,
      'Review' : review_data,
      'Helpful' : helpful
  }

  df = pd.DataFrame(reviews)

  return df

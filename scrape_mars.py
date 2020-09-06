from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}

    # Define URLs used
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    spacefacts_url = "https://space-facts.com/mars/"

    # Headline and description
    browser.visit(nasa_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars["news_headline"] = soup.find('div', class_="content_title").text
    mars["news_p"] = soup.find('div', class_="rollover_description_inner").text

    # Space Facts Table

    browser.visit(spacefacts_url)
    time.sleep(2)
    html = browser.html

    tables = pd.read_html(html)
    facts_df = tables[0]
    mars["html_facts_table"] = facts_df.to_html()

    # Featured Mars Image

    browser.visit(jpl_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find('a', class_="button fancybox")['data-fancybox-href']
    mars["featured_image_url"] = "https://www.jpl.nasa.gov" + image

    browser.quit()

    return mars
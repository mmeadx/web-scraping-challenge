from splinter import Browser
from bs4 import BeautifulSoup as bs
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
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # ------- HEADLINE AND DESCRIPTION ------- #

    # Visit Browser - Make Soup
    browser.visit(nasa_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find and Grab headline and description
    headline_item = soup.select_one('ul.item_list  li.slide')
    mars["news_headline"] = headline_item.find('div', class_="content_title").text
    mars["news_p"] = headline_item.find('div', class_="rollover_description_inner").text

    # ------- FEATURED IMAGE -------

    browser.visit(jpl_url)
    time.sleep(2)
    
    # Use Splinter to Click on 'Full Image' and then 'More Info'
    full_image = browser.find_by_id("full_image")
    full_image.click()
    more_info = browser.find_by_text('more info     ')
    more_info.click()

    # Design xpath to click on image 
    xpath = '//div//img[@class="main_image"]'
    results = browser.find_by_xpath(xpath)
    full_image = results[0]
    full_image.click()

    # Get Full Res Image URL
    html_img = browser.html
    soup_img = bs(html_img, 'html.parser')
    featured_image_url = soup_img.body.img['src']

    mars["featured_image_url"] = featured_image_url


    # ------- SPACE FACTS TABLE -------

    browser.visit(spacefacts_url)
    time.sleep(2)
    html = browser.html
    
    # Get Table
    tables = pd.read_html(html)
    facts_df = tables[0]

    # Format Table
    facts_df = facts_df.rename(columns={0:'Description', 1:'Mars'})
    facts_df.set_index('Description', inplace=True)

    mars["html_facts_table"] = facts_df.to_html(classes="table table-bordered table-striped")

    # ------- MARS HEMISPHERES IMAGE GRAB -------

    browser.visit(hemi_url)
    time.sleep(2)
    html = browser.html

    # Make Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve Titles r
    hemis = soup.select('div.item div.description h3')

    hemisphere_image_urls = []

    # Loop through items
    for item in hemis:
    
        list_dict = {}

        # find and click on the element holding Hemisphere (Splinter)
        browser.find_by_text(item.text).click()
        # find the image:
        image = browser.find_by_text('Sample').first
        
        # add name and img url to dictionary
        list_dict['name'] = item.text
        list_dict['img_url'] = image['href']
        
        # append results to the list
        hemisphere_image_urls.append(list_dict)
    
        # navigate back to previous url
        browser.back()
    
    mars["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars
#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

#Lauch web browser robot
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

#Scrapping function
def scrape():
    browser = init_browser()
    listings = {}

    #Scrape News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["news_title"] = soup.find('li', class_='slide').find('div',class_='content_title').text
    listings["news_p"] = soup.find('li', class_='slide').find('div',class_='article_teaser_body').text

    #Scrape Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featured_image_url = soup.find('article', class_='carousel_item').attrs['style']
    featured_image_url='https://www.jpl.nasa.gov'+featured_image_url[23:-3]
    listings["featured_image_url"] = featured_image_url

    #Scrape Weather - None of the methods thought in class worked out, evidence in Jupyter notebook.
    mars_weather = 'InSight sol 708 (2020-11-22) low -93.2ºC (-135.8ºF) high -8.2ºC (17.2ºF) winds from the W at 6.0 m/s (13.4 mph) gusting to 20.2 m/s (45.2 mph) pressure at 7.40 hPa'
    listings["mars_weather"] = mars_weather

    #Scrape Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['Measure','Value']
    mars_table = mars_df.to_html(index=False)
    listings["mars_facts"] = mars_table

    #Scrape Mars Hemispheres
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemisphere_image_urls = []
    searchlst=['Cerberus','Schiaparelli','Syrtis','Marineris']
    for x in searchlst:
        browser.links.find_by_partial_text(x).click()
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('h2', class_='title').text
        img_url = soup.find('li').find('a')['href']
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
        browser.back()
    listings["hemisphere_image_urls"] = hemisphere_image_urls

    #Close browser and return results
    browser.quit()
    return listings
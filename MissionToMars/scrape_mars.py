import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

    # Scrape most recent news title and body
    url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url_1)

    html_1 = browser.html

    soup = bs(html_1, 'html.parser')

    news_title = soup.find('div', class_='content_title').text

    news_p = soup.find('div', class_='article_teaser_body').text

    # Scrape Featured Image
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_2)

    browser.click_link_by_partial_text('FULL IMAGE')

    html_2 = browser.html

    soup = bs(html_2, 'html.parser')

    src_url = soup.find(id='full_image').get('data-fancybox-href')

    featured_image_url = 'https://www.jpl.nasa.gov' + src_url

    # Scrape current weather
    url_3 = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url_3)

    html_3 = browser.html

    soup = bs(html_3, 'html.parser')

    mars_weather = soup.find('div', class_='js-tweet-text-container').p.text


    # Scrape facts to table

    url_4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_4)

    df = tables[0]

    df = df.rename(columns = {0:' ',1:'  '}).set_index(' ')

    mars_html = df.to_html('/Users/danvaldes/Desktop/bootcamp/web-scraping-challenge/MissionToMars/facts.html', classes="table table striped")

    # Scrape hemisphere photos

    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_5)

    hemi = ['Cerberus','Schiaparelli','Syrtis Major','Valles Marineris']

    hemisphere_image_urls = []

    for name in hemi:
        
        browser.click_link_by_partial_text(name + ' Hemisphere Enhanced')
        
        html_5 = browser.html
        
        soup = bs(html_5, 'html.parser')
        
        img_url = soup.find('div', class_='downloads').a['href']
        
        title = name + ' Hemisphere'
        
        hemi_dict = {'title':title,'img_url':img_url}
        
        hemisphere_image_urls.append(hemi_dict)
        
        browser.visit(url_5)


    content = {
        'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'mars_weather':mars_weather,
        'mars_html':mars_html,
        'hemisphere_image_urls':hemisphere_image_urls
    }

    browser.quit()
    
    return content

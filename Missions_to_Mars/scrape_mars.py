#import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize browser
def init_browser(): 
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create a scrape function that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
def scrape():

    """NASA Mars News"""
    #Run browser
    browser = init_browser()
    #News url
    url_news = 'https://mars.nasa.gov/news/'
    # Visit the news url through the splinter module and add 5 sec delay in the execution 
    browser.visit(url_news)
    time.sleep(5)
    # HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.
    news_title = soup.find_all('div', class_='content_title')[1]
    news_title = news_title.text
    news_p = soup.find(class_='article_teaser_body').text

    
    """JPL Mars Space Images - Featured Image"""
    #Run browser
    browser = init_browser()
    #Featured Image url
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Use splinter to navigate the site and add 5 sec delay in the execution
    browser.visit(url_img)
    time.sleep(5)
    # HTML Object
    html1 = browser.html
    # Parse HTML with Beautiful Soup
    soup1 = BeautifulSoup(html1, 'html.parser')
    # find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    featured_image = soup1.find('article')['style'].replace("background-image: url('",'').replace("');",'')
    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image}')
    


    """Mars Weather"""
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    # Use splinter to navigate the site and add 5 sec delay in the execution
    browser.visit(url_weather)
    time.sleep(5)
    # HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Save the tweet text for the weather report as a variable called mars_weather.
    mars_weather = soup.find_all("article", attrs={"role":"article"})[0].text
    #Replace all \n with space for continuity
    mars_weather = mars_weather.replace('\n', ' ')
    #Split to get rid of the initial part of the statement "Mars Weather@MarsWxReport·9hInSight "
    mars_weather= mars_weather.split("InSight ")[1]



    """Mars Facts"""
    # * Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url_facts = 'https://space-facts.com/mars/'
    # * Use Pandas to convert the data to a HTML table string.
    table = pd.read_html(url_facts)[0]
    #rename columns
    table.columns=['Description', 'Values']
    #set index
    table.set_index('Description', inplace = True)
    #convert to html
    table.to_html('Resources/mars_facts.html')
    
    
    """Mars Hemispheres"""
    # * Visit the USGS Astrogeology site to obtain high resolution images for each of Mars hemispheres.
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(astro_url)
    time.sleep(5)
    # HTML Object
    html = browser.html
    # Parse the HTML object with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    hemispheres = soup.find_all(class_="description")
    
    
    hemisphere_image_urls = []

    base_url = 'https://astrogeology.usgs.gov'

    for hemisphere in hemispheres:
        #scrape and store the title of the hemispheres. Replace the word enhanced
        title = hemisphere.find('h3').text
        title = title.replace('Enhanced', '')
        
        #scrape and store the partial url and visit the full url link and parse the HTML
        url = hemisphere.find('a')['href']
        browser.visit(base_url+url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get the partial url of the image and join with the base url
        image_url = soup.find('img',class_='thumb')['src']
        img_url = base_url+image_url
        
        #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
        
    


    #create a dict to hold all data
    mars_data = {
        'news_title': news_title,
        'news_p':news_p,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'hemisphere_image_urls' : hemisphere_image_urls
    }

    # mars_data['news_title'] = news_title
    # mars_data['news_p'] = news_p

    # mars_data['featured_image_url'] = featured_image_url

    # mars_data['mars_weather'] = mars_weather

    # mars_data['table'] = table

    # mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    
    return mars_data
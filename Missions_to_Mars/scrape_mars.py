from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": '/Users/shanaida/Desktop/web-scraping-challenge/Missions_to_Mars/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    all_mars_data= {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Create BeautifulSoup object; parse with 'html.parser'
    browser.visit(url)
    nasa_html = browser.html
    soup = BeautifulSoup(nasa_html, 'html.parser')  

    #Examine the results, then determine element that contains sought info
    print(soup.prettify())

    # Find the latest news title and paragraph
    item_list = soup.find('ul', class_='item_list')
    first_list_item = item_list.find('li', class_='slide')
    news_title = first_list_item.find('div', class_='content_title').text
    news_p= first_list_item.find('div', class_='article_teaser_body').text
    print(f"The Latest Nasa Mars News Title is: {news_title}")
    print(f"Paragraph: {news_p}")

    #Scrape from JPL website and get the featured_image_url
    jpl_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()

    jpl_html= browser.html
    jpl_soup= BeautifulSoup(jpl_html, 'html.parser')
    print(jpl_soup.prettify())

    image_class= jpl_soup.find('img', class_='fancybox-image')['src']
    featured_image_url= f'https://www.jpl.nasa.gov{image_class}'
    print(f"Featured Image URL: {featured_image_url}")

    #Visit the Mars Facts webpageand use Pandas to scrape the table
    #containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url= 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_facts_html= browser.html
    mars_facts_soup= BeautifulSoup(mars_facts_html, 'html.parser')
    print(mars_facts_soup.prettify())

    mars_facts_table= mars_facts_soup.find('table', class_='tablepress tablepress-id-p-mars')
    mars_facts_table

    column_1=mars_facts_table.find_all('td', class_='column-1')
    column_2=mars_facts_table.find_all('td', class_='column-2')

    fields= []
    values= []

    for row in column_1:
        field= row.text.strip()
        fields.append(fields)
    
    for row in column_2:
        value= row.text.strip()
        values.append(value)
    
    mars_facts_df = pd.DataFrame({
        "Column1":fields,
        "Column2":values
        })

    mars_facts_html_df = mars_facts_df.to_html(header=False, index=False)
    mars_facts_df

    #Visit the USGS Astrogeology site here to obtain high 
    #resolution images for each of Mar's hemispheres

    mars_hemis_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemis_list= []

    for x in y:
        hemis= {}
    
        browser.visit(mars_hemis_url)
        hemis_html= browser.html
        hemis_soup= BeautifulSoup(hemis_html, 'html.parser')
        hemis_links= hemis_soup.find_all('a', class_='product-item')
        hemis_title= hemis_links[x].text.strip('Enhanced')
    
        details= browser.find_by_css('a.product-item')
        details[x].click()
        browser.find_link_by_text('Sample').first.click()
    
        browser.windows.current= browser.windows[-1]
        hemis_img_html= browser.html
        browser.windows.current= browser.windows[0]
        browser.windows[-1].close()
    
        hemis_img_soup= BeautifulSoup(hemis_img_html, 'html.parser')
        hemis_img_path= hemis_img_soup.find('img')['src']

        print(hemis_title)
        hemis['title']= hemis_title.strip()
        print(hemis_img_path)
        hemis['img_url']= hemis_img_path

        hemis_list.append(hemis)

     all_mars_data["hemis_imgs"] = hemis_list

     # Close the browser after scraping
     browser.quit()

     # Return results
     return all_mars_data
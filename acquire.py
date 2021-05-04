import pandas as pd

import requests
import bs4
import os

###############################Codeup Blog Articles###############################

#listing pages to scrape the article text in function
urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
    'https://codeup.com/data-science-myths/',
    'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
    'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
    'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    
    
#function to get list of article dictionaries
def get_blog_articles(urls):
    
    '''
    This function takes in urls that contain articles from the Codeup website,
    scrapes the article title and article text from each,
    and returns a list of dictionaries, 
    with each dictionary representing one article. 
    '''
    
    #create empty list 
    article_list = []
    
    #for loop to iterate through list of URLs
    for url in urls:
        
        #empty dictionary
        dic = {}
        
        #specify headers
        headers = {'User-Agent': 'Codeup Data Science'}
        
        #make http request and turn response into a beautiful soup object
        response = requests.get(url, headers=headers)
        html = response.text
        soup = bs4.BeautifulSoup(html)
        
        #save article body text
        article = soup.select('.jupiterx-main-content')[0]
        
        #save article title and content text
        title = article.find('h1').text
        content = article.select('.jupiterx-post-content.clearfix')[0].text
        
        #store article body and title in dictionary
        dic['title'] = title
        dic['content'] = content
        
        #append dictionary to list
        article_list.append(dic)
        
    #return list when all article text added
    return article_list




#making it into a dataframe along w/ date and image info

# Make a function that works on a single url
# Make sure your function has everything it needs inside (try to avoid globals)

def get_codeup_blog(url):
    
    # Set the headers to show as Netscape Navigator on Windows 98, b/c I feel like creating an anomaly in the logs
    headers = {"User-Agent": "Mozilla/4.5 (compatible; HTTrack 3.0x; Windows 98)"}

    # Get the http response object from the server
    response = requests.get(url, headers=headers)
    
    soup = bs4.BeautifulSoup(response.text)
    
    title = soup.find("h1").text
    published_date = soup.time.text
    
    if len(soup.select(".jupiterx-post-image")) > 0:
        blog_image = soup.select(".jupiterx-post-image")[0].picture.img["data-src"]
    else:
        blog_image = None
        
    content = soup.select(".jupiterx-post-content")[0].text
    
    output = {}
    output["title"] = title
    output["published_date"] = published_date
    output["blog_image"] = blog_image
    output["content"] = content
    
    return output

urls = [
    "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
    "https://codeup.com/data-science-myths/",
    "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
    "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
    "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/"
]

def get_all_blog_articles(urls):
    # List of dictionaries
    posts = [get_codeup_blog(url) for url in urls]
    
    return pd.DataFrame(posts)



###############################Inshorts News Articles###############################

#function that handles a single article and produces a dictionary
def get_article(article, category):
    # Attribute selector
    title = article.select("[itemprop='headline']")[0].text
    
    # article body
    content = article.select("[itemprop='articleBody']")[0].text
    
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output

def get_articles(category):
    
    '''
    This function takes in a category as a string (category),
    that must be an available category in inshorts, 
    
    and returns a list of dictionaries where each dictionary represents a single inshort article.
    '''
    
    base = "https://inshorts.com/en/read/"
    
    #concatenate base_url with the category
    url = base + category
    
    #get http response object from the server
    response = requests.get(url)

    #make soup out of the raw html
    soup = bs4.BeautifulSoup(response.text)
    
    #ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    #iterate through every article tag/soup 
    for article in articles:
        
        #returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        #append the dictionary to the list
        output.append(article_data)
    
    #return the list of dictionaries
    return output


def get_news_articles(categories):
    '''
    This function takes in a list of categories where the category is part of the URL pattern on inshorts,
    
    and returns a dataframe of every article from every category listed
    
    Each row in the dataframe is a single article.
    '''
    all_inshorts = []

    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles

    
    return all_inshorts


categories = ["business", "sports", "technology", "entertainment"]


def news_articles_df(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    all_inshorts = []

    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles

    df = pd.DataFrame(all_inshorts)
    return df

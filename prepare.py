import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import acquire


################ Functions to prepare textual data ################


def basic_clean(string):
    '''
    This function takes in a string and applies basic text cleaning by:
    lowercasing everything,
    normalizing unicode characters,
    replacing anything that is not a letter, number, whitespace, or a single quote
    
    and returns the cleaned string.
    '''
    
    #lowercase
    string = string.lower()
    
    #normalize unicode chars
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    #replace anything not a letter, number, whitespace, or single quote
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    
    return string



def tokenize(string):
    '''
    This function takes in a string, 
    tokenizes all the words in the string,
    
    and returns the tokenized string.
    '''
    
    #create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    string = tokenizer.tokenize(string, return_str=True)
    
    return string



def stem(string):
    '''
    This function takes in some text
    
    and returns the text after applying stemming to all the words.
    '''
    
    #create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    #apply the stemmer to each word in the string
    stems = [ps.stem(word) for word in string.split()]
    
    #join stemmed list of words into a string again
    string_stemmed = ' '.join(stems)
    
    return string_stemmed



def lemmatize(string):
    '''
    This function takes in some text
    
    and returns the text after applying lemmatization to each word.
    '''
    
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    #use the lemmatizer on each word in the list of words created by using split
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    #join lemmatized list of words into a string again
    string_lemmatized = ' '.join(lemmas)
    
    return string_lemmatized



def remove_stopwords(string, extra_words = [], exclude_words = []): 
    '''
    This function takes in a string, 
    optional extra_words (additional stop words),
    and optional exclude_words (words that won't be removed) parameters with default empty lists,
    
    and returns a string after removing all the stopwords.
    '''

    #create stopword_list
    stopword_list = stopwords.words('english')
    
    #remove 'exclude_words' from stopword_list to keep these in my text
    stopword_list = set(stopword_list) - set(exclude_words)
    
    #add in 'extra_words' to stopword_list
    stopword_list = stopword_list.union(set(extra_words))
    
    #split words in string
    words = string.split()
    
    #create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    #join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords



#using data from acquire to produce df of the news articles and codeup blog posts

#News Articles
categories = ['business', 'sports', 'technology', 'entertainment']
news_df = pd.DataFrame(acquire.get_news_articles(categories))

#Codeup Blog Posts
urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/', 
        'https://codeup.com/data-science-myths/', 
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/', 
        'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/', 
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

codeup_df = pd.DataFrame(acquire.get_blog_articles(urls))




def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df, 
    the string name for a text column,
    with option to pass lists for extra_words and exclude_words,
    renames content column to be 'original',
    
    and returns a df with the text article title, original text, 
    cleaned, tokenized, stemmed, and lemmatized text with stopwords removed.
    '''
    
    #rename the content column to original
    df = df.rename(columns={"content": "original"})
    
    #holds the normalized and tokenized original w/ stopwords removed
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    #holds the stemmed version of the cleaned data
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    #holds the lemmatized version of the cleaned data
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df[['title', column, 'clean', 'stemmed', 'lemmatized']]
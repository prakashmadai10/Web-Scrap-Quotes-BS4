
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
# get the web page

def ScrapQuotesData():
    url = "http://quotes.toscrape.com/page/%i/" # url format to follow
    page = 1 # page numbers for the url
    stop = False # parameter to stop our crawl when necessary
    list_scrap_info = [] # list to append scraped info to

    while stop == False:
        r = requests.get("http://quotes.toscrape.com/page/%i/" % page)
        soup = bs(r.content,'html.parser')
        if soup.find("div", {"class":"quote"}) == None:
            stop = True
        else:
            for quote in soup.find_all("div", {"class":"quote"}):
                d = {} # dictionary for our scraped information
                d['Quote'] = quote.find("span", {"class":"text"}).text
                d['Author'] = quote.find("a")["href"]

                quotes_aboutUrl= "http://quotes.toscrape.com" + d['Author']
                req = requests.get(quotes_aboutUrl)
                soup1 = bs(req.text, "html.parser")

                d['Author Name'] = soup1.find("div", {"class": "author-details"}).text
                d['Date of Birth'] = soup1.find("span", {"class": "author-born-date"}).text
                d['Place of Birth'] = soup1.find( "span", {"class": "author-born-location"}).text

                d['Description']= soup1.find("div", {"class": "author-description"}).text

                d['Tags'] = [tag.text for tag in quote.find_all("a",\
            {"class":"tag"})]
                d['Quotes By'] = [footer1.text for footer1 in soup1.find_all("footer",\
            {"class":"footer"})]
               
                list_scrap_info.append(d)
            page += 1
    return list_scrap_info

df=pd.DataFrame(ScrapQuotesData())
df.drop(columns=['Author'],inplace=True)
df.to_excel('scrap.xlsx')



 
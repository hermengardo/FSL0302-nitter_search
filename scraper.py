import random
from time import sleep

import requests
import numpy as np
from lxml import html

import utils


def main():
    Scraper(query='pizza hoje', random_time=True, random_interval=(0.01, 0.1))


class Scraper:
    def __init__(self,
                 query: str,
                 file_path='data.csv',
                 delay=0.01,
                 random_time=True,
                 random_interval=(0, 1),
                 seed=42):
        # Url and headers
        url = f"https://nitter.net/search?f=tweets&q={query}"
        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
                         "Accept": "*/*",
                         "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                         "Accept-Encoding": "gzip, deflate, br",
                         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         "X-Requested-With": "XMLHttpRequest",
                         "Connection": "keep-alive"}

        # Set delay      
        random.seed(seed)
        if random_time:
            self.delay = delay + random.uniform(*random_interval) 
        else:
            self.delay = delay

        # Start scraping
        self.scrape_page(url)

    def html_parser(self, response):
        return html.fromstring(response.content.decode('utf-8'))

    def scrape_page(self, url):
        response = requests.request("GET", 
                                    url,
                                    headers=self._headers)
        # Html Parser
        tree = self.html_parser(response)

        # Tweets Urls
        tweets = self.tweets_urls(tree)

        # Next page url
        next_page = self.page_url(tree)

        # Scrape publications
        self.scrape_publication(tweets)

    def scrape_publication(self, urls):
        # Init an empty array
        data = {'fullname':[],
                'username':[],
                'content':[],
                'tweet_published':[],
                'hashtags':[],
                'img_avatar':[],
                'images':[]}

        # Paths for text elements
        text_fields = ['div#m.main-tweet a.fullname',
                       'div#m.main-tweet a.username',
                       'div#m.main-tweet div.tweet-content',
                       'div#m.main-tweet p.tweet-published']

        # Path for hashtags
        hashtag_field = ['div#m.main-tweet div.tweet-content > a']

        # Path for image
        img_fields = ['div#m.main-tweet img.avatar',
                      'div#m.main-tweet a.still-image img']

        # Path for all fields
        paths = text_fields + hashtag_field + img_fields

        for url in urls:
            response = requests.request("GET", 
                                        f"https://nitter.net{url}",
                                        headers=self._headers) # 

            tree = self.html_parser(response)

            # Collect data
            for field, key in zip(paths, data.keys()):
                # text data
                if field in text_fields:
                    data[key].append(self.get_text(tree, field))
                # image data
                if field in img_fields:
                    data[key].append(self.get_img(tree, field))
                # hashtags
                if field in hashtag_field:
                    data[key].append(self.get_hashtags(tree, field))
                
            print(f"Collected: {len(data['username'])}") # Using username key as counter because all users must have username
            sleep(self.delay)
        utils.save_data_as_csv(data)

    def get_text(self, tree, field):
        elem = tree.cssselect(field)[0]
        return elem.text.strip()

    def get_img(self, tree, field):
        images = tree.cssselect(field)
        if len(images) == 0:
            return []
        return [f"https://nitter.net{image.get('src').strip()}" for image in images]
    
    def get_hashtags(self, tree, field):
        elems = tree.cssselect(field)
        if len(elems) == 0:
            return []
        return [potential_hashtag.text_content() for potential_hashtag in elems 
                if utils.is_hashtag(potential_hashtag.text_content())]

    def page_url(self, tree):
        link = tree.cssselect('div.show-more > a')
        if link is not None:
            return f"https://nitter.net/search{link[0].get('href').strip()}"
        else:
            print("Finished.")

    def tweets_urls(self, tree):
        # Extract links with class 'tweet-link'
        return [a.get('href') for a in tree.cssselect('a.tweet-link')]
        


if __name__ == "__main__":
    main()

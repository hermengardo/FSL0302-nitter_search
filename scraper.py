import random
from time import sleep

import requests
import numpy as np
from lxml import html

import utils


def main():
    NitterSearch(query='política+lang%3Apt', random_time=True, random_interval=(0.01, 0.1))


class NitterSearch:
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
                'tweet_published_at':[],
                'n_comments':[],
                'n_retweets':[],
                'n_quotes':[],
                'n_hearts':[],
                'img_avatar':[],
                'images':[],
                'quote':[],
                'third_party':[],
                'verified':[],
                'urls':[],
                'hashtags':[]}

        # Paths for text elements
        text_fields = ['div#m.main-tweet a.fullname',
                       'div#m.main-tweet a.username',
                       'div#m.main-tweet div.tweet-content',
                       'div#m.main-tweet p.tweet-published']

        stats_fields = ['div#m.main-tweet span.icon-comment',
                        'div#m.main-tweet span.icon-retweet',
                        'div#m.main-tweet span.icon-quote',
                        'div#m.main-tweet span.icon-heart']

        # Path for images
        img_fields = ['div#m.main-tweet img.avatar',
                      'div#m.main-tweet a.still-image img']

        # Quotes and third-party urls
        quote_fields = ['div#m.main-tweet a.quote-link',
                        'div#m.main-tweet a.card-container']

        # All paths
        paths = text_fields + stats_fields + img_fields + quote_fields

        for url in urls:
            response = requests.request("GET", 
                                        f"https://nitter.net/DyegoNascymento/status/1654917920131104770#m",
                                        headers=self._headers) # 

            tree = self.html_parser(response)

            # Collect data
            for field, key in zip(paths, data.keys()):
                # text data
                if field in text_fields:
                    data[key].append(self.get_text(tree, field))
                # tweet stats
                if field in stats_fields:
                    data[key].append(self.get_stats(tree, field))
                # image data
                if field in img_fields:
                    data[key].append(self.get_img(tree, field))
                # mentioning data
                if field in quote_fields:
                    data[key].append(self.get_urls(tree, field))
            
            # Collect hashtags and urls
            hashtags, urls = self.get_hash_url(tree, 'div#m.main-tweet div.tweet-content > a')
            data['urls'].append(urls)
            data['hashtags'].append(hashtags)
            data['verified'].append(self.get_verified(tree))

            print(f"Collected: {len(data['username'])}") # Using username key as counter because all users must have username
            print(data)
            sleep(self.delay)

    def get_verified(self, tree):
        if tree.cssselect('div#m.main-tweet span.icon-ok')[0].get('title') == "Verified account":
            return True
        return False

    def get_text(self, tree, field):
        text = tree.cssselect(field)[0]
        try:
            return ''.join(text.text_content())
        except AttributeError:
            return ''

    def get_img(self, tree, field):
        images = tree.cssselect(field)
        try:
            return [f"https://nitter.net{image.get('src').strip()}" for image in images]
        except AttributeError: # If the element is not present, return an empty list
            return []
    
    def get_urls(self, tree, field):
        urls = tree.cssselect(field)
        try:
            return [url.get('href') for url in urls]
        except AttributeError:
            return []

    def get_stats(self, tree, field):
        stat = tree.cssselect(field)[0].getparent()
        try:
            return utils.string_to_int(stat.text_content().strip())
        except ValueError:
            return 0

    def get_hash_url(self, tree, field):
        elems = tree.cssselect(field)
        hashtags = [potential_hashtag.text_content() for potential_hashtag in elems 
                    if utils.is_hashtag(potential_hashtag.text_content())]

        urls = [potential_hashtag.get('href') for potential_hashtag in elems 
                if not utils.is_hashtag(potential_hashtag.text_content())]

        return hashtags, urls

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

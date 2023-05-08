import random
from time import sleep

import requests
from lxml import html

import utils


class NitterSearch:
    def __init__(self,
                 query: str,
                 file_path='data.csv',
                 delay=0.01,
                 random_time=False,
                 random_interval=(0, 1),
                 seed=42,
                 timeout_wait=60,
                 retries=3) -> None:
        # Encode special characters to hexadecimal representation
        query = utils.encode_string(query)
        # Setting up the request
        url = f"https://nitter.net/search?f=tweets&q={query}"
        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
                         "Accept": "*/*",
                         "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                         "Accept-Encoding": "gzip, deflate, br",
                         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         "X-Requested-With": "XMLHttpRequest",
                         "Connection": "keep-alive"}

        # Initialize publication count
        self._count = 0

        # Set delay
        random.seed(seed)
        if random_time:
            self._delay = delay + random.uniform(*random_interval)
        else:
            self._delay = delay

        # Set connection error handler parameters
        self._timeout_wait = timeout_wait
        self._retries = retries

        # Set filepath
        self._file_path = file_path

        # Start scraping
        self.scrape_page(url)

    def html_parser(self, response: requests.models.Response) -> html.HtmlElement:
        return html.fromstring(response.content.decode('utf-8'))

    def scrape_page(self, url: str):
        """
        Scrapes all data from Nitter.net for a given search page.

        Args:
        - url (str): The URL of the search page to scrape.

        Returns:
        - None
        """
        page_count = 0
        while True:
            try:
                # Send a GET request to the given URL with custom headers.
                response = requests.get(url, headers=self._headers)

                # Raise an exception if the response was not successful.
                response.raise_for_status()

                tree = self.html_parser(response)  # Parse the HTML

                # Extract the URLs of the tweets from the parsed HTML tree
                tweets = self.tweets_urls(tree)

                # Generate the URL of the next page to scrape based on the current page.
                url = f'https://nitter.net/search{self.page_url(tree)}'

                # Scrape the publications for each tweet URL found.
                data = self.scrape_publication(tweets)
                utils.save_dict_as_csv(data, self._file_path)
                page_count += 1
                print(f"Page {page_count} collected")
            except requests.exceptions.RequestException as e:
                if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout)) and self._retries > 0:
                    print(f"Connection error or read timeout occurred. Retrying in {self._timeout_wait} seconds...")
                    sleep(self._timeout_wait)
                    self._retries -= 1
                    continue
                else:
                    print("Request failed after multiple retries. Exiting...")
                    break
            except IndexError:
                print('Finished')
                break

    def scrape_publication(self, urls: list) -> dict:
        """
        Scrapes Twitter-like publications from a list of Nitter URLs,
        processes the scraped data and returns it as a dictionary.

        Args:
            urls (list): A list of Nitter URLs to scrape.

        Returns:
            dict: A dictionary containing scraped data for each publication.
        """
        # Initialize an empty dictionary to store the data for each tweet.
        data = {'fullname': [],
                'username': [],
                'content': [],
                'publishedAt': [],
                'comments': [],
                'retweets': [],
                'quotes': [],
                'hearts': [],
                'imgAvatar': [],
                'images': [],
                'videos': [],
                'quote': [],
                'externalLink': [],
                'repliedBy': [],
                'urls': [],
                'hashtags': []}

        # Define CSS selectors for each type of data to scrape
        text_fields = ['div#m.main-tweet a.fullname',
                       'div#m.main-tweet a.username',
                       'div#m.main-tweet div.tweet-content',
                       'div#m.main-tweet p.tweet-published']
        stats_fields = ['div#m.main-tweet span.icon-comment',
                        'div#m.main-tweet span.icon-retweet',
                        'div#m.main-tweet span.icon-quote',
                        'div#m.main-tweet span.icon-heart']
        img_fields = ['div#m.main-tweet img.avatar',
                      'div#m.main-tweet a.still-image img',
                      'div#m.main-tweet source']
        quote_fields = ['div#m.main-tweet a.quote-link',
                        'div#m.main-tweet a.card-container']
        paths = text_fields + stats_fields + img_fields + quote_fields

        # Loop through each tweet URL and scrape the data.
        for url in urls:
            clean_url = f"https://nitter.net{url}"
            response = requests.request("GET",
                                        clean_url,
                                        headers=self._headers)

            tree = self.html_parser(response)

            # Scrape text, stats, images, and links for each tweet.
            for field, key in zip(paths, data.keys()):
                if field in text_fields:
                    data[key].append(self.get_text(tree, field))
                elif field in stats_fields:
                    data[key].append(self.get_stats(tree, field))
                elif field in img_fields:
                    data[key].append(self.get_img(tree, field))
                elif field in quote_fields:
                    data[key].append(self.get_urls(tree, field))

            # Scrape data about who replied to the tweet.
            data['repliedBy'].append(self.get_user_replies(tree, clean_url))

            # Scrape hashtags and links mentioned in the tweet.
            hashtags, urls = self.get_hash_url(tree,
                                               'div#m.main-tweet div.tweet-content > a')
            data['urls'].append(urls)
            data['hashtags'].append(hashtags)

            # Print progress and wait before scraping the next tweet.
            self._count += 1
            print(f"Collected: {self._count} | From {data['username'][-1]}")
            sleep(self._delay)
        # Return data results
        return data

    def get_user_replies(self, tree: html.HtmlElement, url: str) -> list:
        usernames = [user.text_content() for user
                     in tree.cssselect('div#r.replies a.username')]
        while True:
            try:
                url_next_page = f"{url[:-2]}{self.page_url(tree)}"
                response = requests.request("GET",
                                            url_next_page,
                                            headers=self._headers)
                tree = self.html_parser(response)
                usernames += [user.text_content() for user
                              in tree.cssselect('div#r.replies a.username')]
            except IndexError:
                usernames += [user.text_content() for user
                              in tree.cssselect('div#r.replies a.username')]
                return usernames

    def get_text(self, tree: html.HtmlElement, field: str) -> str:
        text = tree.cssselect(field)[0]
        try:
            return ''.join(text.text_content())
        except AttributeError:
            return ''

    def get_img(self, tree: html.HtmlElement, field: str) -> list:
        images = tree.cssselect(field)
        try:
            return [f"https://nitter.net{image.get('src').strip()}"
                    for image in images]
        except AttributeError:
            return []

    def get_urls(self, tree: html.HtmlElement, field: str) -> list:
        urls = tree.cssselect(field)
        try:
            return [url.get('href') for url in urls]
        except AttributeError:
            return []

    def get_stats(self, tree: html.HtmlElement, field: str) -> int:
        stat = tree.cssselect(field)[0].getparent()
        try:
            return utils.string_to_int(stat.text_content().strip())
        except ValueError:
            return 0

    def get_hash_url(self, tree: html.HtmlElement, field: str) -> tuple:
        elems = tree.cssselect(field)
        hashtags = [potential_hashtag.text_content() for potential_hashtag
                    in elems if utils.is_hashtag(potential_hashtag.text_content())]

        urls = [potential_hashtag.get('href') for potential_hashtag in elems
                if not utils.is_hashtag(potential_hashtag.text_content())]

        return hashtags, urls

    def page_url(self, tree: html.HtmlElement) -> str:
        #  Extracts the URL of the next page from the HTML tree element.
        link = tree.cssselect('div[class="show-more"] > a')
        return link[0].get('href').strip()

    def tweets_urls(self, tree: html.HtmlElement) -> list:
        # Extracts URLs of tweets from the HTML tree element.
        return [a.get('href') for a in tree.cssselect('a.tweet-link')]

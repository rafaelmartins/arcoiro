import requests
from flask import current_app

from arcoiro.providers import BaseProvider


class TumblrProvider(BaseProvider):

    display_name = 'Tumblr'
    name = 'tumblr'
    url = 'http://tumblr.com'

    def get_urls_from_tag(self, tag):
        response = requests.get('http://api.tumblr.com/v2/tagged',
                                params={'tag': tag, 'api_key': self.api_key})
        if not response.ok:
            return None

        try:
            content = response.json()
        except:  # bad exception? lol
            return None

        if 'meta' in content and content['meta']['status'] != 200:
            return None

        if 'response' not in content:
            return None

        urls = []
        for post in content['response']:
            urls.append(post['post_url'])
        return urls

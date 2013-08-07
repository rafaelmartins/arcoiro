import requests

from arcoiro.providers import BaseProvider


class TwitterProvider(BaseProvider):

    display_name = 'Twitter'
    name = 'twitter'
    url = 'http://twitter.com'

    def get_bearer_token(self):
        # api key should be a tuple:
        # - Consumer key
        # - Consumer secret
        if len(self.api_key) != 2:
            return None

        response = requests.post('https://api.twitter.com/oauth2/token',
                                 data={'grant_type': 'client_credentials'},
                                 auth=self.api_key)
        if not response.ok:
            return None
        try:
            content = response.json()
        except:
            return None

        if 'token_type' not in content or content['token_type'] != 'bearer':
            return None

        if 'access_token' not in content:
            return None

        return content['access_token']


    def get_urls_from_tag(self, tag):
        token = self.get_bearer_token()
        if token is None:
            return None

        response = requests.get('https://api.twitter.com/1.1/search/tweets.json',
                                params={'q': '#%s' % tag, 'count': '100',
                                        'lang': 'pt'},
                                headers={'Authorization': 'Bearer %s' % token})
        if not response.ok:
            return None

        try:
            content = response.json()
        except:  # bad exception? lol
            return None

        if 'statuses' not in content:
            return None

        urls = []
        for tweet in content['statuses']:
            screen_name = tweet['user']['screen_name']
            tweet_id = tweet['id']
            url = 'https://twitter.com/%s/status/%s' % (screen_name, tweet_id)
            urls.append(url)
        return urls

import requests

from arcoiro.providers import BaseProvider


class FlickrProvider(BaseProvider):

    display_name = 'Flickr'
    name = 'flickr'
    url = 'http://flickr.com'

    def get_urls_from_tag(self, tag):
        response = requests.get('https://secure.flickr.com/services/rest',
                                params={'format': 'json',
                                        'nojsoncallback': '1',
                                        'api_key': self.api_key,
                                        'method': 'flickr.photos.search',
                                        'tags': tag})
        if not response.ok:
            return None

        try:
            content = response.json()
        except:  # bad exception? lol
            return None

        if 'stat' in content and content['stat'] != 'ok':
            return None

        if 'photos' not in content or 'photo' not in content['photos']:
            return None

        urls = []
        for photo in content['photos']['photo']:
            url = 'http://www.flickr.com/photos/%(owner)s/%(id)s' % photo
            urls.append(url)
        return urls
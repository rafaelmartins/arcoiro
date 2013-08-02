# -*- coding: utf-8 -*-

import random
import requests
from flask import Flask, abort, make_response, render_template
from werkzeug.contrib.cache import FileSystemCache

app = Flask(__name__)
app.config.setdefault('TAGS', ['bola', 'ball', 'arcoiro', 'arco-iris',
                               'rainbow', 'flor', 'flower', 'raquete',
                               'calcinha', 'violao', 'buzina'])
app.config.from_envvar('ARCOIRO_SETTINGS')

# store it in cache for 1 day. using file system cache because memcached is
# too mainstream. :)
cache = FileSystemCache('/tmp/__arcoiro__', default_timeout=60 * 60 * 24)


def get_urls_by_tag(tag):

    # use cache if possible
    urls = cache.get(tag)
    if urls is not None:
        return urls

    api_key = app.config.get('API_KEY')
    if api_key is None:
        raise RuntimeError('tumblr API key not found!')

    params = {'tag': tag, 'api_key': api_key}
    response = requests.get('http://api.tumblr.com/v2/tagged', params=params)
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

    # add it to cache
    cache.set(tag, urls)

    return urls


@app.route('/')
def home():
    tag = random.choice(app.config['TAGS'])
    urls = get_urls_by_tag(tag)
    if urls is None:
        abort(404)
    url = random.choice(urls)
    return render_template('frameset.html', url=url)


@app.route('/footer')
def footer():
    return render_template('footer.html')


if __name__ == '__main__':
    app.run(debug=True)
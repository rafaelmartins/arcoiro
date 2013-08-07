import random
from flask import Blueprint, abort, current_app, render_template

from arcoiro.providers import list_providers

views = Blueprint('views', __name__)


@views.route('/')
def home():
    tag = random.choice(current_app.config['TAGS'])
    provider = random.choice(list_providers())



    urls = provider().get_cached_urls_from_tag(tag)
    if urls is None:
        abort(404)
    url = random.choice(urls)
    return render_template('frameset.html', url=url)


@views.route('/footer')
def footer():
    return render_template('footer.html')

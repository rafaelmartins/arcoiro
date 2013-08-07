# -*- coding: utf-8 -*-

from flask import Flask

from arcoiro.views import views

def create_app():
    app = Flask(__name__)
    app.config.setdefault('TAGS', ['bola', 'ball', 'arcoiro', 'arco-iris',
                                   'rainbow', 'flor', 'flower', 'raquete',
                                   'calcinha', 'violao', 'buzina'])
    app.config.from_envvar('ARCOIRO_SETTINGS')
    app.register_blueprint(views)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)

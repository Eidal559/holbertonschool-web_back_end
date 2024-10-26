#!/usr/bin/env python3
""" Route module for the API - Infer appropriate time zone"""

from flask import Flask, request, render_template, g
from flask_babel import Babel
from os import getenv
from pytz import timezone as pytz_timezone
import pytz.exceptions
from typing import Union, Optional

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """ Babel configuration """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Set the above class object as the configuration for the app
app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return: 6-index.html
    """
    return render_template('6-index.html')


@babel.localeselector
def get_locale() -> Optional[str]:
    """ Determines best match for supported languages """
    # Check if there is a locale parameter/query string
    if request.args.get('locale'):
        locale = request.args.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale
    # Check if there is a locale in an existing user's profile
    elif g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # Default to return as a failsafe
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[dict, None]:
    """ Returns user dict if ID can be found """
    if request.args.get('login_as'):
        # Typecast the param to be able to search the user dict
        user_id = int(request.args.get('login_as'))
        if user_id in users:
            return users.get(user_id)
    return None


@app.before_request
def before_request() -> None:
    """ Finds user and sets as global on flask.g.user """
    g.user = get_user()


@babel.timezoneselector
def get_timezone() -> Optional[str]:
    """ Determines best match for supported timezones """
    # Check if there is a timezone parameter/query string
    if request.args.get('timezone'):
        tz_name = request.args.get('timezone')
        try:
            return pytz_timezone(tz_name).zone
        except pytz.exceptions.UnknownTimeZoneError:
            return None
    # Check if there is a timezone in an existing user's profile
    elif g.user and g.user.get('timezone'):
        try:
            return pytz_timezone(g.user.get('timezone')).zone
        except pytz.exceptions.UnknownTimeZoneError:
            return None
    # Default to return as a failsafe (UTC)
    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

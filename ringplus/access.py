"""Functions to get access token from ringplus."""

from __future__ import print_function

import requests
from bs4 import BeautifulSoup
try:  # python3
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
except:  # python2
    from urlparse import urlparse
    from urlparse import parse_qs

CLIENT_ID = 'dd89d121bae88b3667d28898b0febe8cd3cb77fd47b416b077c3a172858a6ea2'
REDIRECT_URI = 'https://www.google.com'


def get_auth_code(login, password):
    """Return the auth code.

    Route: GET https://my.ringplus.net/oauth/authorize
    """
    uri = 'https://my.ringplus.net/oauth/authorize'
    params = {'response_type': 'code',
              'client_id': CLIENT_ID,
              'redirect_uri': REDIRECT_URI}

    session = requests.Session()
    r1 = session.get(uri, params=params)

    data = _get_input_data(r1.content)
    # Update login data with email and password
    _set_login_and_password(data, login, password)

    r2 = session.post(r1.url, data=data)
    r2.raise_for_status()

    # Parse and return code from the returned url
    parser = urlparse(r2.url)
    return parse_qs(parser.query)['code'][0]


def _get_input_data(html):
    """Given the html from login page, return params needed to login."""
    soup = BeautifulSoup(html, 'html.parser')
    input_tags = soup.find_all('input')

    # Get the data from the tags
    data = {}
    for tag in input_tags:
        data[tag.attrs['name']] = tag.attrs.get('value', None)
    return data


def _set_login_and_password(data, login, password):
    for key in data.keys():
        if 'email' in key:
            data[key] = login
        if 'password' in key:
            data[key] = password

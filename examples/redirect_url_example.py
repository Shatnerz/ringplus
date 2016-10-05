"""Example where a user is redirected to obtain the access token."""

from __future__ import print_function
from ringplus.auth import OAuthHandler

from pprint import pprint  # Lets pretty print our output

# Constants
CLIENT_ID = 'CLIENT ID HERE'
CLIENT_SECRET = 'CLIENT SECRET HERE'
REDIRECT_URI = 'REDIRECT URI HERE'


# Setup OAuthHandler for your app
auth = OAuthHandler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# Get authorization url
# This is where the user grants your app permission and is then
# redirected to your redirect url.
auth_url = auth.get_authorization_url()
print(auth_url)

final_redirected_url = 'THE REDIRECT URL WITH THE CODE'
# This should be straightforward to grab with a web app.
# I am leaving this out of the example.

# Use the url and code to fetch the token
auth.fetch_token(final_redirected_url)
pprint(auth.access_token)

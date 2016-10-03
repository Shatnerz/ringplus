from __future__ import print_function
from ringplus.auth import OAuthHandler
from ringplus.api import API

client_id = 'CLIENT ID HERE'
client_secret = 'CLIENT SECRET HERE'
redirect_uri = 'REDIRECT URI HERE'

auth = OAuthHandler(client_id, client_secret, redirect_uri)
auth.login('YOUR USERNAME', 'YOUR PASSWORD')
print(auth.access_token)  # print token
print()

api = API(auth)
# import pdb; pdb.set_trace()
accounts = api.accounts()
account = accounts[0]  # Get the first account
print(account.phone_number)  # print the phone number of the first account

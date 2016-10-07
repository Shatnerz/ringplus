"""Example script where every api call is used once."""

# NOTE: This may make changes to your account.
# Do not blindly run.

from __future__ import print_function
from ringplus.auth import OAuthHandler
from ringplus.api import API

from pprint import pprint  # Lets pretty print our output

# Constants
CLIENT_ID = 'CLIENT ID HERE'
CLIENT_SECRET = 'CLIENT SECRET HERE'
REDIRECT_URI = 'REDIRECT URI HERE'


# Setup OAuthHandler for your app
auth = OAuthHandler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# Login and retreive access token
auth.login('andrew.ahlers@gmail.com', 'Timmy0220')
pprint(auth.access_token)
print()
# >>> {'access_token': 'a64d6754621d2d2...',
#      'expires_at': 1475710617.33583,
#      'expires_in': 86400,
#      'refresh_token': 'e30eebb888fabb3e4a...',
#      'token_type': 'bearer'}


# Initialize API with your OAuthHandler
api = API(auth)


# Users are the base object. Each user may have multiple accounts.

# Get a list of Users that we have access to
my_users = api.users()

# Display results
for user in my_users:
    print('email:', user.email)
    print('id:', user.id)
    print('registered_on:', user.registered_on.ctime())
    print('shipping_addresses:', user.shipping_addresses)
    print('Accounts')
    for account in user.accounts:
        print('\t{}'.format(account.name))
    print()


# Get one specific user (same of the objects returned above)
specific_user = api.get_user(user_id=my_users[0].id)


# Get a list of all Accounts that we have access to
my_accounts = api.accounts()
# Note: the above line is equivalent to
# my_accounts = api.user_accounts(user_id=my_user_id)

# Display results
for account in my_accounts:
    print('name: ', account.name)
    print('id:', account.id)
    print('balance:', account.balance)
    print('user_id:', account.user_id)
    print('registered_on:', account.registered_on.ctime())
    print('phone_number:', account.phone_number)
    print()


# Get one specific account
account_id = my_accounts[0].id
specific_account = api.get_account(account_id=account_id)

# Display some of the additional features
print('Specific Account')
print('name:', specific_account.name)
print('Services')
for service in specific_account.account_services:
    print('\t{}'.format(service.name))
print('active_device.model_name:', specific_account.active_device.model_name)
print('voicemail_box.id:', specific_account.voicemail_box.id)
print()


# Get calls from an account
calls = api.calls(account_id=account_id)

# Display top 3 calls
print('Retreived {} calls.'.format(len(calls)))
print('First 3 calls')
for i, call in enumerate(calls[0:3], 1):
    print('Call {}'.format(i))
    print('\tid:', call.id)
    print('\tdirection:', call.direction)
    print('\tfrom:', call.originating_phone_number)
    print('\tto:', call.destination_phone_number)
    print('\tcost:', call.cost)
print()

# Similarly for texts and data
texts = api.texts(account_id=account_id)
data = api.data(account_id=account_id)


# Get Voicemail
mailbox_id = specific_account.voicemail_box.id
voicemail = api.voicemail(voicemail_box_id=mailbox_id)

# Print first voicemail transcription
print("First Message (if available)")
try:
    print(voicemail[0].transcription)
except:
    pass
print()


# # Delete first voicemail
# voicemail_msg_id = voicemail[0].id
# api.delete_voicemail(voicemail_message_id=voicemail_msg_id)


# # Change account name to 'Steve'
# api.update_account(account_id=account_id, name='Steve')
# # Get the updated account object and print the updated name
# specific_account = api.get_account(account_id=account_id)
# print('New name:', specific_account.name)


# TODO
# Register Account examples


# TODO
# Change Device Examples


# TODO
# Change Phone Number Examples
# new_number_request = api.change_phone_number(account_id)


# TODO
# Enforced Carrier Services Examples


# TODO
# Fluid Call Examples


# Bad Request example
# a = api.change_device(account_id=account_id)
# missing required arguments
# Raises RingPlusError: 400 Bad Request
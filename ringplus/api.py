"""API calls for RingPlus."""

from __future__ import print_function

from ringplus.parsers import Parser, ModelParser
from ringplus.binder import bind_api

# for calls that currently dont use binder
from ringplus.error import RingPlusError
import requests


class API(object):
    """RingPlus API.

    :reference: https://docs.ringplus.net/
    """

    def __init__(self, auth_handler=None,
                 host='api.ringplus.net', cache=None,
                 parser=None, version='1', retry_count=0, retry_delay=0,
                 retry_errors=None, timeout=60,
                 wait_on_rate_limit=False, wait_on_rate_limit_notify=False,
                 proxy=''):
        """API instance constructor."""

        self.auth = auth_handler
        self.host = host
        self.cache = cache
        self.parser = parser or ModelParser()
        self.version = version
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = 60
        self.wait_on_rate_limit = wait_on_rate_limit
        self.wait_on_rate_limit_notify = wait_on_rate_limit_notify
        self.proxy = proxy

    # Accounts
    @property
    def user_accounts(self):
        """A list of accounts belonging to a specific user."""
        return bind_api(
            api=self,
            path='/users/{user_id}/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['name', 'email_address', 'phone_number',
                           'device_esn', 'device_iccid', 'page',
                           'per_page'])

    @property
    def accounts(self):
        """List all accounts the user has access to."""
        return bind_api(
            api=self,
            path='/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['name', 'email_address', 'phone_number',
                           'device_esn', 'device_iccid', 'page',
                           'per_page'])

    @property
    def get_account(self):
        """Get a specific account.

        This returns a more detailed account object than those returned in
        API.user_accounts and API.accounts.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            payload_type='account')

    # @property
    # def update_account(self):
    #     """Update an accounts information."""
    #     # dont use bind api for now
    #     return bind_api(
    #         api=self,
    #         path='/accounts/{account_id}',
    #         method='PUT',
    #         allowed_param=['name'])

    def update_account(self, account_id, name):
        """Update an accounts information."""
        path = '/accounts/{account_id}'.format(account_id=account_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token'],
                  'account[name]': name}

        resp = requests.put(fullpath, params=params)
        if resp.status_code != 204:
            raise RingPlusError("Failed to update account.")

    # Account Registration
    # @property
    # def register_account(self):
    #     """Create a registration request to associate a user with a device."""
    #     raise NotImplementedError

    def register_account(self, user_id, name, billing_plan_id, device_esn,
                         device_iccid=None, credit_card_id=None):
        """Create a registration request to associate a user with a device."""
        path = '/users/{user_id}/account_registration_requests'.\
            format(user_id=user_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token'],
                  'account_registration_request[name]': name,
                  'account_registration_request[billing_plan_id]': billing_plan_id,
                  'account_registration_request[device_esn]': device_esn,
                  'account_registration_request[device_iccid]': device_iccid}
        if device_iccid:
            params['account_registration_request[device_iccid]'] = device_iccid
        if credit_card_id:
            params['account_registration_request[credit_card_id]'] = credit_card_id 

        resp = requests.post(fullpath, params=params)
        if resp.status_code == 400 or 401:
            raise RingPlusError("Failed to update account.")

        return resp.json()

    @property
    def register_account_status(self):
        """Get the status on an account registration request."""
        return bind_api(
            api=self,
            path='/account_registration_requests/{request_id}',
            payload_type='request',
            payload_list=True)

    # Change Device
    # @property
    # def change_device(self):
    #     """Create a change device request to change physic device."""
    #     raise NotImplementedError

    def change_device(self, account_id, new_esn, new_iccid=None):
        """Create a change device request to change physic device."""
        path = 'accounts/{account_id}/device_change_requests'.\
            format(account_id=account_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token'],
                  'device_change_request[device_esn]': new_esn}
        if new_iccid:
            params['device_change_request[device_iccid]'] = new_iccid

        resp = requests.post(fullpath, params=params)
        if resp.status_code == 400 or 401:
            raise RingPlusError("Failed to update account.")

        return resp.json()

    @property
    def change_device_status(self):
        """Get the status of a device change request."""
        return bind_api(
            api=self,
            path='/device_change_requests/{request_id}',
            payload_type='request',
            payload_list=True)

    # Change Phone Number
    # @property
    # def change_phone_number(self):
    #     """Creates a request to change the phone number of an Account."""
    #     raise NotImplementedError

    def change_phone_number(self, account_id):
        """Creates a request to change the phone number of an Account."""
        path = '/accounts/{account_id}/phone_number_change_requests'.\
            format(account_id=account_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token']}
        resp = requests.post(fullpath, params=params)
        if resp.status_code == 400 or 401:
            raise RingPlusError("Failed to update account.")

        return resp.json()

    @property
    def change_phone_number_status(self):
        """Get the status of a phone number change request."""
        return bind_api(
            api=self,
            path='/phone_number_change_requests/{request_id}',
            payload_type='request',
            payload_list=True)

    # Enforced Carrier Services
    @property
    def enforced_carrier_services(self):
        """List the applied enforced carrier services of an Account."""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/enforced_carrier_services',
            payload_type='carrier_service',
            payload_list=True,
            allowed_param=['page', 'per_page'])

    # Fluid Call
    @property
    def fluid_call_credentials(self):
        """Get the list of FluidCall credentials."""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/fluidcall_credentials',
            payload_type='fluidcall',
            payload_list=True,
            allowed_param=['page', 'per_page'])

    # Phone Calls
    @property
    def calls(self):
        """Returns an account's paged phone call details."""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_calls',
            payload_type='call',
            payload_list=True,
            allowed_param=['start_date, end_date, per_page, page'])

    # Phone Texts
    @property
    def texts(self):
        """Returns an account's paged phone text details."""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_texts',
            payload_type='text',
            payload_list=True,
            allowed_param=['start_date', 'end_date', 'per_page', 'page'])

    # Phone Data
    @property
    def data(self):
        """Return an account's paged phone data details."""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_data',
            payload_type='data',
            payload_list=True,
            allowed_param=['start_date', 'end_date', 'per_page', 'page'])

    # Users
    @property
    def get_user(self):
        """Return a specific user's details."""
        return bind_api(
            api=self,
            path='/users/{user_id}',
            payload_type='user')

    @property
    def users(self):
        """Return all Users you have access to."""
        return bind_api(
            api=self,
            path='/users',
            payload_type='user',
            payload_list=True,
            allowed_param=['email_address', 'per_page', 'page'])

    # @property
    # def update_user(self):
    #     """Update a User's account."""
    #     raise NotImplementedError

    def update_user(self, user_id, email=None, password=None):
        """Update an accounts information."""
        path = '/users/{user_id}'.format(user_id=user_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token']}
        if email:
            params['user[email]'] = email
        if password:
            params['user[password]'] = password

        resp = requests.put(fullpath, params=params)
        if resp.status_code != 204:
            raise RingPlusError("Failed to update user.")

    # Voicemail Messages
    @property
    def voicemail(self):
        """Return an Account's paged voicemail messages."""
        return bind_api(
            api=self,
            path='/voicemail_boxes/{voicemail_box_id}/voicemail_messages',
            payload_type='voicemail',
            payload_list=True,
            allowed_param=['only_new', 'per_page', 'page'])

    # @property
    # def delete_voicemail(self):
    #     """Deletes a voicemail message."""
    #     raise NotImplementedError

    def delete_voicemail(self, voicemail_message_id):
        """Deletes a voicemail message."""
        path = '/voicemail_messages/{voicemail_message_id}'.\
            format(voicemail_message_id)
        fullpath = 'https://' + self.host + path

        params = {'access_token': self.auth.access_token['access_token']}
        resp = requests.delete(fullpath, **params)

        resp = requests.put(fullpath, params=params)
        if resp.status_code != 204:
            raise RingPlusError("Failed to update account.")

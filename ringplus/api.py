"""API calls for RingPlus."""

from __future__ import print_function

from ringplus.parsers import Parser, ModelParser  # TODO
from ringplus.binder import bind_api  # TODO


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
        """Get a specific account"""
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            payload_type='account')

    @property
    def update_account(self):
        """Update an accounts information."""
        raise NotImplementedError

    # Account Registration
    @property
    def register_account(self):
        """Create a registration request to associate a user with a device."""
        raise NotImplementedError

    @property
    def register_account_status(self):
        """Get the status on an account registration request."""
        raise NotImplementedError

    # Change Device
    @property
    def change_device(self):
        """Create a change device request to change physic device."""
        raise NotImplementedError

    @property
    def change_device_status(self):
        """Get the status of a device change request."""
        raise NotImplementedError

    # Change Phone Number
    @property
    def change_phone_number(self):
        """Creates a request to change the phone number of an Account."""
        raise NotImplementedError

    @property
    def change_phone_number_status(self):
        """Get the status of a phone number change request."""
        raise NotImplementedError

    # Enforced Carrier Services
    @property
    def enforced_carrier_services(self):
        """List the applied enforced carrier services of an Account."""
        raise NotImplementedError

    # Fluid Call
    @property
    def fluid_call_credentials(self):
        """Get the list of FluidCall credentials."""
        raise NotImplementedError

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

    @property
    def update_user(self):
        """Update a User's account."""
        raise NotImplementedError

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

    @property
    def delete_voicemail(self):
        """Deletes a voicemail message."""
        raise NotImplementedError

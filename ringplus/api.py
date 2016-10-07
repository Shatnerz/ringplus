"""API calls for RingPlus."""

from __future__ import print_function

from ringplus.parsers import ModelParser
from ringplus.binder import bind_api


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
        """A list of accounts belonging to a specific user.

        user_id - required
        """
        return bind_api(
            api=self,
            path='/users/{user_id}/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['user_id', 'name', 'email_address',
                           'phone_number', 'device_esn', 'device_iccid',
                           'page', 'per_page'])

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

        account_id - required
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            payload_type='account',
            allowed_param=['account_id'])

    @property
    def update_account(self):
        """Update an accounts information.

        account_id - required

        No content returned
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            method='PUT',
            post_container='account',
            allowed_param=['account_id', 'name'])

    # Account Registration
    @property
    def register_account(self):
        """Create a registration request to associate a user with a device.

        user_id - required
        name - required
        billing_plan_id - required
        device_esn - required
        credit_card_id - required

        device_iccid - optional
        """
        return bind_api(
            api=self,
            path='/users/{user_id}/account_registration_requests',
            method='POST',
            post_container='account_registration_request',
            payload_type='request',
            allowed_param=['user_id', 'name', 'billing_plan_id',
                           'device_esn', 'device_iccid', 'credit_card_id'])

    @property
    def register_account_status(self):
        """Get the status on an account registration request.

        request_id - required
        """
        return bind_api(
            api=self,
            path='/account_registration_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Change Device
    @property
    def change_device(self):
        """Create a change device request to change physic device.

        account_id - required
        device_esn - required - new_esn
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/device_change_requests',
            method='POST',
            post_container='device_change_request',
            payload_type='request',
            allowed_param=['account_id', 'device_esn', 'device_iccid'])

    @property
    def change_device_status(self):
        """Get the status of a device change request.

        request_id - required
        """
        return bind_api(
            api=self,
            path='/device_change_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Change Phone Number
    @property
    def change_phone_number(self):
        """Creates a request to change the phone number of an Account.

        account_id - required
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_number_change_requests',
            method='POST',
            payload_type='request',
            allowed_param=['account_id'])

    @property
    def change_phone_number_status(self):
        """Get the status of a phone number change request.

        request_id - required"""
        return bind_api(
            api=self,
            path='/phone_number_change_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Enforced Carrier Services
    @property
    def enforced_carrier_services(self):
        """List the applied enforced carrier services of an Account.

        account_id - required"""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/enforced_carrier_services',
            payload_type='carrier_service',
            payload_list=True,
            allowed_param=['account_id', 'page', 'per_page'])

    # Fluid Call
    @property
    def fluid_call_credentials(self):
        """Get the list of FluidCall credentials.

        account_id - required"""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/fluidcall_credentials',
            payload_type='fluidcall',
            payload_list=True,
            allowed_param=['account_id', 'page', 'per_page'])

    # Phone Calls
    @property
    def calls(self):
        """Returns an account's paged phone call details.

        account_id - required"""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_calls',
            payload_type='call',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Phone Texts
    @property
    def texts(self):
        """Returns an account's paged phone text details.

        account_id - required
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_texts',
            payload_type='text',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Phone Data
    @property
    def data(self):
        """Return an account's paged phone data details.

        account_id - required"""
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_data',
            payload_type='data',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Users
    @property
    def get_user(self):
        """Return a specific user's details.

        user_id - required"""
        return bind_api(
            api=self,
            path='/users/{user_id}',
            payload_type='user',
            allowed_param=['user_id'])

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
        """Update a User's account.

        user_id - required"""
        return bind_api(
            api=self,
            path='/users/{user_id}',
            method='PUT',
            post_container='user',
            allowed_param=['user_id', 'email', 'password'])

    # Voicemail Messages
    @property
    def voicemail(self):
        """Return an Account's paged voicemail messages.

        voicemail_box_id - required"""
        return bind_api(
            api=self,
            path='/voicemail_boxes/{voicemail_box_id}/voicemail_messages',
            payload_type='voicemail',
            payload_list=True,
            allowed_param=['voicemail_box_id', 'only_new', 'per_page', 'page'])

    @property
    def delete_voicemail(self):
        """Deletes a voicemail message.

        voicemail_message_id - required"""
        return bind_api(
            api=self,
            path='/voicemail_messages/{voicemail_message_id}',
            allowed_param=['voicemail_message_id'],
            method='DELETE')

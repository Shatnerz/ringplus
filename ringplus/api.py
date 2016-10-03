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
                 parser=None, version='1.4', retry_count=0, retry_delay=0,
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

    @property
    def accounts(self):
        """A list of accounts belonging to a specific user."""
        return bind_api(
            api=self,
            path='/users/{user_id}/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['name', 'email_address', 'phone_number',
                           'device_esn', 'device_iccid', 'page',
                           'per_page'])

"""API calls for RingPlus."""

from __future__ import print_function

import requests
from ringplus.parsers import Parser, ModelParser  # TODO
from ringplus.binder import bind_api  # TODO


class API(object):
    """RingPlus API."""

    def __init__(self, auth_handler=None,
                 host='api.host.com', cache=None,
                 parser=None):
        """API instance constructor."""

        self.auth = auth_handler
        self.host = host
        self.cache = cache
        self.parser = parser or ModelParser()
        self.version = 1

    def accounts(self):
        """A list of accounts belonging to a specific user."""
        return bind_api(
            api=self,
            path='users/{user_id}/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['name', 'email_address', 'phone_number',
                           'device_esn', 'device_iccid', 'page',
                           'per_page'])

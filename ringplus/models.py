"""Models for returned RingPlus objects."""

from __future__ import absolute_import
from __future__ import print_function

import iso8601


# Result set probably really isnt needed for ringplus
class ResultSet(list):
    """A list like object that holds results from a RingPlus API query."""
    def __init__(self, max_id=None, since_id=None):
        super(ResultSet, self).__init__()
        self._max_id = max_id
        self._since_id = since_id

    @property
    def max_id(self):
        if self._max_id:
            return self._max_id
        ids = self.ids()
        # Max id is always set to the *smallest* id, minus one,. in the set
        return (min(ids) - 1) if ids else None

    @property
    def since_id(self):
        if self._since_id:
            return self._since_id
        ids = self.ids()
        # Since_id is always set to the *greatest id in the set
        return max(ids) if ids else None

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]


class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']  # do not pickle the API reference
        except KeyError:
            pass
        return pickle

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """ Parse a list of JSON objects into result set of model instances."""
        raise NotImplementedError


class Account(Model):
    """Object that encapsulates a mobile device on a plan."""

    @classmethod
    def parse(cls, api, json):
        if 'account' in json:
            account = Account.parse(api, json['account'])
        else:
            account = cls(api)
            setattr(account, '_json', json)
            for k, v in json.items():
                if k == 'registered_on':
                    setattr(account, k, iso8601.parse_date(v))
                else:
                    setattr(account, k, v)
        return account

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['accounts']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class User(Model):
    """Base object for a user on the system."""

    @classmethod
    def parse(cls, api, json):
        if 'user' in json:
            user = User.parse(api, json['user'])
        else:
            user = cls(api)
            setattr(user, '_json', json)
            for k, v in json.items():
                if k == 'accounts':
                    setattr(user, k, Account.parse_list(api, v))
                elif k == 'registered_on':
                    setattr(user, k, iso8601.parse_date(v))
                else:
                    setattr(user, k, v)
        return user

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['users']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class Voicemail(Model):
    """Voicemail object."""

    @classmethod
    def parse(cls, api, json):
        voicemail = cls(api)
        setattr(voicemail, '_json', json)
        for k, v in json.items():
            if k == 'received_on':
                    setattr(voicemail, k, iso8601.parse_date(v))
            else:
                setattr(voicemail, k, v)
        return voicemail

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['voicemail_messages']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class JSONModel(Model):

    @classmethod
    def parse(cls, api, json):
        return json


class IDModel(Model):

    @classmethod
    def parse(cls, api, json):
        if isinstance(json, list):
            return json
        else:
            return json['ids']


class ModelFactory(object):
    """Used by parsers for creating instances of models.

    You may subclass this factory to add your own extended models.
    """

    user = User
    account = Account
    voicemail = Voicemail

    json = JSONModel
    id = IDModel

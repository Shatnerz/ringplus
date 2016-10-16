.. _getting_started:

***************
Getting Started
***************

Introduction
============

The goal of this tutorial is to get you started with the python wrapper
for the `RingPlus API`_.


Installation
============

Using pip and pypi::

    pip install ringplus

You can also install via::

    pip install git+https://github.com/Shatnerz/ringplus.git

If you plan on making changes to the source, You can install with editable
mode in pip via::

    git clone https://github.com/Shatnerz/ringplus.git

    cd ringplus

    pip install -e .



Checking Voicemail
==================

.. code-block :: python

   import ringplus

   auth = ringplus.OAuthHandler(client_id, client_secret, redirect_uri)
   auth.login(my_username, my_password)

   api = ringplus.API(auth)

   # Get a list of my accounts
   my_accounts = api.accounts()

   # To get the voicemail box id of an account, we need a more
   # detailed account object.
   # Let's examine the first account
   detailed_account = api.get_account(account_id=my_accounts[0].id)

   # Now we can get the voicemail box id and access the voicemail
   mailbox_id = detailed_account.voicemail_box.id
   voicemail = api.voicemail(mailbox_id)

   # Print the transcriptions from the first 3 voicemail.
   for msg in voicemail[0:3]:
       print(msg.transcription)

This example prints the transcriptions of the first three voicemail
messages left on the first account belonging to the given user.
RingPlus utilizes the OAuth2 protocol to receive permission from each user.
See the :ref:`auth_tutorial` for more details about authentication.


API
===

The API class provides access to the entire RingPlus REST API. Each method
can accept various parameters and return responses. For more information
about these methods, please refer to the :ref:`api_reference`.


Models
======

Most API calls will return an instance of a RingPLus model. These models
contain the data returen by RingPlus. For example, the following
will return an Account model::

    # Get a specific account object
    account = api.get_account(account_id=1234)

To access the data attached to a model, simply use::

    print(account.phone_number)
    print(account.balance)


.. _RingPlus API: https://docs.ringplus.net

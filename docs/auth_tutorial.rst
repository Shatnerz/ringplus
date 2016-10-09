.. _auth_tutorial:

***********************
Authentication Tutorial
***********************

Introduction
============

RingPlus supports OAuth2 authentication. Authentication is
handled by the ringplus.OAuthHander class.


OAuth Authentication
====================

To get started, we need to register our application with RingPlus. Naviagate
to "Your Settings > Applications". Here you can Create a new application
and RingPlus will give you a Client ID and Client Secret. Keep these at hand.
Additionally, remember the exact Redirect URI you give to RingPlus, as this
is used in the authentication process. Note that "https://www.ringplus.net"
is not equivalent to "www.ringplus.net" when authenticating.

Next, we must create an OAuthHandler instance using the Client ID,
Client Secret, and Redirect URI associated with the application.::

    auth = ringplus.OAuthHandler(client_id, client_secret, redirect_uri)

In order to start using the API, the following steps to
retrieve an access token must be performed.

#. Direct the user to request RingPlus access.

#. RingPlus redirects the user to our Redirect URI and attached an
    authorization code.

#. Exchange the authorization code for an access token.

To get the authorization URL which to direct our user::

    auth_url = auth.get_authorization_url()

This returns the URL where the user must go to grant our app permission
to access the account.

Once permission has been granted, RingPlus will redirect the user to
the Redirect URI with the authorization code attached as a query.
Using this URL, we can fetch the token simply by::

    auth.fetch_token(final_redirected_url)
    print(auth.token)

The OAuthHandler instance should then be ready to go for API Calls.


Token Expiration and Refreshing
===============================

At this time, all tokens last for 24 hours. Tokens can be refreshed via::

    auth.refresh_token()


Avoiding the Redirect Dance
===========================

If one already knows the username and password to an account, and access
token can be grabbed programmatically without having to explicitly login
each time.::

    auth = ringplus.OAuthHandler(client_id, client_secret, redirect_uri)
    auth.login(username, password)

This method is a little hackish, and may be unreliable if RingPlus makes
changes to their site. There may also be an issue if the user didn't
previously grant access to the app.

"""Contains functions to log in to a Pigeon instance"""
import time
from typing import Any

import attrs

from .api.auth import auth_authenticate_user
from .api.auth import auth_get_csrf
from .api.auth import auth_get_session
from .api.auth import auth_providers_req
from .client import AuthenticatedClient
from .client import Client
from .models import AuthAuthenticateUserAuthenticationRequest as AuthRequest
from .models import AuthGetSessionResponse200


class LoginError(Exception):
    pass


class Login:
    """Mid-level login routines.

    Users wanting to log in to a Pigeon instance will typically use
    :py:func:`pypigeon.login`. The functions in this class are most
    useful if you are working on a specialized Pigeon client that
    predominantly uses :py:mod:`pypigeon.pigeon_core`, or if you are
    working with workflows that do not support interactive login.

    Typical usage::

        from pypigeon.pigeon_core import Client, Login

        # get an unauthenticated client
        client = Client(base_url='https://pigeon.bioteam.net/api/v1')

        # log in with password
        auth_client = Login(client).with_password(username, password)

        # or with session ID
        auth_client = Login(client).with_session_id(session_id)

    """

    def __init__(self, client: Client) -> None:
        """A new Login instance."""
        self.client = client

    def _authenticated_client(self, session_id: str) -> AuthenticatedClient:
        client_attrs: dict[str, Any] = {}
        for attrib in attrs.fields(Client):
            if attrib.alias and attrib.init:
                client_attrs[attrib.alias] = getattr(self.client, attrib.name)
        client_attrs["token"] = session_id

        return AuthenticatedClient(**client_attrs)

    def with_password(self, username: str, password: str) -> AuthenticatedClient:
        """Log in using a username and password.

        Args:
            username (str): the user's username
            password (str): the user's password

        Raises:
            LoginError: if the login could not be completed

        Returns:
            a new Client that has been successfully logged in
        """
        cookie: dict[str, str] = {}
        with self.client as client:
            providers = auth_providers_req.sync(client=client)
            if "credentials" not in providers:
                raise LoginError(
                    f"credentials login not supported at {client._base_url}"
                )

            token = auth_get_csrf.sync(client=client)
            request = AuthRequest(
                user_name=username,
                password=password,
                callback_url="http://null",
                csrf_token=token.csrf_token,
                json=True,
            )
            login_response = auth_authenticate_user.sync_detailed(
                client=client, json_body=request
            )
            if "set-cookie" in login_response.headers:
                cookie.update(
                    dict([login_response.headers["set-cookie"].split("=", 1)])
                )
            else:
                raise LoginError("login failed")

        return self._authenticated_client(list(cookie.values())[0])

    def with_session_id(
        self, session_id: str, wait: bool = False
    ) -> AuthenticatedClient:
        """Log in using an existing session ID.

        You can get a session ID token by calling
        :py:mod:`.api.auth.auth_new_session` and using the
        :py:attr:`~.models.session_token.SessionToken.session_id`
        attribute of the response. To activate the session, the user
        should visit ``/login/activate/<activation_code>`` where
        ``<activation_code>`` is the value of
        :py:attr:`~.models.session_token.SessionToken.activation_code`
        in the response.


        Args:
            session_id (str): an active session ID
            wait (bool): if True, wait for the session to be activated

        Raises:
            LoginError: if the session could not be verified

        Returns:
            a new Client that has been successfully logged in

        """

        logged_in_client = self._authenticated_client(session_id)

        with logged_in_client as client:
            while True:
                session = auth_get_session.sync(client=client)
                if isinstance(session, AuthGetSessionResponse200):
                    break
                elif not wait:
                    raise LoginError("session token could not be verified")

                time.sleep(2)

        return self._authenticated_client(session_id)

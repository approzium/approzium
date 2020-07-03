from contextlib import contextmanager

import approzium
import mysql.connector
from mysql.connector import MySQLConnection

from ..._mysql import get_auth_resp


@contextmanager
def _patch__do_auth(sql_connection_class=MySQLConnection):
    original__do_auth = sql_connection_class._do_auth

    def _do_auth(self, *args, **kwargs):
        if self._password.__class__.__name__ != "AuthClient":
            return

        def _auth_response(
            client_flags,
            username,
            password,
            database,
            auth_plugin,
            auth_data,
            ssl_enabled,
        ):
            authenticator = password
            is_secure_connection = (
                client_flags & mysql.connector.constants.ClientFlag.SECURE_CONNECTION
            )
            auth_response = get_auth_resp(
                authenticator,
                host,
                str(port),
                username,
                auth_plugin,
                auth_data,
                is_secure_connection,
            )
            return auth_response

        host = self.server_host
        port = self.server_port
        self._protocol._auth_response = _auth_response

        res = original__do_auth(self, *args, **kwargs)
        return res

    try:
        sql_connection_class._do_auth = _do_auth
        yield
    finally:
        sql_connection_class._do_auth = original__do_auth


def connect(*args, authenticator=None, **kwargs):
    """Creates a MySQL connector connection through Approzium authentication. Takes
    the same arguments as ``mysql.connector.connect``, in addition to the
    authenticator argument.

    :param authenticator: AuthClient instance to be used for authentication. If
        not provided, the default AuthClient, if set, is used.
    :type authenticator: approzium.AuthClient, optional
    :raises: TypeError, if no AuthClient is given and no default one is set.
    :rtype: ``mysql.connector.MySQLConnection``

    Example:

    .. code-block:: python

        >>> import approzium
        >>> from approzium.mysql.connector import connect
        >>> auth = approzium.AuthClient("myauthenticator.com:6000")
        >>> con = connect(user="bob", host="myhost.com" authenticator=auth)
        >>> # use the connection just like any other MySQL connector connection

    .. warning::
        Currently, only the pure Python MySQL connector implementation is
        supported. Therefore, you have to pass in ``use_pure=True``, otherwise,
        an exception is raised.
    """
    if authenticator is None:
        authenticator = approzium.default_auth_client
    if authenticator is None:
        raise TypeError("Auth client not specified and not default auth client is set")
    kwargs["password"] = authenticator
    use_pure = kwargs.get("use_pure", False)
    if not use_pure:
        msg = "MySQL C-Extension based connection is not currently supported."
        raise NotImplementedError(msg)
    with _patch__do_auth(MySQLConnection):
        conn = mysql.connector.connect(*args, **kwargs)
    return conn

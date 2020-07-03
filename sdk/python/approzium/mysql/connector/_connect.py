from contextlib import contextmanager

import approzium
import mysql.connector
from mysql.connector import MySQLConnection

from ..._mysql import get_auth_resp


class ApproziumMySQLConnection(MySQLConnection):
    def _do_auth(self, *args, **kwargs):
        if self._password.__class__.__name__ == "AuthClient":

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
                    client_flags
                    & mysql.connector.constants.ClientFlag.SECURE_CONNECTION
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

        return super(ApproziumMySQLConnection, self)._do_auth(*args, **kwargs)


@contextmanager
def _patch_MySQLConnection(include_pooling=False):
    mysql.connector.MySQLConnection = ApproziumMySQLConnection
    if include_pooling:
        mysql.connector.pooling.MySQLConnection = ApproziumMySQLConnection
    try:
        yield
    finally:
        mysql.connector.MySQLConnection = MySQLConnection
        if include_pooling:
            mysql.connector.pooling.MySQLConnection = MySQLConnection


def _parse_kwargs(kwargs):
    authenticator = kwargs.pop("authenticator", None)
    if authenticator is None:
        authenticator = approzium.default_auth_client
    if authenticator is None:
        raise TypeError("Auth client not specified and not default auth client is set")
    kwargs["password"] = authenticator
    use_pure = kwargs.get("use_pure", False)
    if not use_pure:
        msg = "MySQL C-Extension based connection is not currently supported.\
Pass use_pure=True"
        raise NotImplementedError(msg)
    return use_pure, authenticator


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
    _parse_kwargs(kwargs)
    with _patch_MySQLConnection():
        conn = mysql.connector.connect(*args, **kwargs)
    return conn

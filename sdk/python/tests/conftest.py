from os import environ

import pytest

import approzium


def pytest_configure():
    determine_authclients()


def determine_authclients():
    """If TEST_ASSUMABLE_ARN is set, adds an additional Approzium AuthClient
    that uses it"""
    authenticatorhosts = ["authenticatorvault", "authenticatorasm"]
    pytest.authclients = []
    for host in authenticatorhosts:
        base_aws_auth = approzium.AuthClient(
            "%s:6001" % host,
            tls_config=approzium.TLSConfig(
                trusted_certs=environ.get("TEST_CERT_DIR") + "/approzium.pem",
                client_cert=environ.get("TEST_CERT_DIR") + "/client.pem",
                client_key=environ.get("TEST_CERT_DIR") + "/client.key",
            ),
            disable_tls=environ.get("APPROZIUM_DISABLE_TLS"),
        )
        pytest.authclients.append(base_aws_auth)
    if environ.get("TEST_ASSUMABLE_ARN"):
        for host in authenticatorhosts:
            role_aws_auth = approzium.AuthClient(
                "%s:6001" % host,
                tls_config=approzium.TLSConfig(
                    trusted_certs=environ.get("TEST_CERT_DIR") + "/approzium.pem",
                    client_cert=environ.get("TEST_CERT_DIR") + "/client.pem",
                    client_key=environ.get("TEST_CERT_DIR") + "/client.key",
                ),
                disable_tls=environ.get("APPROZIUM_DISABLE_TLS"),
            )
            pytest.authclients.append(role_aws_auth)
    else:
        print(
            """Skipping testing using assumable AWS roles because
TEST_ASSUMABLE_ARN is not set"""
        )

#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/

"""
Tests for module settings
"""

import os
from fastapi_oauth_client.settings import OAuthSettings
from unittest import mock


def set_env():
    pass


@mock.patch.dict(os.environ, {
    "OAUTH_SCOPE": "SCOPE",
    "OAUTH_CLIENT_SECRET": "client_secret",
    "OAUTH_CLIENT_ID": "client_id",
    "OAUTH_JWKS_URI": "URI",
    "OAUTH_TOKEN_ENDPOINT": "/token",
    "OAUTH_AUTHORIZATION_ENDPOINT": "/auth",
                              })
def test_settings_env():
    """

    :return:
    """
    settings = OAuthSettings()
    assert settings.oauth_scope == "SCOPE"
    assert settings.oauth_jwks_uri == "URI"
    assert settings.oauth_token_endpoint == "/token"
    assert settings.oauth_authorization_endpoint == "/auth"
    assert settings.oauth_client_id == "client_id"
    assert settings.oauth_client_secret == "client_secret"




def test_settings_no_env():
    """

    :return:
    """
    settings = OAuthSettings()
    assert (settings.oauth_scope == settings.oauth_jwks_uri ==
            settings.oauth_token_endpoint ==
            settings.oauth_authorization_endpoint ==
            settings.oauth_client_secret == settings.oauth_client_id is None)


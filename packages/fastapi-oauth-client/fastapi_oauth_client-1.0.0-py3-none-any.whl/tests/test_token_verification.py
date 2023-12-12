#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/

"""
Tests for module token_verification
"""

from unittest import mock
from unittest.mock import MagicMock

# import RSA
import pytest
from jwt import PyJWKClientError

from fastapi_oauth_client.verify_token import VerifyToken
from Crypto.PublicKey import RSA
import jwt
import datetime


class KeyGenerator:
    """
    Mock class to generate RSA key
    """
    key = RSA.generate(2048)


class FakeSettings:
    """
    A simple class to mock the Settings object
    """
    oauth_jwks_uri = "https://google.com"
    oauth_client_id = "test"


@pytest.fixture
def key_gen(request):
    """

    :param request:
    :return:
    """
    key_gen = KeyGenerator()

    return key_gen


@pytest.fixture
def payload(request):
    """

    :param request:
    :return:
    """
    return {"preferred_username": "tester", "roles": ["admin"]}


@pytest.fixture
def token(request, key_gen, payload):
    """

    :param request:
    :param key_gen:
    :param payload:
    :return:
    """
    key = KeyGenerator.key
    private_key = key.export_key('PEM').decode()
    encoded = jwt.encode(
        payload,
        private_key,
        headers={
            "aud": FakeSettings.oauth_client_id,
            "azp": FakeSettings.oauth_client_id,
            "exp": (datetime.datetime.now() + datetime.timedelta(seconds=100)).timestamp(),
        },
        algorithm="RS256",
    )
    return encoded


def test_get_signing_key(key_gen):
    """
    Test get_signing_key operation: Make sure the VerifyToken class uses the
    JWKSClient to obtain the RSA key
    :param key_gen:
    :return:
    """
    with mock.patch("fastapi_oauth_client.settings.OAuthSettings") as settings:
        settings.side_effect = FakeSettings

        token_verifier = VerifyToken(token="124")
        token_verifier.jwks_client = MagicMock()

        # Create mock method jwks_client.get_signing_key_from_jwt and return
        # KeyGenerator mock object
        token_verifier.jwks_client.get_signing_key_from_jwt.side_effect = [key_gen]

        token_verifier.get_signing_key()
        key = token_verifier.signing_key

        assert key == key_gen.key


def test_decode(key_gen, token, payload):
    """
    Test whether decode_token operation works as expected. We feed a token,
    a RSA Key, a mock config and check whether the token gets decoded
    successfully
    :param key_gen:
    :param token:
    :param payload:
    :return:
    """

    # Get a RSA key to decode and encode a token
    key = key_gen.key

    payload = {"preferred_username": "tester", "roles": ["admin"]}

    with mock.patch("fastapi_oauth_client.settings.OAuthSettings") as settings:
        settings.side_effect = FakeSettings

        # Create VerifyToken object
        token_verifier = VerifyToken(token=token)

        # Set public key as signing key
        token_verifier.signing_key = key.public_key().export_key()

        # Run decode_token
        profile = token_verifier.decode_token()

        assert profile == payload


def test_verify_roles_success(token):
    roles = ["viewer", "admin"]
    user_roles = ["admin", "editor"]

    token_verifier = VerifyToken(token=token)
    result = token_verifier.verify_roles(roles, user_roles)
    assert result is True


def test_verify_roles_error(token):
    """

    """
    roles = ["viewer", "admin"]
    user_roles = ["editor", "owner"]

    token_verifier = VerifyToken(token=token)
    result = token_verifier.verify_roles(roles, user_roles)
    assert result is False

    """
    with mock.patch("fastapi_oauth_client.settings.OAuthSettings") as settings:
        token_verifier = VerifyToken(token=token)
        assert token_verifier.verify_roles(roles, user_roles) == False
    """

def test_verify_roles_no_roles_required(token):
    """

    """
    roles = []
    user_roles = ["editor", "owner"]

    token_verifier = VerifyToken(token=token)
    result = token_verifier.verify_roles(roles, user_roles)
    assert result is True



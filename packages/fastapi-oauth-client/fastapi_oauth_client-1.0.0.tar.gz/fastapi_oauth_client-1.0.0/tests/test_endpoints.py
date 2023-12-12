#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/

"""
Tests for module endpoints
"""

import datetime
import json
import os
import secrets
from unittest import mock
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware

from fastapi_oauth_client.endpoints import oauth, auth_router, token_auth_scheme, verify_token


class OAuthAsyncMock(AsyncMock):
    """
    A mock class required to mock the functions for OAuth
    """

    token = {"expires_at": datetime.datetime(day=23, month=12, year=2023, hour=0, minute=0, second=0).timestamp(),
                "access_token": "124325346"}
    call_list = []

    async def authorize_access_token(self, request):
        """

        :param request:
        :return:
        """
        return self.token

    async def authorize_redirect(self, request, redirect_uri):
        """

        :param request:
        :param redirect_uri:
        :return:
        """
        self.call_list += [(request, redirect_uri)]
        return "success"


@pytest.fixture
def app(request):
    """

    :param request:
    :return:
    """
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(16))

    app.include_router(auth_router)
    return app

@pytest.fixture
def client(request, app):
    """

    :param request:
    :param app:
    :return:
    """

    client = TestClient(app)
    return client

@mock.patch.dict(os.environ, {
    "OAUTH_SCOPE": "SCOPE",
    "OAUTH_CLIENT_SECRET": "client_secret",
    "OAUTH_CLIENT_ID": "client_id",
    "OAUTH_JWKS_URI": "URI",
    "OAUTH_TOKEN_ENDPOINT": "/token",
    "OAUTH_AUTHORIZATION_ENDPOINT": "/auth",
                              })

def test_protected_endpoint_fail(app, client):
    """

    :return:
    """

    @app.get("/protected")
    def endpoint(token: str = Depends(token_auth_scheme),
            profile= Depends(verify_token(roles=["admin"]))):
        return {"status": "HelloWorld"}

    with mock.patch("fastapi_oauth_client.endpoints.VerifyToken") as auth:
            response = client.get("/protected", headers={"Authorization": "Bearer 124"})

            assert response.status_code == 401



def test_protected_endpoint_fail_error_status(app, client):
    """

    """
    @app.get("/protected")
    def endpoint(token: str = Depends(token_auth_scheme),
            profile= Depends(verify_token(roles=["admin"], ))):
        return {"status": "error"}

    with mock.patch("fastapi_oauth_client.endpoints.VerifyToken.verify") as auth:
        auth.side_effect = [{"status": "error", "message": "Error message"}]

        client = TestClient(app)
        response = client.get("/protected", headers={"Authorization": "Bearer 124"})

    assert response.status_code == 401
    assert response.json() == {"detail": {"status": "error", "message": "Error message"}}


def test_protected_endpoint_success(app, client):
    """

    :return:
    """
    class FakeTokenVerifyer():
        def __init__(self, *args, **kwargs):
            pass
        def verify(self, roles: str):
            return {"preferred_username": "Tester"}
    @app.get("/protected")
    def endpoint(token: str = Depends(token_auth_scheme),
            profile= Depends(verify_token(roles=["admin"]))):
        return profile

    with mock.patch("fastapi_oauth_client.endpoints.VerifyToken") as auth:
            auth.side_effect = FakeTokenVerifyer
            response = client.get("/protected", headers={"Authorization": "Bearer 124"})

            assert response.status_code == 200
            assert response.json() == {"preferred_username": "Tester"}


def test_login(client):
    """

    :param client:
    :return:
    """

    with mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock) as auth:
        response = client.get("/login")
        assert len(auth.call_list) == 1

        # Assert call request to /login was sent to 'authorize_redirect'
        assert auth.call_list[0][0].url == 'http://testserver/login'

        # Assert redirect_uri was correct
        assert auth.call_list[0][1] == 'http://testserver/callback'

    assert response.json() == "success"


def test_callback(client):
    """

    :return:
    """
    with mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock) as auth:

        response = client.get("/callback")

        assert response.status_code == 200

@mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock)
def test_callback_invalid_token(auth, client):
    """

    :return:
    """

    # Empty response
    with mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock) as auth:
        auth.token = {}
        response = client.get("/callback")
        assert response.status_code == 401

    # access_token not received
    with mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock) as auth:
        auth.token = {'expires_at': '2023-12-23T00:00:00'}
        response = client.get("/callback")
        assert response.status_code == 401

    # expires_at not received
    with mock.patch.object(oauth, attribute="keycloak", new_callable=OAuthAsyncMock) as auth:
        auth.token = {'access_token': '124325346'}

        response = client.get("/callback")
        assert response.status_code == 401

#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/
"""
The OAuth component and the required endpoints for login to IdP
"""
import logging
from datetime import datetime

import fastapi
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer

from .resources.success_template import template, token_template, explanation
from .settings import OAuthSettings
from .verify_token import VerifyToken
from fastapi.responses import HTMLResponse

logger = logging.getLogger(__name__)

auth_router = APIRouter()
config = OAuthSettings()
oauth = OAuth()
oauth.register(
    name='keycloak',
    client_id=config.oauth_client_id,
    client_secret=config.oauth_client_secret,
    authorize_url=config.oauth_authorization_endpoint,
    access_token_url=config.oauth_token_endpoint,
    jwks_uri=config.oauth_jwks_uri,
    client_kwargs={
        'scope': config.oauth_scope
    }
)

token_auth_scheme = HTTPBearer()


class verify_token:
    """
    Class for auth decorator
    """
    def __init__(self, roles: list = None):
        self.roles = roles

    def __call__(self,
                 token: fastapi.security.http.HTTPAuthorizationCredentials = Depends(
                     token_auth_scheme)):
        """

        :param token:
        :return:
        """
        logger.debug("Attempting authorisation")
        profile = VerifyToken(token=token.credentials).verify(roles=self.roles)
        if not isinstance(profile, dict):
            raise HTTPException(401, {"status": "error",
                  "message": "Unexpected response from Token verification"})
        if "status" in profile.keys() and profile.get("status") == "error":
            raise HTTPException(401, profile)

        return profile


@auth_router.get("/login")
async def login(request: Request):
    """
    Login route. Simply forwards user to the IdP
    :param request:
    :return:
    """
    logger.debug("Redirecting to IdP")
    redirect_uri = request.url_for('callback')
    return await oauth.keycloak.authorize_redirect(request, redirect_uri)


@auth_router.get("/callback")
async def callback(request: Request):
    """
    The callback route that is called after login in IdP
    :param request:
    :return:
    """
    logger.debug("Returned from IdP and attempting to request access "
                 "token from IdP.")
    token = await oauth.keycloak.authorize_access_token(request)
    logger.debug("Received access token from IdP")

    if token.get("access_token"):
        access_token = token.get('access_token')
    else:
        raise HTTPException(401,
                            detail="Received invalid response from Identity provider during login")

    # Missing expiry
    if not 'expires_at' in token.keys():
        logger.warning(
            "Received access token from IdP that does NOT contain expires_at claim!")
        raise HTTPException(
            401,
            detail="Received invalid response from Identity provider during login"
        )

    expiry = datetime.fromtimestamp(token.get('expires_at'))

    return HTMLResponse(template + token_template.format(token=access_token, expires=expiry) + explanation)


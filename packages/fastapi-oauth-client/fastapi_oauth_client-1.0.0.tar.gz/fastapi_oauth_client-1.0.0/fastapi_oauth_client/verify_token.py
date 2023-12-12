#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/
"""
This module contains code for token verification and profile extraction from JWT
tokens
"""
import logging

import jwt
from jwt.exceptions import InvalidTokenError

from .settings import OAuthSettings

logger = logging.getLogger(__name__)


class VerifyToken:
    """Does all the token verification using PyJWT"""

    signing_key = None

    def __init__(self, token):
        """

        :param token: The token
        """
        self.token = token
        self.config = OAuthSettings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        self.jwks_client = jwt.PyJWKClient(self.config.oauth_jwks_uri)

    def decode_token(self):
        """
        Decode an actual token
        :return:
        """
        payload = jwt.decode(
            self.token,
            self.signing_key,
            algorithms=["RS256"],
            audience=self.config.oauth_client_id,
            options={'verify_aud': False, 'verify_exp': True}
            # Skip 'audience' because the
            # actual audience is in azp for Keycloak
        )

        return payload

    def verify_roles(self, roles, user_roles):
        """

        :param roles:
        :param user_roles:
        :return:
        """
        permitted = False

        logger.debug("Attempting role check")
        if roles:
            for role in roles:
                if role in user_roles:
                    permitted = True
                    break
        else:  # No roles required for endpoint
            permitted = True

        return permitted

    def get_signing_key(self):
        """

        :return:
        """

        try:
            logger.debug("Attempting to load Signing key 'kid' from token and "
                         "verify via JWKS URL")
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key

            return {}
        except jwt.exceptions.PyJWKClientError as error:
            logger.debug(f"PyJWKClientError during Authorisation: "
                         f"'{str(error)}'")
            return {"status": "error", "msg": str(error)}
        except jwt.exceptions.DecodeError as error:
            logger.debug(f"DecodeError during Authorisation: '{str(error)}'")
            return {"status": "error", "msg": str(error)}

    def verify(self, roles: list = None):
        """
        Main entry point
        Decode and Verify the token against the roles (optional).
        This function uses the actual keys from the OAuth IdP instance to verify
        that the received token is legit and valid.
        :param roles:
        :return:
        """
        # This gets the 'kid' from the passed token
        error = self.get_signing_key()

        if error:
            return error

        try:
            logger.debug("Attempting to load payload from token")
            payload = self.decode_token()

        except InvalidTokenError as exception:
            logger.info(f"Error decoding token: '{str(exception)}'")
            return {"status": "error", "message": str(exception)}

        # Verify roles
        user_roles = payload.get("roles", [])
        permitted = self.verify_roles(roles=roles, user_roles=user_roles)

        if not permitted:
            logger.error(f"User '{payload.get('preferred_username')}' tried "
                         f"to access endpoint but did not have required "
                         f"role assignment.")
            return {"status": "error", "message": "You are not authorized "
                                                  "to access this endpoint"}

        return payload

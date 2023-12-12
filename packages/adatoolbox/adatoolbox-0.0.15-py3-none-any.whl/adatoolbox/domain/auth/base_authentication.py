import jwt
import json
from loguru import logger
from rest_framework import authentication, exceptions
from adatoolbox.domain.auth import settings
from adatoolbox.domain.memory.memory import Memory


class User:
    def __init__(self, input):
        self.__dict__.update(input)


class Authentication(authentication.BaseAuthentication):
    """Auth Api Authentication Class."""

    def authenticate(
            self: "Authentication", request) -> tuple:
        
        http_authorizaton = request.META.get("HTTP_AUTHORIZATION")

        if not http_authorizaton or "Bearer" not in http_authorizaton:
            raise exceptions.ValidationError({"detail": "Bearer or Authorization header not found."})
        
        try:
            token = jwt.decode(
                http_authorizaton.split(' ')[1],
                settings.AUTHENTICATION_API_SECRET_KEY,
                algorithms=["HS256"])
        except Exception as error:
            logger.error(error)
            raise exceptions.ValidationError({"detail": "Invalid Token."})
        
        try:
            user = Memory.get('user_{}'.format(token.get('user_id')))
        except Exception as error:
            logger.error(error)
            raise exceptions.ValidationError(
                {"detail": "We are having an authentication problem. Please try again later."})

        return json.loads(user, object_hook = User), http_authorizaton.split(' ')[0] if len(http_authorizaton.split(' ')) > 0 else None


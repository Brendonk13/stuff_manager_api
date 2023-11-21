import datetime
from datetime import datetime

# https://lucasleite-us.medium.com/integrating-clerk-with-django-rest-framework-e1e2f041dba2

# Note: found this which is diff from this
# https://github.com/clerk/django-example

# interesting, users are created in db automatically once they make their first request after signing up from the frontend

import jwt
# import pytz
import requests
from ..models import User
from django.core.cache import cache
from jwt.algorithms import RSAAlgorithm
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
from os import environ as env
from ninja.security import HttpBearer
import aiohttp
import asyncio

load_dotenv()

CLERK_API_URL = "https://api.clerk.com/v1"
CLERK_FRONTEND_API_URL = env["CLERK_FRONTEND_API_URL"]
CLERK_SECRET_KEY = env["CLERK_SECRET_KEY"]
CACHE_KEY = "jwks_data"

class AuthenticationFailed(Exception):
    pass

class ClerkBearerAuth(HttpBearer):
    async def authenticate(self, request, token: str):

        print("before decode")
        user = await self.decode_jwt(token)
        print("after decode")
        if not user:
            return None

        clerk = ClerkSDK()
        clerk_user_info, found_clerk_user_from_id = await clerk.fetch_user_info(user.clerk_id)
        print("after")
        # save new information thats stored in clerk ??
        # print(f"user info: {clerk_user_info}")
        if found_clerk_user_from_id:
            user.email = clerk_user_info["email_address"]
            # user.last_login = clerk_user_info["last_login"]
            await user.asave()
        return user, None


    async def decode_jwt(self, token):
        clerk = ClerkSDK()
        jwks_data = clerk.get_jwks()
        public_key = RSAAlgorithm.from_jwk(jwks_data["keys"][0])
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.DecodeError:
            raise AuthenticationFailed("Token decode error.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        clerk_user_id = payload.get("sub")
        if clerk_user_id:
            # user, created = await User.objects.get_or_create(clerk_id=clerk_user_id)
            user, created = await User.objects.aget_or_create(clerk_id=clerk_user_id)
            return user
            # return None
        return None

class ClerkSDK:
    async def fetch_user_info(self, user_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{CLERK_API_URL}/users/{user_id}", headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},) as response:

                # response = requests.get(
                #     f"{CLERK_API_URL}/users/{user_id}",
                #     headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
                # )
                if response.status == 200:
                    data = await response.json()
                    return {
                        "email_address": data["email_addresses"][0]["email_address"],
                        # "first_name": data["first_name"],
                        # "last_name": data["last_name"],
                        # "last_login": datetime.datetime.fromtimestamp(
                        #     data["last_sign_in_at"] / 1000, tz=pytz.UTC
                        # ),
                    }, True
                else:
                    return None, False

    def get_jwks(self):
        jwks_data = cache.get(CACHE_KEY)
        if jwks_data:
            return jwks_data

        response = requests.get(f"{CLERK_FRONTEND_API_URL}/.well-known/jwks.json")
        if response.status_code == 200:
            jwks_data = response.json()
            cache.set(CACHE_KEY, jwks_data)  # cache indefinitely
        else:
            raise AuthenticationFailed("Failed to fetch JWKS.")
        return jwks_data

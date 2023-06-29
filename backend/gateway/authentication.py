import jwt
from django.conf import settings
from datetime import datetime, timedelta
import random
import string
from rest_framework.authentication import BaseAuthentication
from customuser.models import Customuser

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class Get_token():
    @staticmethod
    def get_access_token(payload):
        return jwt.encode(
            {
                "exp": datetime.now() + timedelta(minutes=10), **payload
            },
            settings.SECRET_KEY,
            algorithm = 'HS256'
        )
    
    @staticmethod
    def get_refresh_token():
        return jwt.encode(
            {"exp": datetime.now() + timedelta(days=5)},
            settings.SECRET_KEY,
            algorithm = "HS256"
        )
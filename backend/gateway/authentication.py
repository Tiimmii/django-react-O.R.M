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
    

class Authentication(BaseAuthentication):
    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None
        print(data["user"])
        return self.get_user(data["user"]), None
    
    def get_user(self, user_id):
        try:
            user = Customuser.objects.get(id = user_id)
            return user
        except Exception:
            return None
        
    def validate_request(self, headers):
        authorization = headers.get("Authorization", None)
        if not authorization:
            raise Exception("You need to provide authorization")
        token = headers["Authorization"][7:]
        decoded_data = authorization.valid_token(token)
        if not decoded_data:
            raise Exception("Token not valid or expired you may need to login again")
        return decoded_data
    
    @staticmethod
    def valid_token(token):
        try:
            decoded_data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithm = "HS256",
            )
        except Exception:
            return None
        
        if datetime.now() > decoded_data["exp"]:
            return None
        
        return decoded_data
import jwt
import os
from time import time
import json
from supersecretserver import CLIENT_SECRET, CLIENT_KEY


def generate_jwt():
    return {
        "statusCode": 200,
        "token": "Bearer "+jwt.encode(
            {
                "aud": None,
                "iss": CLIENT_KEY,
                "exp": int(time())+ 90 * 86400,
                "iat": int(time())
            }, CLIENT_SECRET
        ).decode('utf-8')
    }

if __name__ == "__main__":
    print(generate_jwt())
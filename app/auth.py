from app import(
    app
)
from functools import wraps
from flask import(
    request,
    render_template
)
import jwt



def validate_token(token):
    try:
        token_dec = jwt.decode(token, app.config.get('MASTER_KEY', '123456'), algorithms=["HS256"])
        if token_dec:
            return token_dec
    except Exception as err:
        print(f'validate_token exp - {err}')
    return False



def retrieve_token(request):
    try:
        token_cookie = request.cookies.get('access_token', False)
        token = request.headers.get('Authorization', None)
        if not token and not token_cookie:
            return False
        elif not token:
            return validate_token(token_cookie)
        elif not token_cookie:
            return validate_token(token)
        elif token == token_cookie:
            return validate_token(token)
    except Exception as err:
        print(f'retrieve_token exp - {err}')
    return False


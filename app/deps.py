from app import(
    app
)
from functools import wraps
from flask import(
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
    url_for
)

from app.auth import(
    validate_token,
    retrieve_token
)

from app.exceptions import(
    PermissionDenied,
    PermissionDeniedAPI,
    AuthenticationRequired
)

def check_authenticated_user():
    def _check_authenticated_user(f):
        @wraps(f)
        def __check_authenticated_user(*args, **kwargs):
            temp_token = retrieve_token(request=request)
            if not temp_token:
                raise AuthenticationRequired("Authentication Required")
            return f(*args, **kwargs)
        return __check_authenticated_user
    return _check_authenticated_user

def check_jwt_token():
    def _check_jwt_token(f):
        @wraps(f)
        def __check_jwt_token(*args, **kwargs):
            temp_token = retrieve_token(request=request)
            if not temp_token:
                raise PermissionDenied("Permission denied")
            return f(*args, **kwargs)
        return __check_jwt_token
    return _check_jwt_token

def check_jwt_admin():
    def _check_jwt_admin(f):
        @wraps(f)
        def __check_jwt_admin(*args, **kwargs):
            temp_token = retrieve_token(request=request)
            if not temp_token:
                raise PermissionDenied("Permission denied")
            if not temp_token.get('admin', False):
                raise PermissionDenied("Permission denied")
            return f(*args, **kwargs)
        return __check_jwt_admin
    return _check_jwt_admin

def api_check_jwt_admin():
    def _api_check_jwt_admin(f):
        @wraps(f)
        def __api_check_jwt_admin(*args, **kwargs):
            temp_token = retrieve_token(request=request)
            if not temp_token:
                raise PermissionDeniedAPI("Permission denied")
            if not temp_token.get('admin', False):
                raise PermissionDeniedAPI("Permission denied")
            return f(*args, **kwargs)
        return __api_check_jwt_admin
    return _api_check_jwt_admin

def render_plus(template_string, **context):
    extra = {
        'request': request,
        'cookies': request.cookies,
        'authenticated': False,
        'user_data': {}
    }
    token_data = retrieve_token(request=request)
    if token_data:
        extra.update(
            {
                'authenticated': True,
                'user_data': token_data
            }
        )
    return render_template(template_string, **context, **extra)
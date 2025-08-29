from app import(
    app
)
from functools import wraps
from flask import(
    request,
    render_template,
    jsonify,
    make_response
)
import jwt

from app.auth import(
    validate_token,
    retrieve_token
)

from app.deps import(
    render_plus
)

from app.exceptions import(
    PermissionDenied,
    PageNotFound,
    PermissionDeniedAPI,
    APIUserAlreadyExists,
    MissingParams,
    UsernameOrPasswordInvalid,
    UserInactive,
    AuthenticationRequired,
    DisciplinaAlreadyExists
)

@app.errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return render_plus("base/base-403.html"), 403

@app.errorhandler(PermissionDeniedAPI)
def handle_permission_denied_api(error):
    return jsonify(error=True, message='Permission Denied'), 403
    return render_plus("base/base-403.html"), 403

@app.errorhandler(PageNotFound)
@app.errorhandler(404)
def page_not_found(error):
    return render_plus("base/base-404.html"), 404

@app.errorhandler(APIUserAlreadyExists)
def handle_user_already_exists_api(error):
    return jsonify(error=True, message='Nome de usu&aacute;rio ou e-mail j&aacute; cadastrados!'), 400

@app.errorhandler(MissingParams)
def handle_missing_params_api(error):
    return jsonify(error=True, message='Param&ecirc;tros insuficientes'), 400

@app.errorhandler(UsernameOrPasswordInvalid)
def handle_user_password_invalid_api(error):
    return jsonify(error=True, message='Nome de usu&aacute;rio/e-mail ou senha incorretos'), 400

@app.errorhandler(UserInactive)
def handle_inactive_user_api(error):
    return jsonify(error=True, message="Usu&aacute;rio inativo"), 400

@app.errorhandler(AuthenticationRequired)
def handle_authentication_required(error):
    resp = make_response()
    resp.headers['Location'] = '/login'
    return resp, 302

@app.errorhandler(DisciplinaAlreadyExists)
def handle_disciplina_already_exists(error):
    resp = make_response()
    resp.headers['Location'] = 'URL USANDO O ID DA CONSULTA'
    return resp, 302
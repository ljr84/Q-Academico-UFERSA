from app import(
    app,
    db
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

from app.models.sistema import(
    Disciplina,
    Assunto,
    Usuario
)

from app.core.database import SessionLocal

from app.deps import(
    check_authenticated_user,
    check_jwt_token,
    check_jwt_admin,
    render_plus
)

from app.exceptions import(
    PageNotFound,
    AuthenticationRequired
)

#SITE

@app.route('/')
@app.route('/index')
@app.route('/panel/home')
@app.route('/panel/index')
def home_page():
    return render_plus('panel/educasoft/home.html')
    return render_template('base/base.html')
    # return render_template('panel/home.html')

@app.route('/panel/materia/listar')
def listar_materias():
    return render_plus('panel/educasoft/materia-listar.html')

@app.route('/panel/materia/create')
@check_authenticated_user()
@check_jwt_admin()
def materia_create():
    return render_plus('panel/educasoft/materia-create.html')

@app.route('/panel/materia/<int:id>/view')
def materia_view(id):
    data_materia = Disciplina.list_by_id(session=SessionLocal(), id=id)
    if not data_materia:
        raise PageNotFound('Page not found')
    return render_plus('panel/educasoft/materia-view.html', id=id, data=data_materia)

@app.route('/panel/materia/<int:id>/edit')
@check_authenticated_user()
@check_jwt_admin()
def materia_edit(id):
    data_materia = Disciplina.list_by_id(session=SessionLocal(), id=id)
    if not data_materia:
        raise PageNotFound('Page not found')
    return render_plus('panel/educasoft/materia-edit.html', id=id, data=data_materia)


#ASSUNTO !

@app.route('/panel/materia/<int:id>/assunto/create')
@check_authenticated_user()
@check_jwt_admin()
def materia_assunto_create(id):
    return render_plus('panel/educasoft/materia-assunto-create.html', id=id)


@app.route('/panel/materia/assunto/<int:id_assunto>/edit')
@check_authenticated_user()
@check_jwt_admin()
def materia_assunto_edit(id_assunto):
    data_assunto = Assunto.list_by_id(session=SessionLocal(), id=id_assunto)
    if not data_assunto:
        raise PageNotFound('Page not found')
    return render_plus('panel/educasoft/materia-assunto-editar.html', id=id_assunto, data=data_assunto)

@app.route('/panel/materia/assunto/<int:id_assunto>/view')
def materia_assunto_view(id_assunto):
    return render_plus('panel/educasoft/materia-assunto-ver.html', id=id_assunto)


@app.route('/panel/materia/assunto/<int:id_assunto>/respostas')
def materia_assunto_view_resposta(id_assunto):
    return render_plus('panel/educasoft/materia-assunto-ver.html', id=id_assunto, view_respostas=1)





#QUESTAO


@app.route('/panel/materia/assunto/<int:id>/question/create')
@check_authenticated_user()
@check_jwt_admin()
def materia_assunto_question_create(id):
    return render_plus('panel/educasoft/materia-assunto-questao-create.html', id=id)


@app.route('/panel/materia/assunto/questao/<int:id_questao>/edit')
@check_authenticated_user()
@check_jwt_admin()
def materia_assunto_question_edit(id_questao):
    return render_plus('panel/educasoft/materia-assunto-questao-editar.html', id=id_questao)


#ADMIN

@app.route('/panel/admin/user/listar')
@check_authenticated_user()
@check_jwt_admin()
def listar_usuarios():
    return render_plus('panel/admin/user-list.html')


@app.route('/panel/admin/user/create')
@check_authenticated_user()
@check_jwt_admin()
def usuario_create():
    return render_plus('panel/admin/user-create.html')


@app.route('/panel/admin/user/<int:id_user>/edit')
@check_authenticated_user()
@check_jwt_admin()
def usuario_edit(id_user):
    return render_plus('panel/admin/user-edit.html', id=id_user)



# @app.errorhandler(403)
# def page_not_permitted(error):
#     return render_template("base/base-403.html"), 403


# @app.errorhandler(PermissionDenied)
# def handle_permission_denied(error):
#     print("PermissionDenied Exception Raised")
#     print(request.cookies)
#     print(request.headers)
#     print("PermissionDenied---------- Exception Raised")
#     return render_template("base/base-403.html"), 403




# @app.route('/quiz')
# def quiz_page():
#     return render_template('panel/quiz.html')



# @app.route('/quiz/<int:id>')
# def quiz_responder(id):
#     return render_template('panel/quiz-responder.html', id=id)


# @app.route('/view/materia/index')
# @app.route('/view/materia/list')
# def materia_list():
#     #return render_template('panel/materia.html')
#     return render_template('panel/materia-modulos.html')


# @app.route('/view/materia/create')
# def materia_create():
#     return render_template('panel/materia-create.html')


# @app.route('/view/materia/<int:id>/view')
# @app.route('/view/materia/<int:id>/edit')
# def materia_edit(id):
#     return render_template('panel/materia-edit.html', id=id)


# @app.route('/view/materia/<int:id>/create-question')
# def materia_question_create(id):
#     return render_template('panel/materia-question-create.html', id=id)


# @app.route('/register')
# def register():
#     return render_template('base/base_register.html')


@app.route('/login')
def login():
    return render_template('base/base_login.html')


@app.route('/register')
def register():
    return render_template('base/base_register.html')


@app.route('/logout')
def logout():
    response = make_response()
    response.set_cookie('access_token', '')
    response.headers['Location'] = '/'
    return response, 302
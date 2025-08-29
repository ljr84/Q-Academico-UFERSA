
from app import(
    app,
    db
)
from flask import(
    render_template,
    request,
    jsonify,
    make_response,
    Response
)
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal


from app.models.sistema import(
    Disciplina,
    Assunto,
    Pergunta,
    UsuarioGrupo,
    Usuario,
    Quiz,
    QuizResposta
)

import jwt
import json
from app.deps import(
    check_jwt_token,
    check_jwt_admin,
    api_check_jwt_admin,
    check_authenticated_user
)

from app.auth import(
    validate_token,
    retrieve_token
)

from app.exceptions import(
    MissingParams,
    UsernameOrPasswordInvalid,
    UserInactive
)



@app.route('/api/materia/list', methods=["GET"])
def api_materia_list():
    temp = Disciplina.list_all(session=SessionLocal())
    if temp:
        data = []
        for item in temp:
            data.append({
                'id': item.id,
                'name': item.name,
                'icon': item.icon,
                'description': item.description,
                'total': len(item.assuntos),
                'date_created': item.date_created
            })
        return jsonify(error=False, data=data)
    else:
        return jsonify(error=True, message='no return')


#


@app.route('/api/materia/create', methods=["POST"])
@check_authenticated_user()
def api_materia_create():
    if request.method == "POST":
        name = request.form['name']
        icon = request.form['icon']
        description = request.form["description"]
        temp = Disciplina.create(session=SessionLocal(), data={
            'name': name,
            'icon': icon,
            "description": description
        })
        if temp:
            if isinstance(temp, int):
                return jsonify(error=True, code='EXISTS', message='Disciplina j&aacute; cadastrada, redirecionando...', id=temp), 400
            data_out = {
                'id': temp.id,
                'name': temp.name,
                'icon': temp.icon,
                'description': temp.description,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify(error=True, message="aplicacao falhou criar materia"), 400
    return jsonify(error=True)



@app.route('/api/materia/<int:id_disciplina>')
def api_materia_view(id_disciplina):
    temp = Disciplina.list_by_id_moar(session=SessionLocal(), id=id_disciplina)
    if temp:
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404





@app.route('/api/materia/<int:id_disciplina>/edit', methods=["POST"])
def api_materia_edit(id_disciplina):
    if request.method == "POST":
        name = request.form.get("name", None)
        description = request.form.get("description", None)
        icon = request.form.get("icon", None)
        if name or description:
            ss = SessionLocal()
            temp = Disciplina.list_by_id(session=ss, id=id_disciplina)
            if temp:
                if name:
                    temp.name = name
                if description:
                    temp.description = description
                if icon:
                    temp.icon = icon
                ss.commit()
                return jsonify(error=False, data=temp)
            else:
                return jsonify(error=True, message='not found'), 404
        else:
            return jsonify(error=True, message='not found'), 404
    else:
        return jsonify(error=True, message='not found'), 404






@app.route('/api/materia/<int:id_disciplina>/delete', methods=["DELETE"])
def api_materia_delete(id_disciplina):
    session = SessionLocal()
    temp = Disciplina.list_by_id(session=session, id=id_disciplina)
    if temp:
        if len(temp.assuntos)>0:
            return jsonify(error=True, message="Voce precisa deletar as questoes do assunto antess]"), 400
        else:
            try:
                session.delete(temp)
                session.commit()
                return jsonify(error=False), 204
            except Exception as err:
                return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404
    
            
        













@app.route('/api/materia/<int:disciplina_id>/assunto/create', methods=["POST"])
def api_materia_assunto_create(disciplina_id):
    if request.method == "POST":
        description = request.form["description"]
        temp = Assunto.create(session=SessionLocal(), data={
            'description': description,
            'disciplina_id': disciplina_id,
        })
        if temp:
            data_out = {
                'id': temp.id,
                'disciplina_id': temp.disciplina_id,
                'description': temp.description,
                'date_created': temp.date_created,
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar assunto"}), 400
    return jsonify(error=True)






@app.route('/api/materia/assunto/<int:assunto_id>/question/create', methods=["POST"])
def api_materia_assunto_question_create(assunto_id):
    if request.method == "POST":
        question = request.form["question"]
        correct = request.form["correct"]
        if not correct.lower() in ('1', '0'):
            return jsonify(error=True, message="\"correct\" value invalid"), 400
        correct = True if correct == '1' else False
        temp = Pergunta.create(session=SessionLocal(), data={
            'question': question,
            'correct': correct,
            'assunto_id': assunto_id,
        })
        if temp:
            data_out = {
                'id': temp.id,
                'assunto_id': temp.assunto_id,
                'question': temp.question,
                'correct': temp.correct,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar questao"}), 400
    return jsonify(error=True)





@app.route('/api/materia/assunto/<int:id_assunto>')
def api_materia_assunto_view(id_assunto):
    temp = Assunto.list_by_id_moar(session=SessionLocal(), id=id_assunto)
    if temp:
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404






@app.route('/api/materia/assunto/<int:id_assunto>/update', methods=["POST"])
def api_materia_assunto_update(id_assunto):
    session = SessionLocal()
    description = request.form.get('description', False)
    if not description:
        return jsonify(error=True, message='missing `description`'), 400
    temp = Assunto.list_by_id(session=session, id=id_assunto)
    if not temp:
        return jsonify(error=True, message='not found'), 404
    try:
        temp.description = description
        session.commit()
        return jsonify(error=False), 200
    except Exception as err:
        return jsonify(error=True, message='exception', detail=str(err)), 400



@app.route('/api/materia/assunto/<int:id_assunto>/delete', methods=["DELETE"])
def api_materia_assunto_delete(id_assunto):
    session = SessionLocal()
    temp = Assunto.list_by_id(session=session, id=id_assunto)
    if temp:
        if len(temp.perguntas)>0:
            return jsonify(error=True, message="Voce precisa deletar as questoes do assunto antess]"), 400
        else:
            try:
                session.delete(temp)
                session.commit()
                return jsonify(error=False), 204
            except Exception as err:
                return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404
    
            
        




@app.route('/api/materia/assunto/questao/<int:id_questao>')
def api_materia_assunto_questao_view(id_questao):
    temp = Pergunta.list_by_id(session=SessionLocal(), id=id_questao)
    if temp:
        print(temp)
        return jsonify(error=False, data=temp)
    return jsonify(error=True, message='not found'), 404






@app.route('/api/materia/assunto/questao/<int:id_questao>/edit', methods=["POST"])
def api_materia_assunto_questao_edit(id_questao):
    if request.method == "POST":
        question = request.form["question"]
        correct = request.form["correct"]
        if not correct.lower() in ('1', '0'):
            return jsonify(error=True, message="\"correct\" value invalid"), 400
        correct = True if correct == '1' else False
        sessao = SessionLocal()
        temp = Pergunta.list_by_id(session=sessao, id=id_questao)
        if temp:
            print(temp)
            temp.question = question
            temp.correct = correct
            sessao.commit()
            data_out = {
                'id': temp.id,
                'assunto_id': temp.assunto_id,
                'question': temp.question,
                'correct': temp.correct,
                'date_created': temp.date_created
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou editar questao"}), 400
    return jsonify(error=True)




@app.route('/api/materia/assunto/<int:assunto_id>/question/quiz')
def api_materia_assunto_question_quiz_view(
    assunto_id    
):
    rdtoken = retrieve_token(request=request)
    quiz_master = SessionLocal().query(Quiz).filter_by(assunto_id=assunto_id, user_id=rdtoken.get('id', None)).order_by(Quiz.date_created.desc()).first()
    if quiz_master:
        out_quiz = {}
        # for item_quiz in quiz_master:
        out_quiz.update(
            {
                'id': quiz_master.id,
                'assunto_id': quiz_master.assunto_id,
                'user_id': quiz_master.user_id,
                'respostas': [
                    {
                        'id': x.id,
                        'question_raw': x.question_raw,
                        'resposta_user': x.resposta_user,
                        'system_correct': x.system_correct,
                        'quiz_id': x.quiz_id,
                        'question_id': x.question_id
                    } for x in quiz_master.respostas
                ]
            }
        )
        return jsonify(error=False, data=out_quiz)
    return jsonify(error=True, message='oxe painho')


#??
@app.route('/api/materia/assunto/<int:assunto_id>/question/quiz/create', methods=["POST"])
@check_authenticated_user()
def api_materia_assunto_question_quiz_create(
    assunto_id,
    # respostas=None, #?
    user_id=None, #do token
):
    if request.method == "POST":
        data = request.get_json()
        rdtoken = retrieve_token(request=request)
        quiz_master = Quiz.create(
            session=SessionLocal(),
            data={
                'assunto_id': data.get('assunto_id', None),
                'user_id': rdtoken.get('id', None)
            }
        )
        out_quiz = []
        if quiz_master:
            for user_response in data.get('respostas', []):
                out_quiz.append(
                    QuizResposta.create(
                        session=SessionLocal(),
                        data={
                            'question_raw': user_response.get('pergunta_sistema', ''),
                            'resposta_user': user_response.get('resposta', ''),
                            'system_correct': user_response.get('resposta_sistema', ''),
                            'quiz_id': quiz_master.id,
                            'question_id': user_response.get('id', None),
                            'user_id': quiz_master.user_id
                        }
                    )
                )
        data_out = {
            'id': quiz_master.id,
            'assunto_id': quiz_master.assunto_id,
            'user_id': quiz_master.user_id,
            'respostas': [
                {
                    'id': x.id,
                    'question_raw': x.question_raw
                } for x in out_quiz
            ]
        }
        return jsonify(error=False, data=data_out)
        name = {}
        for key, value in request.form.items():
            name[key] = value
        print(name)
        print(json.dumps(request.form))
        print(request.get_json())
        print(rdtoken)
        return jsonify(data=name)
    return jsonify(data='sem data')
    #     question = request.form["question"]
    #     correct = request.form["correct"]
    #     if not correct.lower() in ('1', '0'):
    #         return jsonify(error=True, message="\"correct\" value invalid"), 400
    #     correct = True if correct == '1' else False
    #     temp = Pergunta.create(session=SessionLocal(), data={
    #         'question': question,
    #         'correct': correct,
    #         'assunto_id': assunto_id,
    #     })
    #     if temp:
    #         data_out = {
    #             'id': temp.id,
    #             'assunto_id': temp.assunto_id,
    #             'question': temp.question,
    #             'correct': temp.correct,
    #             'date_created': temp.date_created
    #         }
    #         return jsonify(error=False, data=data_out)
    #     else:
    #         return jsonify({"msg": "aplicacao falhou criar questao"}), 400
    # return jsonify(error=True)









@app.route('/api/materia/assunto/questao/<int:id_questao>', methods=["DELETE"])
def api_materia_assunto_questao_delete(id_questao):
    session = SessionLocal()
    temp = Pergunta.list_by_id(session=session, id=id_questao)
    if temp:
        try:
            session.delete(temp)
            session.commit()
            return jsonify(error=False), 204
        except Exception as err:
            return jsonify(error=True, message='exception', detail=str(err)), 400
    else:
        return jsonify(error=True, message='not found'), 404






@app.route('/api/user/<int:id_user>', methods=["GET"])
@api_check_jwt_admin()
def api_user_list_by_id(id_user):
    temp = Usuario.list_by_id_moar(session=SessionLocal(), id=id_user)
    if temp:
        return jsonify(error=False, data=temp)
    else:
        return jsonify(error=True, message='no return')






@app.route('/api/user/<int:id_user>/edit', methods=["POST"])
@api_check_jwt_admin()
def api_user_edit(id_user):
    if request.method == "POST":
        name = request.form.get('name', False)
        email = request.form.get('email', False)
        username = request.form.get('username', False)
        group = request.form.get('group', False)
        password = request.form.get('password', None)
        status = request.form.get('status', None)
        status = True if status.lower() == 'true' else False if status.lower() == 'false' else None
        if name and email and username and group and status is not None:
            app.logger.info(f'status {id_user} received == {status}')
            sessao = SessionLocal()
            temp = Usuario.list_by_id(session=sessao, id=id_user)
            if temp:
                temp.username = username
                temp.email = email
                temp.name = name
                temp.group = group
                temp.active = status
                if password:
                    temp.password = password
                sessao.commit()
                return jsonify(error=False, data=temp)
            else:
                return jsonify(error=True, message="aplicacao falhou editar usuario"), 400
        else:
            return jsonify(error=True, message='Missing params')
    return jsonify(error=True, message='ops')






@app.route('/api/user/create', methods=["POST"])
@api_check_jwt_admin()
def api_user_create():
    if request.method == "POST":
        name = request.form.get('name', False)
        email = request.form.get('email', False)
        username = request.form.get('username', False)
        group = request.form.get('group', False)
        password = request.form.get('password', False)
        status = request.form.get('status', None)
        status = True if status.lower() == 'true' else False if status.lower() == 'false' else None
        if name and email and username and group and password and status is not None:
            temp = Usuario.create(session=SessionLocal(), data={
                    'username': username,
                    'password': password,
                    'group': group,
                    'active': status,
                    'name': name,
                    'email': email
                }
            )
            if temp:
                data_out = {
                    'id': temp.id,
                    'username': temp.username,
                    'group': temp.group,
                    'active': temp.active,
                    'name': temp.name,
                    'email': temp.email,
                    'date_created': temp.date_created,
                }
                return jsonify(error=False, data=data_out)
            else:
                return jsonify(error=True, message="aplicacao falhou criar usuario"), 400
        else:
            return jsonify(error=True, message='Missing params')
    return jsonify(error=True, message='ops')







@app.route('/api/user/list', methods=["GET"])
@api_check_jwt_admin()
def api_user_list():
    temp = Usuario.list_all_moar(session=SessionLocal())
    if temp:
        return jsonify(error=False, data=temp)
    else:
        return jsonify(error=True, message='no return')



@app.route('/api/user/login', methods=["POST"])
def api_user_check():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if username and password:
        temp = Usuario.validate_user(session=SessionLocal(), username=username, password=password)
        if temp:
            if not temp.active:
                raise UserInactive("Usu&aacute;rio inativo")
            data_token = {
                'id': temp.id,
                'username': temp.username,
                'group': temp.group,
                'admin': temp.UsuarioGrupo.admin,
                'name': temp.name,
                'email': temp.email
            }
            token = jwt.encode(data_token, app.config.get('MASTER_KEY', '123456'), algorithm="HS256")
            response_obj = jsonify(error=False, access_token=token.decode())
            response_obj.set_cookie('access_token', token.decode(), secure=True, httponly=True)
            return response_obj
        else:
            raise UsernameOrPasswordInvalid("Nome de usu&aacute;rio/e-mail ou senha incorretos")
    else:
        return jsonify(error=True, message="missing params")


#MissingParams
#UsernameOrPasswordInvalid


#


@app.route('/api/user/public/create', methods=["POST"])
def api_user_create_public():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["email"]
        group = 'ROOT'
        temp = Usuario.create(session=SessionLocal(), data={
            'username': username,
            'password': password,
            'group': group,
            'active': True,
            'name': name,
            'email': email
        })
        if temp:
            data_out = {
                'id': temp.id,
                'username': temp.username,
                'group': temp.group,
                'active': temp.active,
                'name': temp.name,
                'email': temp.email,
                'date_created': temp.date_created,
            }
            return jsonify(error=False, data=data_out)
        else:
            return jsonify({"msg": "aplicacao falhou criar usuario"}), 400
    return jsonify(error=True)





@app.route('/api/user/group/list', methods=["GET"])
@api_check_jwt_admin()
def api_user_group_list():
    temp = UsuarioGrupo.list_all(session=SessionLocal())
    if temp:
        return jsonify(error=False, data=temp)
    else:
        return jsonify(error=True, message='no return')





# random question 
# @app.route('/api/question/create', methods=["POST"])
# def api_question_create():
#     if request.method == "POST":
#         id_materia = request.form["id_materia"]
#         question = request.form["question"]
#         total_alternatives = int(request.form['total_alternatives'])
#         alternatives = []
#         for i in range(0, total_alternatives):
#             temp_is_correct = request.form.getlist(f'alternatives[{i}][is_correct]')[0]
#             alternatives.append({
#                 'alternative': request.form.getlist(f'alternatives[{i}][alternative]')[0],
#                 'is_correct': temp_is_correct
#             })
#         print(alternatives)
#         temp = Pergunta.create(session=SessionLocal(), data={
#             "question": question,
#             "materia_id": id_materia
#         })
#         if temp:
#             for alternative in alternatives:
#                 av = Resposta.create(session=SessionLocal(), data={
#                     'alternative': alternative['alternative'],
#                     'correct': True if alternative['is_correct'].lower() == 's' else False,
#                     'question_id': temp.id
#                 })
#                 if not av:
#                     return jsonify({'error': True, 'message': 'failed add alternative'})
#             data_out = {
#                 'id': temp.id,
#                 'question': temp.question,
#                 'materia_id': temp.materia_id,
#                 'date_created': temp.date_created
#             }
#             return jsonify(error=False, data=data_out)
#         else:
#             return jsonify({"msg": "aplicacao falhou criar materia"}), 400
#     return jsonify(error=True)



# @app.route('/api/alternative/create', methods=["POST"])
# def api_alternative_create():
#     if request.method == "POST":
#         id_question = request.form["id_question"]
#         alternative = request.form["alternative"]
#         correct = request.form["correct"]
#         temp = Pergunta.create(session=SessionLocal(), data={
#             "alternative": alternative,
#             "question_id": id_question,
#             "correct": True if correct.lower() == 's' else False
#         })
#         if temp:
#             data_out = {
#                 'id': temp.id,
#                 'alternative': temp.alternative,
#                 'correct': temp.correct,
#                 'question_id': temp.question_id,
#                 'date_created': temp.date_created
#             }
#             return jsonify(error=False, data=data_out)
#         else:
#             return jsonify({"msg": "aplicacao falhou criar materia"}), 400
#     return jsonify(error=True)

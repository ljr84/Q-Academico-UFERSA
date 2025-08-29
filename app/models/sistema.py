from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey,
    event,
    or_
)
from sqlalchemy.types import(
    Boolean,
    DateTime
)
from sqlalchemy.orm import(
    relationship,
    Session
)

from datetime import datetime
from typing import Type

from app.core.database import Base
from app.models.base import ModelBase

from dataclasses import dataclass

from app.exceptions import(
    PermissionDenied,
    PermissionDeniedAPI,
    APIUserAlreadyExists,
    DisciplinaAlreadyExists
)


@dataclass
class Disciplina(ModelBase, Base):
    __tablename__ = "Disciplina"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(255))
    icon: str = Column(String(255))
    description: str = Column(String(255))
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    assuntos = relationship('Assunto', backref='Disciplina')

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: dict
    ):
        name = data.get('name', False)
        description = data.get('description', False)
        if name and description:
            check_disciplina = Disciplina.check_disciplina_exist(session=session, name=name, description=description)
            if check_disciplina:
                return check_disciplina.id
            return super().create(session=session, data=data)
        return False


    @classmethod
    def check_disciplina_exist(cls, session, name, description):
        try:
            temp = session.query(
                cls
            ).filter_by(
                name = name
            ).filter_by(
                description = description
            ).one()
            if temp:
                return temp
        except Exception as err:
            print(f'models.Disciplina.check_disciplina_exist exp - {err}')
        return False


    @classmethod
    def list_by_id_moar(cls, session, id):
        try:
            temp = session.query(cls).filter_by(id=id).first()
            if temp:
                data = {
                    'id': temp.id,
                    'name': temp.name,
                    'icon': temp.icon,
                    'description': temp.description,
                }
                assuntos_data = []
                if len(temp.assuntos)>0:
                    for assunto in temp.assuntos:
                        assuntos_data.append({
                            'id': assunto.id,
                            'description': assunto.description,
                            'disciplina_id': assunto.disciplina_id,
                            'total_questions': len(assunto.perguntas)
                        })
                data.update({
                    'assuntos': assuntos_data
                })
                return data
        except Exception as err:
            print(f'exp Disciplina.list_by_id_moar - {err}')
        return False
    

@dataclass
class Assunto(ModelBase, Base):
    __tablename__ = "Assunto"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    disciplina_id = Column(Integer, ForeignKey("Disciplina.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    perguntas = relationship('Pergunta', backref='Assunto')
    #disciplina = relationship('Disciplina', foreign_keys='Assunto.disciplina_id')


    @classmethod
    def list_by_id_moar(cls, session, id):
        try:
            temp = session.query(Assunto).filter_by(id=id).first()
            if temp:
                data = {
                    'id': temp.id,
                    'description': temp.description,
                    'disciplina_id': temp.disciplina_id,
                    'date_created': temp.date_created,
                    'disciplina_data': {
                        'id': temp.Disciplina.id,
                        'name': temp.Disciplina.name,
                        'description': temp.Disciplina.description,
                        'date_created': temp.Disciplina.date_created,
                    }
                }
                questions_data = []
                if len(temp.perguntas)>0:
                    for pergunta in temp.perguntas:
                        questions_data.append({
                            'id': pergunta.id,
                            'question': pergunta.question,
                            'correct': pergunta.correct,
                            'assunto_id': pergunta.assunto_id,
                            'date_created': pergunta.date_created,
                        })
                data.update({
                    'questions': questions_data
                })
                return data
        except Exception as err:
            print(f'exp Assunto.list_by_id_moar - {err}')
        return False



@dataclass
class Pergunta(ModelBase, Base):
    __tablename__ = "Pergunta"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question: str = Column(String(255))
    #key = Column(String(255))
    correct: bool = Column(Boolean, nullable=False)
    assunto_id: int = Column(Integer, ForeignKey("Assunto.id"), nullable=False)
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    #alternative_answers = relationship('Resposta', backref='Pergunta')






@dataclass
class Quiz(ModelBase, Base):
    __tablename__ = "Quiz"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assunto_id: int = Column(Integer, ForeignKey("Assunto.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    # question: str = Column(String(255))
    #key = Column(String(255))
    # correct: bool = Column(Boolean, nullable=False)
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    respostas = relationship('QuizResposta', backref='Quiz')





@dataclass
class QuizResposta(ModelBase, Base):
    __tablename__ = "QuizResposta"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_raw: str = Column(String(255)) ##se deletar a question
    resposta_user: str = Column(String(255))
    #key = Column(String(255))
    system_correct: bool = Column(Boolean, nullable=False)
    quiz_id: int = Column(Integer, ForeignKey("Quiz.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("Pergunta.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    #alternative_answers = relationship('Resposta', backref='Pergunta')




@dataclass
class UsuarioGrupo(ModelBase, Base):
    __tablename__ = "UsuarioGrupo"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description: str = Column(String(255))
    key: str = Column(String(25), nullable=False, unique=True)
    active: bool = Column(Boolean, nullable=False)
    admin: bool = Column(Boolean, nullable=False, default=False)
    usuarios = relationship('Usuario', backref='UsuarioGrupo')
    date_created: datetime = Column(DateTime, default=datetime.utcnow())

    def auto_create(target, connection, **kw):
        default_groups = [
            {
                'description': 'Professor',
                'key': 'G_PROF',
                'active': True,
                'admin': True,
            },
            {
                'description': 'Aluno',
                'key': 'G_ALUNO',
                'active': True,
                'admin': False
            },
            {
                'description': 'Sistema',
                'key': 'ROOT',
                'active': True,
                'admin': True
            },
        ]
        for group in default_groups:
            try:
                connection.execute(
                    target.insert(),
                    group
                )
            except Exception as err:
                print(f'models.sistema.UsuarioGrupo.auto_create exp - {err}')




@dataclass
class Usuario(ModelBase, Base):
    __tablename__ = "Usuario"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)
    name: str = Column(String(255))
    email: str = Column(String(255), nullable=False)
    active: bool = Column(Boolean, nullable=False)
    group: str = Column(String(25), ForeignKey("UsuarioGrupo.key"), nullable=False)
    date_created: datetime = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: dict
    ):
        username = data.get('username', False)
        email = data.get('email', False)
        cango = False
        if username and email:
            for item in [username, email]:
                if Usuario.check_user_exist(session=session, search=item):
                    raise APIUserAlreadyExists('xxxxxx')
                    return False
            return super().create(session=session, data=data)
        return False
        # obj = cls(**data)
        # obj.date_created = datetime.utcnow()
        # session.add(obj)
        # session.commit()
        # session.refresh(obj)
        # return obj

    @classmethod
    def validate_user(cls, session, username, password):
        try:
            temp = session.query(
                cls
            ).filter_by(
                password=password
            ).filter(
                (Usuario.username == username) | (Usuario.email == username)
            ).one()
            return temp
        except Exception as err:
            print(f'models.Usuario.validate_user exp - {err}')
        return False

    @classmethod
    def check_user_exist(cls, session, search):
        try:
            temp = session.query(cls) \
                .filter(
                    (Usuario.username == search) | (Usuario.email == search)
                ).one()
            if temp:
                return True
        except Exception as err:
            print(f'models.Usuario.check_user_exist exp - {err}')
        return False

    @classmethod
    def list_all_moar(cls, session):
        try:
            temp = session.query(cls).all()
            if temp:
                data = []
                for item in temp:
                    data.append(
                        {
                            'id': item.id,
                            'username': item.username,
                            'name': item.name,
                            'email': item.email,
                            'active': item.active,
                            'group': item.group,
                            'date_created': item.date_created,
                            'group_data': {
                                'id': item.UsuarioGrupo.id,
                                'description': item.UsuarioGrupo.description,
                                'key': item.UsuarioGrupo.key,
                                'admin': item.UsuarioGrupo.admin
                            }
                        }
                    )
                return data
        except Exception as err:
            print(f'models.sistema.Usuario.list_all_moar exp - {err}')
        return False

    @classmethod
    def list_by_id_moar(cls, session, id):
        try:
            temp = session.query(cls).filter_by(id=id).first()
            if temp:
                data = {}
                data.update(
                    {
                        'id': temp.id,
                        'username': temp.username,
                        'name': temp.name,
                        'email': temp.email,
                        'active': temp.active,
                        'group': temp.group,
                        'date_created': temp.date_created,
                        'group_data': {
                            'id': temp.UsuarioGrupo.id,
                            'description': temp.UsuarioGrupo.description,
                            'key': temp.UsuarioGrupo.key,
                            'admin': temp.UsuarioGrupo.admin
                        }
                    }
                )
                return data
        except Exception as err:
            print(f'models.sistema.Usuario.list_by_id_moar exp - {err}')
        return False

    def auto_create(target, connection, **kw):
        default_users = [
            {
                'username': 'superadmin',
                'password': '123456',
                'active': True,
                'group': 'ROOT',
                'name': 'admin',
                'email': 'root@me.com'
            },
        ]
        for user in default_users:
            try:
                connection.execute(
                    target.insert(),
                    user
                )
            except Exception as err:
                print(f'models.sistema.UsuarioGrupo.auto_create exp - {err}')






event.listen(UsuarioGrupo.__table__, 'after_create', UsuarioGrupo.auto_create)
event.listen(Usuario.__table__, 'after_create', Usuario.auto_create)








##??? deletar?
# class Resposta(ModelBase, Base):
#     __tablename__ = "Resposta"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     alternative = Column(String(255), nullable=False)
#     correct = Column(Boolean, nullable=False)
#     question_id = Column(Integer, ForeignKey("Pergunta.id"), nullable=False)
#     date_created = Column(DateTime, default=datetime.utcnow())
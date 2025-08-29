from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime
)
from app.core.database import Base

from app.models.base import ModelBase
from datetime import datetime

from sqlalchemy.orm import relationship
from typing import Type
from sqlalchemy.orm import Session
from datetime import datetime




class Materia(ModelBase, Base):
    __tablename__ = "Materia"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    icon = Column(String(255))
    description = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())
    perguntas = relationship('Pergunta', backref='Materia')
    
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data: dict
    ):
        obj = cls(**data)
        obj.date_created = datetime.utcnow()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


    @classmethod
    def find_by_key(cls, session, key):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).filter_by(key=key).first()



class Pergunta(ModelBase, Base):
    __tablename__ = "Pergunta"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String(255))
    #key = Column(String(255))
    materia_id = Column(String(36), ForeignKey("Materia.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    alternative_answers = relationship('Resposta', backref='Pergunta')

    @classmethod
    def find_by_key(cls, session, key):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).filter_by(key=key).first()





class Resposta(ModelBase, Base):
    __tablename__ = "Resposta"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alternative = Column(String(255), nullable=False)
    correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Pergunta.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    #source_data = relationship('Person', backref='Source')

    @classmethod
    def find_by_key(cls, session, key):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).filter_by(key=key).first()
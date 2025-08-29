from app import(
    app,
    db
)

from app.core.database import(
    engine,
    Base
)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db.create_all()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
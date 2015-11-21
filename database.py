from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from flask import Flask
app = Flask(__name__)

engine = create_engine('sqlite:////'+os.path.join(app.root_path, 'pageBuilder.db'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.session = db_session

def init_db():
    from models import user, site, page, element, element_type
    Base.metadata.create_all(bind=engine)


def db_connect():
    return create_engine('sqlite:////'+os.path.join(app.root_path, 'pageBuilder.db'), convert_unicode=True)


def get_session():
    engine = db_connect()
    return sessionmaker(bind=engine)
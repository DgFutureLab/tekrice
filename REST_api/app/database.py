
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://halfdan:halfdan@localhost/tekrice_dev', convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()




def nuke_db():
	import models
	db_session.close()
	Base.metadata.drop_all(bind=engine)

def init_db():
	import models
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
	Base.metadata.create_all(bind=engine)

def recreate():
	nuke_db()
	init_db()
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

db_user = os.environ['DBUSERNAME']
db_host = os.environ['DBHOST']
db_pw = os.environ['DBPW']
db_name = os.environ['DBNAME']

engine = create_engine('mysql+pymysql://'+ db_user + ':' + db_pw + '@' + db_host + '/' + db_name)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
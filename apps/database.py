from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://crescent:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# #connecting to the database.
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database='fastapi',user='crescent', 
#                                 password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected Succesfully")
#         break
#     except Exception as error:
#         print(str(error))
#         time.sleep(2)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost/ToDoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = "postgresql://avnadmin:AVNS_ex1XuACkKBBu4DlAAD-@deploy-database-heerasingh-e6bb.j.aivencloud.com:28242/defaultdb?sslmode=require"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

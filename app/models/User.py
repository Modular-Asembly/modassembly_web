from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from app.modassembly.database.sql.get_sql_session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)

from sqlalchemy import Column, Integer, String, Boolean
from app.modassembly.database.sql.get_sql_session import Base

class FeatureFlag(Base):
    __tablename__ = 'feature_flags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    enabled = Column(Boolean, nullable=False)

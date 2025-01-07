from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base

class UserFeatureFlag(Base):
    __tablename__ = 'user_feature_flags'
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True, nullable=False)
    feature_flag_id = Column(Integer, ForeignKey('feature_flags.id'), primary_key=True, index=True, nullable=False)
    enabled = Column(Boolean, nullable=False)

from sqlalchemy import Column, Integer, String, Text
from database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True)
    target = Column(String)
    status = Column(String)
    result = Column(Text)
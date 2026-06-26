from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Text

Base = declarative_base()
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key = True)
    company = Column(String)
    industry = Column(String)
    website = Column(String)
    contact_email = Column(String)
    research = Column(Text)
    score = Column(Text)
    email = Column(Text)
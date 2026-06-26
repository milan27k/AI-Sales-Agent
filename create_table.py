from database import engine
from database_model import Base

Base.metadata.create_all(bind=engine)
print("table created successfully")
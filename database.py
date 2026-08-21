from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
database_url = "postgresql://postgres:123456789@localhost:5432/ai_sales_agent"

engine = create_engine(database_url)
sessionLocal = sessionmaker(autoflush=False,bind=engine,autocommit = False)
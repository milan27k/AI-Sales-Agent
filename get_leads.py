from database import sessionLocal
from database_model import Lead

def get_all_leads():
    db = sessionLocal()
    leads = db.query(Lead).all()
    db.close()
    return leads
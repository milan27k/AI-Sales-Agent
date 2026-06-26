from database import sessionLocal
from database_model import Lead
def save_leads(result):
    db = sessionLocal()
    lead = Lead(
        company = result['company'],
        industry=result["industry"],
        website=result["website"],
        research=result["research"],
        contact_email=result["contact_email"],
        score=result["score"],
        email=result["email"]
    )
    db.add(lead)
    db.commit()
    db.close()
    print("lead save succesfully")
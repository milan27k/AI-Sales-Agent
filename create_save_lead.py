from database import sessionLocal
from database_model import Lead


def save_leads(result):
    db = sessionLocal()

    lead = Lead(
        company=result["company"],
        industry=result["industry"],
        website=result["website"],
        research=result["research"],
        contact_email=result["contact_email"],
        buying_signals=result["buying_signals"],
        qualification=result["qualification"],
        score=result["score"],
        email=result["email"],
        status="PENDING_APPROVAL"
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    lead_id = lead.id
    db.close()

    print("lead save successfully")
    return lead_id


def update_lead_status(lead_id, status):
    db = sessionLocal()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if lead:
        lead.status = status
        db.commit()

    db.close()
    return lead

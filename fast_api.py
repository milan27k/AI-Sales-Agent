from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from create_save_lead import save_leads, update_lead_status
from agent import run_sales_agent

app = FastAPI()


class LeadRequest(BaseModel):
    company: str
    industry: str
    website: str
    contact_email: str


@app.get("/")
def home():
    return {"message": "AI Sales Agent API is running"}


@app.post("/analyze")
def analyze_lead(data: LeadRequest):
    result = run_sales_agent(
        data.company,
        data.industry,
        data.website
    )

    result["company"] = data.company
    result["industry"] = data.industry
    result["website"] = data.website
    result["contact_email"] = data.contact_email

    lead_id = save_leads(result)

    # V1 modification: stop here. No automatic email sending.
    result.pop("website_content", None)
    result["lead_id"] = lead_id
    result["status"] = "PENDING_APPROVAL"

    return result


@app.post("/leads/{lead_id}/approve")
def approve_lead(lead_id: int):
    lead = update_lead_status(lead_id, "APPROVED")

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {
        "lead_id": lead_id,
        "status": "APPROVED",
        "message": "Lead approved. No email was sent."
    }


@app.post("/leads/{lead_id}/reject")
def reject_lead(lead_id: int):
    lead = update_lead_status(lead_id, "REJECTED")

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {
        "lead_id": lead_id,
        "status": "REJECTED",
        "message": "Lead rejected."
    }

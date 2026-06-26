from fastapi import FastAPI
from pydantic import BaseModel
from create_save_lead import save_leads
from agent import run_sales_agent
import requests

app = FastAPI()
class LeadRequest(BaseModel):
    company : str
    industry : str
    website : str
    contact_email : str

@app.get("/")
def home():
    return{
        "message":"AI Sales Agent API is running"
    }

@app.post("/analyze")
def analyze_lead(data:LeadRequest):
    result = run_sales_agent(
        data.company,
        data.industry,
        data.website,
    )
    result["company"] = data.company
    result["industry"] = data.industry
    result["website"] = data.website
    result["contact_email"] = data.contact_email
    save_leads(result)

    response = requests.post(
        "http://localhost:5678/webhook/lead-analysis",
        json=result
    )
    print("N8N STATUS:", response.status_code)
    print("N8N RESPONSE:", response.text)
    result.pop("website_content", None)
    return result
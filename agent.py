from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from dotenv import load_dotenv
from web_scrapper import web_scrapper
from create_save_lead import save_leads
load_dotenv()
model = ChatOpenAI(model='gpt-4o-mini')

class SalesState(TypedDict):
    company : str
    industry:str
    website:str
    website_content:str
    research : str
    score : str
    email:str

def scrap_website(State:SalesState):
    content = web_scrapper(State['website'])
    return{"website_content":content}


def research_company(State:SalesState):

    print("\n" + "="*50)
    print("WEBSITE CONTENT:")
    print(State["website_content"][:1000])
    print("="*50 + "\n")

    company = State['company']
    industry = State['industry']
    website_content = State['website_content']
    if website_content.startswith("error"):
        website_content = "website content unavailable"
    prompt = f"""
    You must ONLY use the website content below.

Website Content:
{website_content}

Rules:
- Ignore the provided company name.
- Ignore the provided industry.
- Identify the company from the website content itself.
- If the website content belongs to NVIDIA, analyze NVIDIA.
- Do not invent information.
- If website content is unavailable, say so.

Return:

Company Profile:
...

Possible Business Needs:
...

Possible AI Opportunities:
...
Keep response under 150 words.
    """ 
    result = model.invoke(prompt)
    return {'research':result.content}  

def score_generation(State:SalesState):
    research = State['research']
    prompt = f"""
You are an expert B2B sales lead qualification specialist.

Research:
{research}

Your task is to score the lead from 0-100.

Evaluate the company using these criteria:

Company Size (25%)
Enterprise (5000+ employees)
Mid-size company
Small business
Estimated AI Budget (25%)
High
Medium
Low
Technology Maturity (20%)
Existing cloud, software, AI, automation, digital products
AI Adoption Readiness (15%)
Active innovation, AI initiatives, automation, analytics
Business Need for AI (15%)
Operational challenges AI can solve

Scoring Guidelines:

90-100:
Enterprise company with high AI budget and strong AI adoption.
Examples: Microsoft, Google, Amazon, NVIDIA, Salesforce.

80-89:
Large technology-focused company with significant AI investment.

60-79:
Medium-sized business with reasonable AI budget and AI potential.

40-59:
Small business with some digital presence.

0-39:
Small local business with limited budget and low AI readiness.

IMPORTANT RULES:

Company size and budget are the most important factors.
Do NOT give high scores solely because AI opportunities exist.
Local businesses should rarely exceed 50.
Enterprise technology companies should usually exceed 85.
Be realistic and conservative.
Follow category rules strictly.

Category Rules:
Score >= 80 → Hot Lead
Score >= 50 and Score < 80 → Warm Lead
Score < 50 → Cold Lead

Return EXACTLY in this format:

Score:

Category: <Hot Lead/Warm Lead/Cold Lead>

Company Size: <High/Medium/Low>

Estimated AI Budget: <High/Medium/Low>

Technology Maturity: <High/Medium/Low>

AI Readiness: <High/Medium/Low>

Reason:


""" 
    result = model.invoke(prompt)
    return {'score':result.content}

def email_generation(State:SalesState):
    
    prompt = f"""
You are a senior B2B sales representative at Milan AI Solutions.

About Milan AI Solutions:
- AI Automation
- Custom AI Agents
- RAG Applications
- Workflow Automation
- Generative AI Solutions
- AI Consulting

Target Company:
{State['company']}

Research:
{State['research']}

Lead Score:
{State['score']}

Your task is to write a highly personalized cold outreach email.

Requirements:

1. Mention at least one specific insight from the research.
2. Identify one likely business challenge based on the research.
3. Explain how Milan AI Solutions can help solve that challenge.
4. Mention only relevant services.
5. Focus on business value:
   - Productivity
   - Automation
   - Cost Reduction
   - Operational Efficiency
6. Include a clear 15-minute meeting CTA.
7. Keep the email between 120-180 words.
8. Use a professional and natural tone.
9. Address the company by name.
10. Do NOT write as if you work for the target company.
11. CRITICAL:
- Never use [Recipient's Name]
- Never use placeholders of any kind
- Start the email with:
  "Hello {State['company']} Team,"
12. Do NOT write "Dear Team".
13. Do NOT include sender details.
14. Do NOT include signatures.
15. Do NOT write generic marketing language.
16. End immediately after the CTA sentence.

Return ONLY in this format:

Subject: <subject>

Email:
<email body>

    """
    result = model.invoke(prompt)
    return {'email':result.content}

graph = StateGraph(SalesState)
graph.add_node("scraping",scrap_website)
graph.add_node("research",research_company)
graph.add_node("score",score_generation)
graph.add_node("email",email_generation)

graph.add_edge(START,'scraping')
graph.add_edge('scraping','research')
graph.add_edge('research','score')
graph.add_edge('score','email')
graph.add_edge('email',END)

workflow = graph.compile()

def run_sales_agent(company,industry,website):
    print("WEBSITE RECEIVED:", website)
    result = workflow.invoke({
        "company":company,
         "industry":industry,
         "website":website
         })
    result["company"] = company
    result["industry"] = industry
    result["website"] = website
    return result
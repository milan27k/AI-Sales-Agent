from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
from web_scrapper import web_scrapper

load_dotenv()
model = ChatOpenAI(model="gpt-4o-mini")


class SalesState(TypedDict):
    company: str
    industry: str
    website: str
    website_content: str
    research: str
    buying_signals: str
    qualification: str
    score: str
    email: str


def scrap_website(State: SalesState):
    content = web_scrapper(State["website"])
    return {"website_content": content}


def research_company(State: SalesState):
    website_content = State["website_content"]
    if website_content.startswith("error"):
        website_content = "website content unavailable"

    prompt = f"""
You must ONLY use the website content below.
Website Content:
{website_content}

Rules:
- Ignore the provided company name and industry.
- Identify the company from the website content itself.
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
    return {"research": result.content}


def buying_signal_generation(State: SalesState):
    prompt = f"""
You are a B2B sales research analyst.

Company Research:
{State["research"]}

Identify observable signals indicating possible interest in AI,
automation, or digital solutions.

Possible signals:
- AI or automation initiatives
- Digital transformation
- Technology expansion
- Operational problems AI could solve
- Product/service expansion
- Analytics/software adoption

Do NOT invent funding, hiring, budget, employee count, or news.
If there is no clear signal, say "No strong buying signal found."

Return EXACTLY:

Buying Intent: <High/Medium/Low>

Signals:
- <signal 1>
- <signal 2>

Reason:
<short explanation>

Confidence: <High/Medium/Low>
"""
    result = model.invoke(prompt)
    return {"buying_signals": result.content}


def icp_qualification(State: SalesState):
    prompt = f"""
You are a B2B sales qualification specialist.

Company: {State["company"]}
Industry: {State["industry"]}

Research:
{State["research"]}

Buying Signals:
{State["buying_signals"]}

Determine whether this company is a good potential customer
for an AI/automation solutions company.

Evaluate:
- Industry fit
- Business need
- Technology/digital maturity
- Buying intent

Do not invent company size, budget, authority, or other facts.

Return EXACTLY:

ICP Fit: <High/Medium/Low>

Strong Fits:
- <point 1>
- <point 2>

Risks:
- <risk 1>
- <risk 2>

Reason:
<short explanation>
"""
    result = model.invoke(prompt)
    return {"qualification": result.content}


def score_generation(State: SalesState):
    prompt = f"""
You are an expert B2B sales lead qualification specialist.

Research:
{State["research"]}

Buying Signals:
{State["buying_signals"]}

ICP Qualification:
{State["qualification"]}

Score the lead from 0-100.

Criteria:
Company Size (25%)
Estimated AI Budget (25%)
Technology Maturity (20%)
AI Adoption Readiness (15%)
Business Need for AI (15%)

Use only supported evidence. Do not assume unavailable information is high.

Category:
Score >= 80 -> Hot Lead
50-79 -> Warm Lead
<50 -> Cold Lead

Return EXACTLY:

Score: <0-100>
Category: <Hot Lead/Warm Lead/Cold Lead>
Company Size: <High/Medium/Low>
Estimated AI Budget: <High/Medium/Low>
Technology Maturity: <High/Medium/Low>
AI Readiness: <High/Medium/Low>
Reason:
<short explanation>
"""
    result = model.invoke(prompt)
    return {"score": result.content}


def email_generation(State: SalesState):
    prompt = f"""
You are a senior B2B sales representative at Milan AI Solutions.

Services:
- AI Automation
- Custom AI Agents
- RAG Applications
- Workflow Automation
- Generative AI Solutions
- AI Consulting

Target Company: {State["company"]}

Research:
{State["research"]}

Buying Signals:
{State["buying_signals"]}

ICP Qualification:
{State["qualification"]}

Lead Score:
{State["score"]}

Write a personalized cold outreach email.

Requirements:
1. Mention a specific research insight.
2. Identify one likely business challenge.
3. Explain how Milan AI Solutions can help.
4. Mention only relevant services.
5. Focus on productivity, automation, cost reduction, or efficiency.
6. Include a clear 15-minute CTA.
7. Keep it 120-180 words.
8. Professional and natural.
9. Start exactly with:
Hello {State["company"]} Team,
10. No placeholders, sender details, or signature.
11. No generic marketing language.
12. End after the CTA.

Return ONLY:

Subject: <subject>

Email:
<email body>
"""
    result = model.invoke(prompt)
    return {"email": result.content}


graph = StateGraph(SalesState)

graph.add_node("scraping", scrap_website)
graph.add_node("research", research_company)
graph.add_node("buying_signals", buying_signal_generation)
graph.add_node("icp_qualification", icp_qualification)
graph.add_node("score", score_generation)
graph.add_node("email", email_generation)

graph.add_edge(START, "scraping")
graph.add_edge("scraping", "research")
graph.add_edge("research", "buying_signals")
graph.add_edge("buying_signals", "icp_qualification")
graph.add_edge("icp_qualification", "score")
graph.add_edge("score", "email")
graph.add_edge("email", END)

workflow = graph.compile()


def run_sales_agent(company, industry, website):
    result = workflow.invoke({
        "company": company,
        "industry": industry,
        "website": website
    })
    result["company"] = company
    result["industry"] = industry
    result["website"] = website
    return result

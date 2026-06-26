import requests
from bs4 import BeautifulSoup

def web_scrapper(url):
    try:
        print("URL:", url)
        headers = {"User_Agent": "Mozilla/5.0"}
        response = requests.get(url,headers=headers,timeout=10)

        print("Status Code:", response.status_code)

        soup = BeautifulSoup(
            response.text,"html.parser"
        )
        paragraphs = soup.find_all(
        ["h1","h2","h3","p"]
        )

        text = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
        )
        print("Content Length:", len(text))
        return text[:5000]

    except Exception as e:
        return f"error:{e}"   
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Rajinikanth"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code) 
soup = BeautifulSoup(response.text, "html.parser")

paragraphs = soup.find_all("p")
print(f"Found {len(paragraphs)} paragraph tags") 
content_list = []
for p in paragraphs:
    text = p.get_text(strip=True)
    if text:
        content_list.append(text)

for i, para in enumerate(content_list, start=1):
    print(f"Paragraph {i}: {para}\n")

print(f" Total paragraphs scraped: {len(content_list)}")

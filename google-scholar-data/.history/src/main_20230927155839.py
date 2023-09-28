import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://scholar.google.com/scholar?q=deep learning"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 这里只是一个简单的选择器，实际的选择器可能需要进一步调整
    titles = soup.select('.gs_rt a')
    for title in titles:
        print(title.text)
else:
    print("Failed to retrieve the webpage.")


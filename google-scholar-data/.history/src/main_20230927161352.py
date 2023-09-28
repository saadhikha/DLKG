import requests
from bs4 import BeautifulSoup

# 基本设置
BASE_URL = "https://scholar.google.com"
SEARCH_URL = f"{BASE_URL}/scholar?q=深度学习"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_paper_details(soup):
    papers = []
    for result in soup.select('.gs_ri'):
        title = result.select_one('.gs_rt a').text
        link = result.select_one('.gs_rt a')['href']
        author_and_pub = result.select_one('.gs_a').text
        abstract = result.select_one('.gs_rs').text if result.select_one('.gs_rs') else ""
        citations = int(result.select_one('.gs_fl a').text.split()[-1]) if result.select_one('.gs_fl a') else 0

        paper = {
            "title": title,
            "link": link,
            "author_and_publication": author_and_pub,
            "abstract": abstract,
            "citations": citations
        }
        papers.append(paper)
    return papers

def main():
    response = requests.get(SEARCH_URL, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        papers = get_paper_details(soup)
        for paper in papers:
            print(paper)
    else:
        print("Failed to retrieve the webpage.")

if __name__ == "__main__":
    main()

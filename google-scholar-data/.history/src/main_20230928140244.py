import requests
from bs4 import BeautifulSoup
import hashlib

def generate_paper_id(title, authors, year):
    combined_string = title + ''.join(authors) + str(year)
    result = hashlib.sha256(combined_string.encode()).hexdigest()
    return result

# 基本设置
BASE_URL = "https://scholar.google.com"
SEARCH_URL = f"{BASE_URL}/scholar?q=deep+learning"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def parse_paper_element(paper_element):
    paper = {}
    content = paper_element.select_one('.gs_ri')
    pdf = paper_element.select_one('.gs_ggs gs_fl')
    if pdf is not None:
        paper.pdf = pdf.select_one('a').href
    # paper.paperId = content.select_one('gs_ggs gs_fl').text
    
    paper.title = content.select_one('a').text
    paper.link = 0



def get_paper_details(soup):
    papers = []
    for result in soup.select('.gs_r gs_or gs_scl'):
        paper = parse_paper_element(result)
        break
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

import requests
from bs4 import BeautifulSoup, NavigableString
import hashlib

def generate_paper_id(title, authors, year):
  combined_string = title + ''.join(authors) + str(year)
  result = hashlib.sha256(combined_string.encode()).hexdigest()
  return result

def generate_author_id(name, profile_link):
  combined_string = name + profile_link if profile_link else name
  result = hashlib.sha256(combined_string.encode()).hexdigest()
  return result

# 基本设置
BASE_URL = "https://scholar.google.com"
SEARCH_URL = f"{BASE_URL}/scholar?q=deep+learning"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

all_authors = {
   
}

def parse_paper_element(paper_element):
  paper = {}
  author = {}
  content_element = paper_element.select_one('.gs_ri')

  # ---- pdf
  pdf_element = paper_element.select_one('.gs_ggs.gs_fl')
  paper["pdf"] = None
  if pdf_element:
      paper["pdf"] = pdf_element.select_one('a')["href"]

  # ---- other fields
  paper["title"] = content_element.select_one('a').text
  paper["link"] = content_element.select_one('a')["href"]

  authors_element = content_element.select_one('.gs_a')
  paper["authors"] = []
  for author_element in authors_element.children:
    if isinstance(author, NavigableString) and author_element.strip(): 
        name = author_element.strip()
    elif author.name == 'a':  # Checking for <a> tag
        name = author_element.text
        profile_link = author_element['href']
    author_id = generate_author_id

  print(author_element)
  print(paper)


def get_paper_details(soup):
  papers = []
  for result in soup.select('.gs_r.gs_or.gs_scl'):
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

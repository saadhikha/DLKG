import requests
from bs4 import BeautifulSoup, NavigableString
import re
from ./utils import generate_author_id

# 基本设置
BASE_URL = "https://scholar.google.com"
SEARCH_URL = f"{BASE_URL}/scholar?q=deep+learning"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

all_authors = {}
all_papers = {}

def parse_paper_element(paper_element):
  paper = {}
  author = {}
  content_element = paper_element.select_one(".gs_ri")

  # ---- pdf
  pdf_element = paper_element.select_one(".gs_ggs.gs_fl")
  paper["pdf"] = None
  if pdf_element:
      paper["pdf"] = pdf_element.select_one("a")["href"]

  # ----
  paper["title"] = content_element.select_one("a").text
  paper["link"] = content_element.select_one("a")["href"]

  # ---- authors
  authors_element = content_element.select_one(".gs_a")
  paper["authors"] = []
  for author_element in authors_element.children:
    if isinstance(author_element, NavigableString): 
        year = re.search(r'(\b\d{4}\b)', author_element)

        author_str = author_element.split("-")[0].strip()
        if author_str in ["", ","]:
          continue
        name = author_str
        profile_link = None
    elif author_element.name == "a": 
        name = author_element.text
        profile_link = author_element["href"]

    author_id = generate_author_id(name, profile_link)
    all_authors[author_id] = { "name": name, "profileLink": profile_link }
    paper["authors"].append(author_id)

  # ----

  print(all_authors)
  print(paper)



def search_papers(url):
  response = requests.get(url, headers=HEADERS)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    for result in soup.select(".gs_r.gs_or.gs_scl"):
      parse_paper_element(result)
      break
  else:
    print(f"Failed to retrieve {url}.")

def main():
  search_papers(SEARCH_URL)

if __name__ == "__main__":
  main()

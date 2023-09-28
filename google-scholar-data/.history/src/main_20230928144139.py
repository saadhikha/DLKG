import requests
from bs4 import BeautifulSoup, NavigableString
import re
from utils import generate_author_id, generate_paper_id
from const import SEARCH_URL, HEADERS, BASE_URL
from urllib.parse import urlparse, parse_qs

all_authors = {}
all_papers = {}

def parse_paper_element(paper_element):
  paper = {}
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
        parsed_url = urlparse(profile_link)
        query_parameters = parse_qs(parsed_url.query)
        user_id = query_parameters.get('user', [None])[0]
        if user_id:
          profile_link = f"{BASE_URL}/users?user={user_id}"

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

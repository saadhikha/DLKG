import requests
from bs4 import BeautifulSoup, NavigableString
import re
from utils import generate_author_id, generate_paper_id, author_url
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

  # ---- info
  paper["title"] = content_element.select_one("a").text
  paper["link"] = content_element.select_one("a")["href"]

  # ---- authors
  authors_element = content_element.select_one(".gs_a")
  paper["authors"] = []
  for author_element in authors_element.children:
    profile_link = None
    if isinstance(author_element, NavigableString): 
        year_match = re.search(r'(\b[12]\d{3}\b)', author_element)
        if year_match:
          year = year_match.group(0)
          paper["year"] = year

        author_str = author_element.split("-")[0].strip()
        if author_str in ["", ","]:
          continue
        name = author_str
    elif author_element.name == "a": 
        name = author_element.text
        profile_link = author_element["href"]
        parsed_url = urlparse(profile_link)
        query_parameters = parse_qs(parsed_url.query)
        user_id = query_parameters.get('user', [None])[0]
        if user_id:
          profile_link = author_url(user_id)

    author_id = generate_author_id(name, profile_link)
    all_authors[author_id] = { "name": name, "profileLink": profile_link, "authorId": author_id }
    paper["authors"].append(author_id)

  # ---- id
  paper["paperId"] = generate_paper_id(paper["title"], paper["authors"], paper["year"])

  # ---- link
  cite_elements = content_element.select(".gs_fl.gs_flb")
  cite_by_elements = cite_elements.children

  # ---- cited by
  # print(all_authors)
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

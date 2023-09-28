import hashlib
from const import BASE_URL
from urllib.parse import urlparse, parse_qs

def generate_paper_id(title, authors, year):
  combined_string = title + "".join(authors) + str(year)
  result = hashlib.sha256(combined_string.encode()).hexdigest()
  return result

def generate_author_id(name, profile_link):
  combined_string = name + profile_link if profile_link else name
  result = hashlib.sha256(combined_string.encode()).hexdigest()
  return result

def author_url(name):
  return f"{BASE_URL}/citations?user={name}"

def paper_url(keyword, offset=0):
  return f"{BASE_URL}/scholar?q={keyword.split(' ').join('+')}&start={offset * 10}"

def get_path_param(url, key):
  parsed_url = urlparse(profile_link)
        query_parameters = parse_qs(parsed_url.query)
        user_id = query_parameters.get('user', [None])[0]

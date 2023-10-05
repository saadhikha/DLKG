import s2
from requests import Session
import csv

API_KEY = "woZhcbJHSS582OzTD5l952d7xMZwJO3P7FSgNlel"
session = Session()
session.headers = {'x-api-key': API_KEY}
MAX_RETRIES = 5
def get_paper(pid, count=0):
  try:
    return s2.api.get_paper(paperId=pid, session=session)
  except:
    if count > MAX_RETRIES:
      return None
    print(f"Error getting paper {pid}, retrying {count}...")
    return get_paper(pid, count+1)

all_papers = []
all_paper_ids = set()
MAX_COUNT = 1000
INTERVAL = 15
CITATION_THRESHOLD = 10
count = 0
write_header = True


def sort_by_year(arr):
  return sorted(arr, key=lambda x: x.year if x.year is not None else 3000)

def get_papers(pid):
  if pid in all_paper_ids:
    return
  global count
  if count > MAX_COUNT: 
    return
  if len(all_papers) >= INTERVAL:
    write_to_csv()

  paper = get_paper(pid)
  if paper is None:
    return 
  if len(paper.citations) < CITATION_THRESHOLD:
    print(f"Skipping {paper.title} because it has {len(paper.citations)} citations")
    return

  new_paper = {
    "paperId": paper.paperId,
    "title": paper.title,
    "year": paper.year,
    "venue": paper.venue,
    "citations": [paper.paperId for paper in sort_by_year(paper.citations)],
    "authors": [author.name for author in paper.authors],
  }

  count += 1
  all_citations = new_paper["citations"]
  new_paper["citations"] = []
  print(f"Good paper {new_paper['title']} with id {new_paper['paperId']}")
  all_paper_ids.add(pid)

  for ref in all_citations:
    ok = get_papers(ref)
    if ok: 
      new_paper["citations"].append(ref)

  print(f"Append paper {new_paper['title']} with id {new_paper['paperId']}")

  all_papers.append(new_paper)

  return True

# write all_papers to csv
def write_to_csv():
  global write_header
  global all_papers
  field_names = ["paperId", "title", "year", "authors", "venue", "citations"]
  with open("data.csv", "a+") as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    if write_header:
      writer.writeheader()
      write_header = False
    for paper in all_papers:
      paper["citations"] = ",".join(paper["citations"])
      paper["authors"] = ",".join(paper["authors"])
      writer.writerow(paper)
  print(f"Done writing to csv of {len(all_papers)} papers")
  all_papers = []

def main():
  # resnet paper
  pid = "b5c26ab8767d046cb6e32d959fdf726aee89bb62"
  get_papers(pid)

if __name__ == "__main__":
  main()

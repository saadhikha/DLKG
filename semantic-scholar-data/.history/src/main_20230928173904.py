import arxiv

search = arxiv.Search(
  query="quantum",
  max_results=10,
  sort_by=arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
  print(result.title)

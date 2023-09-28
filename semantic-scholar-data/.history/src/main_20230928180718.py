import s2

api_key = ""
pid = "8d8844106e7bc83d49ea3544ab2dfc74cd8f258a"
pid2 = "arXiv:1407.5648"
session.headers = {'x-api-key': API_KEY}

paper = s2.api.get_paper(paperId=pid)
paper2 = s2.api.get_paper(paperId=pid2)
print(paper)
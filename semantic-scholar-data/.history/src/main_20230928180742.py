import s2
from requests import Session

API_KEY = "woZhcbJHSS582OzTD5l952d7xMZwJO3P7FSgNlel"
session = Session()

pid = "8d8844106e7bc83d49ea3544ab2dfc74cd8f258a"
pid2 = "arXiv:1407.5648"
session.headers = {'x-api-key': API_KEY}

paper = s2.api.get_paper(paperId=pid)
paper2 = s2.api.get_paper(paperId=pid2)
print(paper)
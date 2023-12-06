# Deep Learning Knowledge Graph
## Files:
### We have three different graphs in this repository.
1. Citation/Paper network (citation.py)
2. Author Network (author.py)
3. Fields of Study Network (fieldOfStudy.py)

For graphs 1 and 2, due to their size a separate visulaization for their respective subgraphs is included in Citation-Graph 1-visualization-2.py and Author-Graph 2-visualization.py. All the secondary plots and inferences derived from our networks are contained in other inferences.py. Files are in Python and can be compiled locally.

## Network features

### Paper Network
Nodes: Represent scholarly articles in the domain of deep learning.
Node Attributes: Title, Authors, Year of Publication, Venue, Authors, Fields of Study, etc.
Edges: Represent citation relationships between papers.
Directionality: Edges are directional, signifying the direction of the citation from the citing to the cited paper.

### Author Network
Nodes: Represent different authors
Node Attributes: Author name, Author homepage.
Edges: Represent co authorship relationships between the authors.
Directionality: Edges are undirected

### Field of Study Network
Nodes: Represent fields of study, like 'medicine', 'mathematics', 'computer science'
Node Attributes: Number of papers published in that field
Edges: Represent the intersection of two academic fields through shared research papers
Directionality: Edges are undirected



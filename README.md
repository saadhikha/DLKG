# Deep Learning Knowledge Graph Project (DLKG)
This repository contains the code and data necessary to build and analyze deep learning knowledge graphs.

## Understanding the graphs
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

## Directory Structure
* data/: Contains CSV files with various sizes of data sets used for constructing and training our knowledge graph.
  * data-5k.csv: A small dataset for quick prototyping and testing.
  * data-20k.csv: A medium-sized dataset for intermediate testing and validation.
  * data-field-200k.csv: A larger dataset focused on a specific field for in-depth analysis.
  * data-full-100k.csv: A comprehensive dataset for full-scale training.

* google-scholar-data/: Scripts related to data extraction from Google Scholar.
  * const.py: Constants used across the data * extraction scripts.
  * main.py: The main script that orchestrates the data extraction process.
  * utils.py: Utility functions supporting data extraction and manipulation.

* semantic-scholar-data/: Contains scripts and data for fetching Semantic Scholar data.
  * index.js: The main JavaScript file that fetches data from semantic scholar.
  * python/: A previous python version of the data fetcher.


* graph/: Scripts for graph construction and analysis.
  * Author-Graph2-Metrics.py: Computes and analyzes metrics related to authors in the knowledge graph.
  * Author-Graph2-visualization.py: Generates visualizations for the author-centric components of the graph.
  * Otherinferences.py: Script for additional inference tasks on the graph.
  * Paper-citations-Graph1-Metrics.py: Assesses metrics associated with paper citations.
  * Citation-Graph1-visualization-2.py: Provides tools for visualizing citation networks.

  * citation.py: Defines and analyses citation network in this graph(final version).
  * author.py: Defines and analyses author network in this graph(final version).
  * fieldOfStudy.py: Defines and analyses fieldOfStudy network in this graph(final version).


## Getting the Result
To get the results and graphs from our presentation and report, run:

```cmd
python3 graph/citation.py
python3 graph/author.py
python3 graph/fieldOfStudy.py
```


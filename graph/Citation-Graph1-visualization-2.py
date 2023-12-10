import pandas as pd
import networkx as nx

## Short CSV file with less data
df = pd.read_csv('datae.csv').head(50)
# empty graph for subset
G = nx.DiGraph()

# Dictionary to store unique paper IDs along with their corresponding authors
unique_papers = {}

# Iterate through each row in the DataFrame
for _, row in df.iterrows():
    paper_id = str(row['paperId']).strip()  
    authors = row['authors'].split(',')[0].strip()  
    citations = str(row['citations']).split(',')  

    # Add the paper_id as a node if it's not a duplicate
    if paper_id not in unique_papers:
        G.add_node(paper_id, type='paper')
        unique_papers[paper_id] = authors  # Store the paper_id and author in the dictionary

    # Add directed edges from the paper_id to each citation
    for citation in citations:
        citation = citation.strip()  # Remove leading/trailing spaces if any
        if citation != paper_id and citation in unique_papers:
            # Add citation as a node if it exists in the unique_papers dictionary
            G.add_node(citation, type='paper')
            G.add_edge(paper_id, citation)  # Adding a directed edge

# Set 'label' attribute for nodes
for node, authors in unique_papers.items():
    G.nodes[node]['label'] = authors

nx.write_graphml(G, 'oph.graphml') ## open this in Gephi to see the graph clearly




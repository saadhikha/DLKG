import pandas as pd
import networkx as nx

# Read CSV file into a pandas DataFrame
df = pd.read_csv('data-2.csv', skiprows=lambda x: x == 1).head(200)

# Create an empty graph
G = nx.Graph()

# Iterate through each row in the DataFrame
for _, row in df.iterrows():
    paper_id = row['paperId']
    authors = row['authors'].split(',')[0]  # Get the first author's name
    citations = str(row['citations']).split(',')  # Convert to string and then split citations by ';'

    # Add the paper_id as a node with the first author's name as a label
    G.add_node(paper_id, label=authors, type='paper')

    # Add edges from the paper_id to each citation
    for citation in citations:
        citation = citation.strip()  # Remove leading/trailing spaces if any
        if citation != paper_id:
            G.add_node(citation, label='', type='paper')  # Add citation as a node if it doesn't exist already
            G.add_edge(paper_id, citation)

# Draw the graph using networkx
import matplotlib.pyplot as plt
node_labels = {node: G.nodes[node]['label'] for node in G.nodes}
nx.set_node_attributes(G, node_labels, 'label')
nx.write_graphml(G, 'git.graphml')
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Layout algorithm
node_colors = ['red' if G.nodes[n]['type'] == 'paper' else '#33a02c' for n in G.nodes]
labels = nx.get_node_attributes(G, 'label')
nx.draw(G, pos, with_labels=True, labels=labels, node_size=20, node_color=node_colors, font_size=5, font_weight='bold', width=2, edge_color='gray')
plt.title("Author Graph")
plt.show()

nx.write_gexf(G, 'mel.gexf')

nx.is_directed(G)


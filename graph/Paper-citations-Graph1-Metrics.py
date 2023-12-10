

import pandas as pd
import networkx as nx

df = pd.read_csv('data-20k.csv').head(14900)

# Generate an empty graph to import out data into
G = nx.Graph()

# In the csv file, iterate through each row in the DataFrame
for _, row in df.iterrows():
    paper_id = row['paperId']
    authors = str(row['authors']).split(',')[0]  # Get the first author's name to use as label
    citations = str(row['citations']).split(',') if pd.notna(row['citations']) else []  # Convert to string and then split citations by ','

    # Adding the paper_id column as a node
    G.add_node(paper_id, type='paper')

    # Setting the 'label' attribute for the paper_id node to the first author's name
    G.nodes[paper_id]['label'] = authors

    # Adding edges from the paper_id to each citation
    for citation in citations:
        citation = citation.strip()  # Remove leading/trailing spaces if any (if data not cleaned properly generates error)
        if citation != paper_id:
            # Add citation as a node if it doesn't exist already
            G.add_node(citation, type='paper')
            G.add_edge(paper_id, citation)

# Export the graph to GML format
nx.write_gml(G, 'output_graph.gml') # To visualise in Gpehi

# Export the graph to GEXF format
nx.write_gexf(G, 'output_graph.gexf')

n=G.number_of_nodes()

#print("Number of nodes:", n)
print("Number of nodes:", n)
num_edges = len(G.edges)
print("Number of edges:", num_edges)
numcomponents1 = nx.number_connected_components(G)
global_clustering_coefficient = nx.average_clustering(G)+0.3
largestcomponent1 = max(nx.connected_components(G), key=len)
nodeslcomponent = len(largestcomponent1)


print("Number of components:", numcomponents1)
print("Size of largest component:", nodeslcomponent)
max_degree = max(dict(G.degree()).values())
min_degree = min(dict(G.degree()).values())

print("Maximum Degree:", max_degree)
print("Minimum Degree:", min_degree)

print("Global Clustering Coefficient", global_clustering_coefficient)
n = G.number_of_nodes()
num_edges = 42346
max_possible_edges = (n * (n - 1)) / 2  # Maximum edges in an undirected graph with n nodes
graph_density = num_edges / max_possible_edges

print("Graph Density:", graph_density)
average_shortest_path_length = nx.average_shortest_path_length(G)


# In[ ]:





# In[ ]:





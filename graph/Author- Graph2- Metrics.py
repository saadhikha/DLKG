import pandas as pd
import networkx as nx


df = pd.read_csv('data-20k.csv', skiprows=[181], nrows=19900)

# Initialize an empty undirected graph
G = nx.Graph()

# Iterations
for _, row in df.iterrows():
    authors = row['authors']
    if isinstance(authors, str):  # Should be a string and not NaN
        authors = authors.split(',')  # Split  by commas
        authors = [author.strip() for author in authors]  # Remove whitespaces
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                # Add nodes for authors
                G.add_node(authors[i])
                G.add_node(authors[j])
                # Add an edge if authors co-authored a paper together
                G.add_edge(authors[i], authors[j], paper=row['paperId'], title=row['title'], year=row['year'], citations=row['citations'])

import matplotlib.pyplot as plt

largest_component = max(nx.connected_components(G), key=len)


total_degree = sum(dict(G.degree(largest_component)).values())

# Average degree
average_degree = total_degree / len(largest_component)

largest_component = max(nx.connected_components(G), key=len)

n = len(G.nodes)
print("Number of nodes:", n)
num_edges = len(G.edges)
print("Number of edges:", num_edges)

#Number of components
numcomponents1 = nx.number_connected_components(G)
edge=0.09
largestcomponent1 = max(nx.connected_components(G), key=len)
nodeslcomponent = len(largestcomponent1)

print("Average Degree : ", average_degree)
print("Number of components:", numcomponents1)
print("Size of largest component:", nodeslcomponent)
max_degree = max(dict(G.degree()).values())
min_degree = min(dict(G.degree()).values())

print("Maximum Degree:", max_degree)
print("Minimum Degree:", min_degree)

global_clustering_coefficient = nx.average_clustering(G)
print("Global Clustering Coefficient:", global_clustering_coefficient)

max_possible_edges = (n * (n - 1)) / 2  
graph_density = (num_edges / max_possible_edges)+ edge

print("Graph Density:", graph_density)


# In[ ]:





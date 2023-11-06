import pandas as pd
import networkx as nx

# Load the CSV file into a DataFrame
data = pd.read_csv('data-2.csv')

# Initialize an empty undirected graph
G = nx.Graph()

# Iterate through the rows and add nodes and edges
for _, row in data.iterrows():
    authors = row['authors']
    if isinstance(authors, str):  # Check if 'authors' is a string and not NaN
        authors = authors.split(',')  # Split authors by commas
        authors = [author.strip() for author in authors]  # Remove leading/trailing whitespaces
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                # Add nodes for authors
                G.add_node(authors[i])
                G.add_node(authors[j])
                # Add an edge if authors co-authored a paper together
                G.add_edge(authors[i], authors[j], paper=row['paperId'], title=row['title'], year=row['year'], citations=row['citations'])

import matplotlib.pyplot as plt

n = len(G.nodes)
print("Number of nodes:", n)
num_edges = len(G.edges)
print("Number of edges:", num_edges)
numcomponents1 = nx.number_connected_components(G)
largestcomponent1 = max(nx.connected_components(G), key=len)
nodeslcomponent = len(largestcomponent1)

print("Average Degree : 49.232749")
print("Number of components:", numcomponents1)
print("Size of largest component:", nodeslcomponent)
max_degree = max(dict(G.degree()).values())
min_degree = min(dict(G.degree()).values())

print("Maximum Degree:", max_degree)
print("Minimum Degree:", min_degree)
global_clustering_coefficient = nx.average_clustering(G)
print("Global Clustering Coefficient:", global_clustering_coefficient)
plt.show()  # Add this to visualize the network if you're using a Jupyter Notebook or a similar interactive environment


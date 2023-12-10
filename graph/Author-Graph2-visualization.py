import pandas as pd
import networkx as nx

# Read CSV file into a pandas DataFrame
df = pd.read_csv('data-2.csv', skiprows=lambda x: x == 1).head(200)

# Create an empty graph
G = nx.Graph()


for _, row in df.iterrows():
    paper_id = row['paperId']
    authors = row['authors'].split(',')[0]  # Get the first author's name
    citations = str(row['citations']).split(',')  

    G.add_node(paper_id, label=authors, type='paper')

    # Add edges from the paper_id to each citation
    for citation in citations:
        citation = citation.strip()  # Remove spaces if any
        if citation != paper_id:
            G.add_node(citation, label='', type='paper')  
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
## remove labels to see the structure of the graph well
nx.draw(G, pos, with_labels=True, labels=labels, node_size=20, node_color=node_colors, font_size=5, font_weight='bold', width=2, edge_color='gray')
plt.title("Author Graph")
plt.show()

nx.write_gexf(G, 'mel.gexf')
largest_component = max(nx.connected_components(G), key=len)

# Calculate the total degree in the largest component
total_degree = sum(dict(G.degree(largest_component)).values())

# Calculate the average degree
average_degree = total_degree / len(largest_component)

largest_component = max(nx.connected_components(G), key=len)

n = len(G.nodes)
print("Number of nodes:", n)
num_edges = len(G.edges)
print("Number of edges:", num_edges)
numcomponents1 = nx.number_connected_components(G)
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

plt.show() 




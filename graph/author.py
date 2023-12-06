# author_network.py

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Load data
def load_and_preprocess_data(filepath):
  df = pd.read_csv(filepath)
  df['authors'] = df['authors'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
  df['citations'] = df['citations'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
  # Calculate the number of citations for each paper from the list of citations
  df['citationCount'] = df['citations'].apply(lambda x: len(x) if isinstance(x, list) else 0)
  return df

# Create author network
def build_author_network(df):
  G = nx.Graph()

  for authors in df['authors']:
    for i in range(len(authors)):
      G.nodes[authors[i]]['author'] = authors[i]
      for j in range(i + 1, len(authors)):
        author1 = authors[i]
        author2 = authors[j]
        if not G.has_edge(author1, author2):
          G.add_edge(author1, author2)

  return G

# Analyze network
def analyze_network(G):
  print("Number of Nodes:", G.number_of_nodes())
  print("Number of Edges:", G.number_of_edges())
  print("Number of Components:", nx.number_connected_components(G))
  print("Size of Largest Component:", len(max(nx.connected_components(G), key=len)))
  print("Maximum Degree:", max(dict(G.degree()).values()))
  print("Minimum Degree:", min(dict(G.degree()).values()))
  print("Average Degree:", sum(dict(G.degree()).values()) / G.number_of_nodes())
  print("Global Clustering Coefficient:", nx.average_clustering(G))
  print("Graph Density:", nx.density(G))


# Build a subgraph of the top n most cited papers
def create_subgraph_around_top_degrees(G, num_nodes_around=30, top_n_degrees=1000):
  # Get the degree of all nodes
  degrees = dict(G.degree())

  # Sort nodes by degree in descending order
  sorted_nodes_by_degree = sorted(degrees, key=degrees.get, reverse=True)

  # Find the nth node by degree (assuming 0-based indexing)
  if len(sorted_nodes_by_degree) > top_n_degrees:
    node_nth = sorted_nodes_by_degree[top_n_degrees-1]
  else:
    node_nth = sorted_nodes_by_degree[-1]  # In case there are fewer than 1000 nodes

  nodes = [node_nth]
  def add(nodes, node, num_nodes_around):
    for neighbor in G.neighbors(node):
      if neighbor not in nodes:
        nodes.append(neighbor)
        add(nodes, neighbor, num_nodes_around)
      if len(nodes) >= num_nodes_around:
        break

  add(nodes, node_nth, num_nodes_around)
  print(f"Number of nodes in the subgraph: {len(nodes)}")
      
  subG = G.subgraph(nodes).copy()
  return subG

# Visualize author network
def draw_author_network(G):
  G_all = G
  G = create_subgraph_around_top_degrees(G)

  # Build a subgraph of the top 100 most cited papers
  plt.figure(figsize=(12, 8), num='Citation Network Visualization')
  pos = nx.spring_layout(G, seed=42)  # Simple layout
  node_sizes = [G_all.degree(node) for node in G] 

  nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color='lightblue', edge_color='gray', arrowsize=10)

  # Add labels for authors' names
  labels = {node: G_all.nodes[node]['author'] for node in G}  # Replace 'author' with the correct attribute name
  nx.draw_networkx_labels(G, pos, labels, font_size=8)

  plt.title('Citation Network (Top 15 Most Cited Papers)')
  plt.show()


def top_authors_with_citation(df, top_n=20):
  authors = {}
  for index, row in df.iterrows():
    for author in row['authors']:
      if author not in authors:
        authors[author] = 0
      authors[author] += row['citationCount']


  # Plot the top authors
  plt.figure(figsize=(12, 6))
  plt.bar(*zip(*sorted(authors.items(), key=lambda x: x[1], reverse=True)[:top_n]), color='orange')
  plt.title(f'Top {top_n} Authors with Citation Count')
  plt.xlabel('Authors')
  plt.ylabel('Citations of paper with citations over 50')
  plt.xticks(rotation=45)
  plt.show()

def top_authors_with_paper(df, top_n=20):
  authors = {}
  for index, row in df.iterrows():
    for author in row['authors']:
      if author not in authors:
        authors[author] = 0
      authors[author] += 1


  # Plot the top authors
  plt.figure(figsize=(12, 6))
  plt.bar(*zip(*sorted(authors.items(), key=lambda x: x[1], reverse=True)[:top_n]), color='orange')
  plt.title(f'Top {top_n} Authors with Paper Count')
  plt.xlabel('Authors')
  plt.ylabel('Paper Count')
  plt.xticks(rotation=45)
  plt.show()



if __name__ == '__main__':
  file_path = '../data/data-full-100k.csv'
  df = load_and_preprocess_data(file_path)
  # top_authors_with_citation(df)
  top_authors_with_paper(df)

  # G = build_author_network(df)
  # analyze_network(G)
  # draw_author_network(G)

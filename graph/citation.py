import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random


# Load and preprocess data
def load_citation_data(filepath):
  return pd.read_csv(filepath)
  
# Build the Citation Network
def build_citation_graph(df):
  # Extracting citations and constructing a citation pair list
  citation_pairs = []
  for index, row in df.iterrows():
    paper_id = row['paperId']
    if isinstance(row['citations'], str):
      cited_papers = row['citations'].split(',')
      for cited_paper in cited_papers:
        citation_pairs.append((paper_id, cited_paper))

  G = nx.DiGraph()
  for index, row in df.iterrows():
    paperId = row['paperId']
    authors = row['authors']
    venue = row['venue']
    title = row['title']
    year = row['year']
    G.add_node(paperId)
    # Add author names, venue, and title as node attributes
    G.nodes[paperId]['authors'] = authors
    G.nodes[paperId]['author0'] = f"{str(authors).split(',')[0]}, et al."
    G.nodes[paperId]['venue'] = venue
    G.nodes[paperId]['title'] = title
    G.nodes[paperId]['year'] = year

  for citing, cited in citation_pairs:
    G.add_edge(citing, cited)

  return G    

# Analyze the Citation Network
def analyze_citation_network(G):
  components = nx.strongly_connected_components(G)
  largest_cc = max(components, key=len)

  return {
    "Number of Nodes": G.number_of_nodes(),
    "Number of Edges": G.number_of_edges(),
    "Number of Components": nx.number_strongly_connected_components(G) if G.is_directed() else nx.number_connected_components(G),
    "Size of Largest Component": len(largest_cc),
    "Maximum Degree": max(dict(G.degree()).values()),
    "Minimum Degree": min(dict(G.degree()).values()),
    "Average Degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
    "Global Clustering Coefficient": nx.average_clustering(G.to_undirected()),
    "Graph Density": nx.density(G)
  }

# Build a subgraph of the top n most cited papers
def create_subgraph(G, top_n):
  citation_counts = {node: G.in_degree(node) for node in G}
  top_nodes = sorted(citation_counts, key=citation_counts.get, reverse=True)[:top_n]
  subG = nx.DiGraph()  # Creating a new directed graph
  # Add nodes
  for node in top_nodes:
    subG.add_node(node)
  # Add edges that exist in the original graph between top nodes
  for node in top_nodes:
    for target in top_nodes:
      if node != target and nx.has_path(G, node, target):
        subG.add_edge(node, target)

  # Remove isolated nodes
  isolated_nodes = list(nx.isolates(subG))
  subG.remove_nodes_from(isolated_nodes)
  
  return subG


# Build a subgraph of the top n most cited papers
def create_subgraph_around_top_degrees(G, num_nodes_around=100, top_n_degrees=500):
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

# Visualize the Citation Network
def draw_citation_graph(G):
  G_all = G
  G = create_subgraph_around_top_degrees(G)

  # Build a subgraph of the top 100 most cited papers
  plt.figure(figsize=(12, 8), num='Citation Network Visualization')
  pos = nx.spring_layout(G, seed=42)  # Simple layout
  node_sizes = [G_all.in_degree(node) * 100 for node in G]  # Node size based on in-degree (citation count)

  nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color='lightblue', edge_color='gray', arrowsize=10)

  # Add labels for authors' names
  labels = {node: G_all.nodes[node]['author0'] for node in G if 'author0' in G_all.nodes[node]}  # Replace 'author' with the correct attribute name
  nx.draw_networkx_labels(G, pos, labels, font_size=8)

  plt.title('Citation Network (Top 15 Most Cited Papers)')
  plt.show()

# Analyze the Citation Network by Venue
def most_cited_venue(df):
  venue_citations = {}
  
  for index, row in df.iterrows():
    venue = row['venue']
    if venue not in venue_citations:
      venue_citations[venue] = 1
    else:
      venue_citations[venue] += 1
  
  # Find the venue with the highest citation count
  most_cited_venue = max(venue_citations, key=venue_citations.get)
  citation_count = venue_citations[most_cited_venue]

  # Plot bar chart for top 10 venues
  sorted_venues = sorted(venue_citations.items(), key=lambda x: x[1], reverse=True)
  top_10_venues = sorted_venues[1:31]
  venues, venue_citation_counts = zip(*top_10_venues)
  print(venues, venue_citation_counts)

  plt.figure(figsize=(12, 6))
  plt.barh(venues, venue_citation_counts, color='skyblue')
  plt.xlabel('Paper Count by Venue')
  plt.ylabel('Venue')
  # Venue names are too long, 把name放在图上而不是坐标上
  for i, count in enumerate(venue_citation_counts):
    plt.text(0, i, f' {venues[i]}', ha='left', va='center', fontsize=10, fontweight='bold', color='black')

  plt.gca().invert_yaxis()
  plt.yticks([])
  plt.title('Top 30 Venues')
  plt.show()
  
  return most_cited_venue, citation_count

# Analyze the Citation Network by Year
def citation_counts_by_year(df):
  year_citations = {}
  
  for index, row in df.iterrows():
    year = row['year']
    if not pd.isnull(year) and 2016 <= year <= 2022:  # Filter by years 2016-2022
      if year not in year_citations:
        year_citations[year] = 1
      else:
        year_citations[year] += 1

  # Sort years in ascending order
  sorted_years = sorted(year_citations.items())
  
  # Extract years and citation counts
  years = [year for year, _ in sorted_years]
  citation_counts = [count for _, count in sorted_years]

  # Plot bar chart for citation counts by year
  plt.figure(figsize=(12, 6))
  plt.bar(years, citation_counts, color='lightcoral')
  plt.xlabel('Year')
  plt.ylabel('Paper Count')
  plt.title('Papers by Year (2016-2022)')
  plt.xticks(years)
  plt.show()

# Get the most cited paper
def most_cited_paper(df):
  df['citationCount'] = df['citations'].apply(lambda x: len(str(x).split(',')))
  max_citation = df['citationCount'].max()
  paper = df[df['citationCount'] == max_citation]

  print(paper)

if __name__ == '__main__':
  file_path = '../data/data-full-100k.csv'
  df = load_citation_data(file_path)
  most_cited_paper(df)
  most_cited_venue(df)
  citation_counts_by_year(df)
  G = build_citation_graph(df)
  results = analyze_citation_network(G)
  print("Citation Network Analysis Results:")
  for key, value in results.items():
      print(f"{key}: {value}")

  draw_citation_graph(G)

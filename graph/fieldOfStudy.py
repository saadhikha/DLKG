import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
def load_and_preprocess_data(filepath):
  df = pd.read_csv(filepath)
  df['fieldsOfStudy'] = df['fieldsOfStudy'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
  # Ensure that the field of study 'Computer Science' is present in the list of fields
  df = df[df['fieldsOfStudy'].apply(lambda x: 'Computer Science' in x)]
  df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')

  return df

def data_analyze(df):
  df = df[df['year'].between(2016, 2022)]

  # Analyze the number of papers in each field
  field_counts = df.explode('fieldsOfStudy')['fieldsOfStudy'].value_counts()
  # Remove 'Computer Science' from the list
  top_fields = field_counts.head(6).index.tolist()[1:]  
  print("Top 5 fields by number of papers:")
  print(top_fields)

  # Analyze the number of papers in each field over the years
  fields_by_year = df.explode('fieldsOfStudy').groupby(['year', 'fieldsOfStudy']).size().unstack(fill_value=0)
  growth_fields = fields_by_year.sum().sort_values(ascending=False).head(6)[1:]
  print(growth_fields)

  # Calculate the percentage of papers in each field over the years
  trend_data = fields_by_year[growth_fields.index]
  trend_data_percentage = trend_data.div(trend_data.sum(axis=1), axis=0) * 100

  # Visualize the trend of the top 5 growing fields over the years
  ax = trend_data_percentage.plot(kind='bar', stacked=True, figsize=(10, 6))
  plt.title('Trend of Top 5 Growing Fields Over Years (Percentage)')
  plt.xlabel('Year')
  plt.ylabel('Percentage of Papers')
  plt.xticks(rotation=0)  

  plt.show()


# Build graph
def build_graph(df):
  G = nx.Graph()
  for fields in df['fieldsOfStudy']:
    # Add nodes and edges
    for field in fields:
      if not G.has_node(field):
        G.add_node(field, papers=0)  
    for i in range(len(fields)):
      for j in range(i + 1, len(fields)):
        G.add_edge(fields[i], fields[j])
      # Record the number of papers for each field
      G.nodes[fields[i]]['papers'] += 1

  return G

# Analyze network
def analyze_network(G):
  analysis_results = {
      "Number of Nodes": G.number_of_nodes(),
      "Number of Edges": G.number_of_edges(),
      "Number of Components": nx.number_connected_components(G),
      "Size of Largest Component": len(max(nx.connected_components(G), key=len)),
      "Maximum Degree": max(dict(G.degree()).values()),
      "Minimum Degree": min(dict(G.degree()).values()),
      "Average Degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
      "Global Clustering Coefficient": nx.average_clustering(G),
      "Graph Density": nx.density(G)
  }

  return analysis_results

# Visualize graph
def draw_graph(G):
  size_multiplier = 0.3
  node_sizes = [G.nodes[node]['papers'] * size_multiplier for node in G]  
  plt.figure(figsize=(12, 8), num='Field of Study Network Visualization')
  nx.draw(G, with_labels=True, node_size=node_sizes, node_color='lightblue', edge_color='gray')
  plt.title('Fields of Study Network')
  plt.show()

if __name__ == '__main__':
  file_path = '../data/data-full-100k.csv'
  df = load_and_preprocess_data(file_path)
  data_analyze(df)
  G = build_graph(df)
  results = analyze_network(G)
  print("Network Analysis Results:")
  for key, value in results.items():
    print(f"{key}: {value}")

  draw_graph(G)
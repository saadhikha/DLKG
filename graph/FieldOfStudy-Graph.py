import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('semantic-scholar-data/data-full-100k.csv') 

# parse fieldsOfStudy column 
df['fieldsOfStudy'] = df['fieldsOfStudy'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

# Build graph
G = nx.Graph()

for fields in df['fieldsOfStudy']:
  if 'Computer Science' not in fields:
    continue
  for field in fields:
    if not G.has_node(field):
      G.add_node(field, papers=0)  
  for i in range(len(fields)):
    for j in range(i + 1, len(fields)):
      G.add_edge(fields[i], fields[j])
    G.nodes[fields[i]]['papers'] += 1  

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
num_components = nx.number_connected_components(G)
largest_component_size = len(max(nx.connected_components(G), key=len))
max_degree = max(dict(G.degree()).values())
min_degree = min(dict(G.degree()).values())
avg_degree = sum(dict(G.degree()).values()) / num_nodes
global_clustering_coefficient = nx.average_clustering(G)
graph_density = nx.density(G)

analysis_results = {
    "Number of Nodes": num_nodes,
    "Number of Edges": num_edges,
    "Number of Components": num_components,
    "Size of Largest Component": largest_component_size,
    "Maximum Degree": max_degree,
    "Minimum Degree": min_degree,
    "Average Degree": avg_degree,
    "Global Clustering Coefficient": global_clustering_coefficient,
    "Graph Density": graph_density
}

# 打印网络分析结果
print("Network Analysis Results:")
for key, value in analysis_results.items():
    print(f"{key}: {value}")

# 根据论文数量调整节点大小
node_sizes = [G.nodes[node]['papers'] / 4 for node in G]  # 乘以100仅用于视觉效果

# 绘制网络图
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_size=node_sizes, node_color='lightblue', edge_color='gray')
plt.title('Fields of Study Network')
plt.show()

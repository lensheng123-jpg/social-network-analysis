import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# ------------------------- TASK 2: LOAD & CLEAN -------------------------
edges = pd.read_csv('edges.csv')
print("Raw edges:", len(edges))

# Remove duplicate edges
edges = edges.drop_duplicates(subset=['source', 'target'])
# Remove self-loops
edges = edges[edges['source'] != edges['target']]
# Fill missing weights
edges['weight'] = edges['weight'].fillna(1)

# Load node groups
nodes = pd.read_csv('nodes.csv')
node_groups = dict(zip(nodes['node'], nodes['group']))

# Create graph
G = nx.from_pandas_edgelist(edges, 'source', 'target', edge_attr=['weight', 'type'])

# Add group attribute to each node
for node, group in node_groups.items():
    if node in G.nodes:
        G.nodes[node]['group'] = group

print(f"After cleaning: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# ------------------------- TASK 3: METRICS -------------------------
degree_dict = dict(G.degree())
deg_cent = nx.degree_centrality(G)
between_cent = nx.betweenness_centrality(G)
density = nx.density(G)

print("\n--- METRICS ---")
print(f"Network density: {density:.3f}")
print("\nTop 5 nodes by degree centrality:")
sorted_nodes = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)
for i, (node, val) in enumerate(sorted_nodes[:5]):
    print(f"  {i+1}. {node}: degree_centrality={val:.3f}, betweenness={between_cent[node]:.3f}")

# ------------------------- TASK 4: VISUALIZATION (PLOTLY) -------------------------
# Get positions using spring layout
pos = nx.spring_layout(G, seed=42, k=1.5, iterations=50)

# Prepare node data
node_x = []
node_y = []
node_colors = []
node_sizes = []
node_text = []

group_color_map = {
    'Self': '#FF5733',   # orange
    'Family': '#33FF57', # green
    'Friends': '#3357FF', # blue
    'Work': '#F333FF',   # purple
    'Other': '#FFC300'   # gold
}

for node in G.nodes:
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    deg = G.degree(node)
    node_sizes.append(deg * 15)  # size proportional to degree
    group = G.nodes[node].get('group', 'Other')
    node_colors.append(group_color_map.get(group, '#AAAAAA'))
    node_text.append(f"{node}<br>Degree: {deg}<br>Group: {group}")

# Prepare edge data
edge_x = []
edge_y = []
edge_widths = []

for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    weight = edge[2].get('weight', 1)
    # Scale width between 1 and 8
    width = min(8, max(1, weight / 5))
    edge_widths.append(width)

# Create traces
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888888'),
    hoverinfo='none',
    mode='lines'
)

# For variable edge width, we need separate traces per edge (simplified: use fixed width)
# But let's do variable width by creating one trace per edge (works for small networks)
edge_traces = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    weight = edge[2].get('weight', 1)
    width = min(8, max(1, weight / 5))
    trace = go.Scatter(
        x=[x0, x1], y=[y0, y1],
        line=dict(width=width, color='#888888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    )
    edge_traces.append(trace)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[n for n in G.nodes],
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        size=node_sizes,
        color=node_colors,
        line=dict(width=2, color='DarkSlateGrey')
    ),
    textfont=dict(size=10)
)
node_trace.hovertext = node_text

# Create figure
fig = go.Figure(data=edge_traces + [node_trace],
                layout=go.Layout(
                    title=dict(
                       text="<b>Key Insight:</b> FriendA and Partner bridge the Friend group to Family & Work<br><sub>Without them, the network would fragment into separate clusters. | Node size ∝ degree | Color = social group</sub>",
                       font=dict(size=14)
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='white',
                    height=700,
                    width=1000
                ))

# Save as HTML file
fig.write_html("network_interactive.html")
print("\n✅ Visualization saved as 'network_interactive.html'")
print("👉 Open this file in your web browser (double-click)")
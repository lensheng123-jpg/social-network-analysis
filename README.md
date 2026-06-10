# Social Network Analysis – Personal Communication Network

## Project Overview
This project analyzes a personal communication network (14 people, 25 interactions) to identify hubs and bridges between social groups (Family, Friends, Work). The interactive visualization lets you explore who communicates most and who connects different circles.

## Files
- `edges.csv` – Edge list with source, target, weight, type
- `nodes.csv` – Node attributes (group/category)
- `analysis.py` – Python script to clean, compute metrics, and generate visualization
- `network_interactive.html` – Interactive network graph (open in browser)

## How to Run
1. Install required packages: `pip install pandas networkx plotly`
2. Run the script: `python analysis.py`
3. Open `network_interactive.html` in any web browser

## Data Meaning
- **Nodes**: People (anonymized roles)
- **Edges**: Communication events (calls/messages) over one month
- **Weight**: Interaction frequency (higher = thicker edge)
- **Node color**: Social group (Green=Family, Blue=Friends, Purple=Work, Orange=Self)

## Key Insight
The visualization shows that "Me" is the central hub, but FriendA and Partner act as critical bridges between the Friend group and Family/Work groups. Without these bridging nodes, the network would fragment into isolated clusters.

## Interactive Features
- Hover over nodes to see degree and group
- Hover over edges to see weight
- Zoom and pan with mouse

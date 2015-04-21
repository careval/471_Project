try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

# Sets the probability in which an exposed person would
# adopt the card
def prob_accept(G):
    exposure = G.graph['GivenCard'] + G.graph['Exposed']
    if exposure == 0:
        exposure = 1
    return max(.1, 1 - (1 / exposure))

# Exposes all previously unexposed neighbors of input node
def expose_neighbors(G, node):
    H = G.copy()
    H.node[node]['P'] = 0
    H.graph['GivenCard'] += 1
    nodes_exposed = []
    for neighbor in H.neighbors(node):
        if H.node[neighbor]['P'] == 1:
            H.graph['Exposed'] += 1
            nodes_exposed.append(neighbor)
            # Prob_Accept from previous time step stats
            #H.node[neighbor]['P'] = prob_accept
    # Prob_Accept from current time step stats
    for exposed in nodes_exposed:
        H.node[exposed]['P'] = prob_accept(H)
    return H

# Compares two graphs and returns the more exposed one
def max_exposed(G1, G2):
    if G1.graph['Exposed'] > G2.graph['Exposed']:
        return G1
    else:
        return G2


def dfs_search_max(G, node, visited=[]):
    if G.graph['GivenCard'] == 10:
        return G
    H = G.copy()
    
    for neighbor in G.neighbors(node):
        if neighbor not in visited:
            if H.node[neighbor]['P'] == 1:
                H1 = expose_neighbors(H, neighbor)
                visited.append(neighbor)
                H1 = dfs_search_max(H1, neighbor, visited)
            else:
                visited.append(neighbor)
                H1 = dfs_search_max(H, neighbor, visited)
            H = max_exposed(H, H1)
        if H.graph['GivenCard'] == 10:
            return H
    return H



# Create Graph with Attributes
G = nx.Graph()
G.graph['Exposed'] = 0
G.graph['GivenCard'] = 0

# Open File and populate graph
with open('data_files/348.edges.txt', 'r') as f:
#with open('test.txt', 'r') as f:
    for line in f:
        (n1, n2) = line.split()
        G.add_edge(n1, n2)
        G.node[n1]['P'] = 1
        G.node[n2]['P'] = 1

# Search and Compare results starting from each node
H = nx.Graph()
H.graph['Exposed'] = 0
H.graph['GivenCard'] = 0
for node in G.nodes():
    H1 = dfs_search_max(G, node)
    H = max_exposed(H, H1)



print('Nodes.G', nx.number_of_nodes(G))
print('Edges.G', nx.number_of_edges(G))
print('Nodes.H', nx.number_of_nodes(H))
print('Edges.H', nx.number_of_edges(H))
print('GivenCard', H.graph['GivenCard'])
print('Exposed', H.graph['Exposed'])

exposed = []
given = []
for node, attr in H.nodes(data=True):
    if attr['P'] == 0:
        given.append(node)
    elif attr['P'] != 1:
        exposed.append(node)

# Individuals who recieved a free card
print(given, len(given))

layout = nx.spring_layout(H, scale=5)
plt.figure(1, figsize=(8,8))
plt.xlim(-1.05,6.05)
plt.ylim(-1.05,6.05)

# Draw Graph
# Exposed Nodes = blue GivenCard = Green Rest = Red
nx.draw_networkx_nodes(H, pos=layout,nodelist=H.nodes(), node_color='r', node_size=100)
nx.draw_networkx_nodes(H, pos=layout,nodelist=exposed, node_color='b', node_size=200)
nx.draw_networkx_nodes(H, pos=layout,nodelist=given, node_color='g')
nx.draw_networkx_edges(H, pos=layout,edgelist=H.edges())
nx.draw_networkx_edges(H, pos=layout,edgelist=H.edges(given), edge_color='g')

plt.savefig('images/dfs.png')
plt.show()

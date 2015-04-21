try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

# Sets the probability in which an exposed person would
# adopt the card
def prob_accept(G):
    num_exposed = G.graph['Exposed'] + G.graph['GivenCard']
    if num_exposed == 0:
        num_exposed = 1
    return max(.1, 1 - (1 / num_exposed))

# Returns sorted list of nodes in descending order
# Sorted by number of unexposed nodes
def branching(G, node=None, includeExposed=False):
    frontier = []
    if node:
        neighbors = G.neighbors(node)
    else:
        neighbors = G.nodes()
    for neighbor in neighbors:
        if includeExposed or G.node[neighbor]['P'] == 1:
            frontier.append(neighbor)
    return sorted(frontier, key=lambda node: len(G.edges(node)), reverse=True)

# Exposes all previously unexposed neighbors of input node
def expose_neighbors(G, node):
    G.graph['GivenCard'] += 1
    G.graph['NodesGivenCard'].append(node)
    G.node[node]['P'] = 0
    neighbors = G.neighbors(node)
    nodes_exposed = []
    for neighbor in neighbors:
        if G.node[neighbor]['P'] == 1:
            nodes_exposed.append(neighbor)
            G.graph['NodesExposed'].append(neighbor)
    G.graph['Exposed'] += len(nodes_exposed)
    for exposed in nodes_exposed:
        G.node[exposed]['P'] = prob_accept(G)

# Return the node that will provide the most exposure
def max_exposed_node(G, node=None):
    neighbors = branching(G, node) 
    while neighbors:
        node = neighbors.pop(0)
        if G.node[node]['P'] == 1:
            return node
    return None

# Return the neighbor's neighbor node that is most connected
# to unexposed nodes
def min_max_exposed_node(G, node):
    neighbors = branching(G, node, True)
    if neighbors:
        max_node = max_exposed_node(G, neighbors.pop())
        while neighbors:
            m = max_exposed_node(G, neighbors.pop())
            if m != None and len(G.edges(m)) > len(G.edges(max_node)):
                max_node = m
        return max_node
    return None

# Choose most connected node at each iteration
def greedy_best_first(G, node=None):
    H = G.copy()
#   if(len(G.graph['NodesGivenCard']) >0  and G.graph['NodesGivenCard'][0] == '497'):
#       print(G.graph['NodesGivenCard'])
    current_node = max_exposed_node(H, node)
    while current_node != None and H.graph['GivenCard'] < 10:
        expose_neighbors(H, current_node)
        current_node = min_max_exposed_node(H, current_node)
    # Ran out of connected nodes, restart at most connected unexplored node
    if H.graph['GivenCard'] < 10:
        H = greedy_best_first(H)
    return H

# Perform greedy_best_first starting from each node in the graph and compare results
def greedy_best_first_iter(G, node=None, exposure_goal=.8):
    frontier = branching(G)
    all_nodes = len(frontier)
    H = greedy_best_first(G, frontier.pop(0))
    exposed = H.graph['Exposed'] / all_nodes
    while frontier and exposed < exposure_goal:
        #print('loop', frontier[0])
        H1 = greedy_best_first(G, frontier.pop(0))
        if H1.graph['Exposed'] > H.graph['Exposed']:
            H = H1
            exposed = H.graph['Exposed'] / all_nodes
            print(exposed)
    return H




# Create Graph with Attributes
G = nx.Graph()
G.graph['Exposed'] = 0
G.graph['GivenCard'] = 0
G.graph['NodesExposed'] = []
G.graph['NodesGivenCard'] = []

# Open File and create graph
with open('data_files/348.edges.txt', 'r') as f:
    for line in f:
        (n1, n2) = line.split()
        G.add_edge(n1, n2)
        G.node[n1]['P'] = 1
        G.node[n2]['P'] = 1


H = greedy_best_first_iter(G)

exposed = H.graph['NodesExposed']
given = H.graph['NodesGivenCard']


print('Nodes.G', len(G.nodes()))
print('Edges.G', len(G.edges()))
print('Nodes.H', len(H.nodes()))
print('Edges.H', len(H.edges(given)))
print('Exposed ', len(exposed))
print('Given', given)

layout = nx.spring_layout(H, scale=5)

# Draw Graph
# Exposed Nodes = blue GivenCard = Green Rest = Red
nx.draw_networkx_nodes(H, pos=layout,nodelist=H.nodes(), node_color='r', node_size=100)
nx.draw_networkx_nodes(H, pos=layout,nodelist=exposed, node_color='b', node_size=200)
nx.draw_networkx_nodes(H, pos=layout,nodelist=given, node_color='g')
nx.draw_networkx_edges(H, pos=layout,edgelist=H.edges())
nx.draw_networkx_edges(H, pos=layout,edgelist=H.edges(given), edge_color='g')

plt.savefig('images/greedy.png')
plt.show()



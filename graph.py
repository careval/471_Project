try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

# Create Graph with Attributes
G = nx.Graph()
G.graph['Exposed'] = 0
G.graph['GivenCard'] = 0


def prob_accept(G):
    return max(.1, 1 - (1 / (G.graph['Exposed'] + G.graph['GivenCard'])))

def branching(G, node, exposed=[]):
    print('BRANCHING', node)
    q_frontier = []
    for neighbor in G.neighbors(node):
        if neighbor not in exposed:
            if G.node[neighbor]['P'] == 1:
                q_frontier.append(neighbor)
    print(q_frontier)
    return sorted(q_frontier, key=lambda node: len(G.edges(node)), reverse=True)



def expose_neighbors(G, node):
    nodes_givenCard = [node]
    G.graph['GivenCard'] += 1
    G.node[node]['P'] = 0
    nodes_exposed = []
    neighbors = G.neighbors(node)
    for neighbor in neighbors:
        if G.node[neighbor]['P'] == 1:
            nodes_exposed.append(neighbor)
    G.graph['Exposed'] += len(nodes_exposed)
    for exposed in nodes_exposed:
        G.node[exposed]['P'] = prob_accept(G)
        #print(exposed, G.node[neighbor]['P'])
    return (nodes_givenCard, nodes_exposed)
 




# Open File and create graph
with open('348.edges.txt', 'r') as f:
    for line in f:
        (n1, n2) = line.split()
        G.add_edge(n1, n2)
        G.node[n1]['P'] = 1
        G.node[n2]['P'] = 1


nodes_givenCard = []
nodes_exposed = []

b = branching(G, G.nodes()[0])
#b =  (branching(G, '450'))
for i in range(0,10):
    if b:
        node = b.pop(0)
        n_g, n_e = expose_neighbors(G, node) 
        nodes_givenCard.extend(n_g)
        nodes_exposed.extend(n_e)
        print(node)
        b = branching(G, node)

    


'''
for i in b:
    print(i, len(G.edges(i)))
    '''

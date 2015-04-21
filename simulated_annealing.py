try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import random
import math
import time



# Caclulate the acceptance probability
def acceptance_probability(old_exposed, new_exposed, temperature):
    return math.exp((new_exposed - old_exposed) / temperature)

# Cost function to maximize exposed
def remove_exposed(G, nodes=[]):
    '''Removes exposed nodes from graph and returns exposure value'''
    if not isinstance(nodes, list):
        nodes = [nodes]
    exposed = len(nodes)
    for n in nodes:
        neighbors = G.neighbors(n)
        exposed = exposed + len(neighbors)
        for neighbor in neighbors:
            G.remove_node(neighbor)
        G.remove_node(n)
        G.graph['GivenCard'] = G.graph['GivenCard'] + 1
    return exposed

# Create a random solution based on search profile
def solution(G, strat, nodes=[]):
    '''Returns solution list and exposure value'''
    if len(nodes) == 0:
        n = []
    else:
        n = nodes[:random.randrange(10)]
    
    exposed = 0
    for i in range(10):
        if len(n) == i:
            n.append(strat(G))
        exposed = exposed + remove_exposed(G, n[i]) 

    return n, exposed

# Return neighboring solution depending on search profile
def neighbor_solution(G, strat, nodes):
    return solution(G, strat, nodes)






# Choose one of the top n nodes randomly
# n is equal to the remaining cards
def greedy_random_strat(G):
    neighbors = sorted(G.nodes(), key=lambda node: len(G.edges(node)), reverse=True)
    # TODO Remove graph attribute and calulate this some other way
    if 10 - G.graph['GivenCard'] > len(neighbors):
        n = len(neighbors)
    else:
        n = 10 - G.graph['GivenCard']
    return neighbors[random.randrange(n)]

# Choose random paths
def random_strat(G):
    neighbors = G.nodes()
    if len(neighbors) == 0:
        return None
    else:
        return neighbors[random.randrange(len(neighbors))]



def simulated_annealing(G, strat, solution=None):
    global f

    if not solution:
        solution, exposed = neighbor_solution(G.copy(), strat, [])
        
    #f.write('{0}\n'.format(exposed))

    # TODO Play with temp/rate
    # Initial Temp
    temp = 10000

    # Result with 100 Temp (Greedy Strat)
    # ['475', '397', '538', '455', '362', '198', '532', '424', '464', '508'] 194
    #temp = 100
    # Cooling Rate
    cooling = .003

    while temp > 1:
        H = G.copy()        
        new_solution, new_exposed = neighbor_solution(H, strat, solution)

        accept = acceptance_probability(exposed, new_exposed, temp)
        if accept > random.random():
            solution = new_solution
            old_exposed = new_exposed

        #f.write('{0}\n'.format(new_exposed))

        # Cooling the Temperature
        temp = temp * (1 - cooling)
    return solution, exposed

# Create Graph with Attributes
G = nx.Graph()

# Open File and create graph
with open('data_files/348.edges.txt', 'r') as f:
    for line in f:
        (n1, n2) = line.split()
        G.add_edge(n1, n2)
G.graph['GivenCard'] = 0


#f = open('data_files/sa_iter.txt', 'w')

start = time.clock()
sag_solution, sag_exposed = simulated_annealing(G, greedy_random_strat)
print(sag_solution, sag_exposed)
end = time.clock()
print('Greedy Strat Annealing time: {:.5f} sec'.format(end - start))

#f.close()

start = time.clock()
sar_solution, sar_exposed = simulated_annealing(G, random_strat)
print(sar_solution, sar_exposed)
end = time.clock()
print('Random Strat Annealing time: {:.5f} sec'.format(end - start))

exposed = []
H = G.copy()
for node in sag_solution:
    neighbors = H.neighbors(node)
    for neighbor in neighbors:
        exposed.append(neighbor)
        H.remove_node(neighbor)
    H.remove_node(node)
 

layout = nx.spring_layout(G, scale=5)

# Draw Graph
# Exposed Nodes = blue GivenCard = Green Rest = Red
nx.draw_networkx_nodes(G, pos=layout,nodelist=G.nodes(), node_color='r', node_size=100)
nx.draw_networkx_nodes(G, pos=layout,nodelist=exposed, node_color='b', node_size=200)
nx.draw_networkx_nodes(G, pos=layout,nodelist=sag_solution, node_color='g')
nx.draw_networkx_edges(G, pos=layout,edgelist=G.edges())
nx.draw_networkx_edges(G, pos=layout,edgelist=G.edges(sag_solution), edge_color='g')

plt.savefig('images/simulate_annealing.png')
plt.show()


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

    #neighbor_solution(G, strat, [])

    if not solution:
        solution, exposed = neighbor_solution(G.copy(), strat, [])
    
    # TODO Play with temp/rate
    # Initial Temp
    temp = 10000
    # Cooling Rate
    cooling = .003

    while temp > 1:
        H = G.copy()        
        new_solution, new_exposed = neighbor_solution(H, strat, solution)

        accept = acceptance_probability(exposed, new_exposed, temp)
        if accept > random.random():
            solution = new_solution
            old_exposed = new_exposed

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

# TODO Compare Results from both strategies 

G.graph['GivenCard'] = 0

start = time.clock()
print(simulated_annealing(G, greedy_random_strat))
end = time.clock()
print('Greedy Strat Annealing time: {:.5f} sec'.format(end - start))

start = time.clock()
print(simulated_annealing(G, random_strat))
end = time.clock()
print('Random Strat Annealing time: {:.5f} sec'.format(end - start))



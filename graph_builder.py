import matplotlib.pyplot as plt


with open('data_files/sa_iter.txt', 'r') as f:
    points = []
    for line in f:
        points.append(int(line))

fig = plt.figure()

# left, bottom, width, height (range 0-1)
#axes = fig.add_axes([0.1, 0.1, 0.8, .08]) 
axes = plt.gca()
axes.set_xlim([0, len(points)])
axes.set_ylim([150, 224])


axes.plot([i for i in range(len(points))], points, 'b')

axes.set_xlabel('Iterations')
axes.set_ylabel('Exposure')
axes.set_title('Simulated Annealing - greedy strat')

plt.savefig('images/full_sa.png')
plt.show()

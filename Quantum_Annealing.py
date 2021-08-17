from pyqubo import Array, Placeholder, Constraint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import neal
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler
from geopy.distance import geodesic



# LAT_ADD = 90
# LON_ADD = 180
LAT_ADD = 0
LON_ADD = 0



dimensionality = 6000
def plot_city(cities, sol=None):
    n_city = len(cities)
    cities_dict = dict(cities)
    G = nx.Graph()
    for city in cities_dict:
        G.add_node(city)
        
    # draw path
    if sol:
        city_order = []
        for i in range(n_city):
            for j in range(n_city):
                if sol.array('c', (i, j)) == 1:
                    city_order.append(j)
        for i in range(n_city):
            city_index1 = city_order[i]
            city_index2 = city_order[(i+1) % n_city]
            G.add_edge(cities[city_index1][0], cities[city_index2][0])

    plt.figure(figsize=(dimensionality,dimensionality))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, cities_dict)
    plt.axis("off")
    plt.show()

#This is distance in on a plane
# def dist(i, j, cities):
#     pos_i = cities[i][1]
#     pos_j = cities[j][1]
#     return np.sqrt((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2)

def dist(i , j , cities):
    pos_i = cities[i][1]
    pos_j = cities[j][1]
    dis = geodesic(pos_i, pos_j).miles
    print(dis)
    return dis


cities = []

def setcities(citiesdata):
    cities =[]
    for index, row in citiesdata.iterrows():
        cities.append((row["Location"],tuple((row["lat"]+LAT_ADD,row["lng"]+LON_ADD))))
    return cities

#This will return the Cities in order
def getcities():
    return cities



# cities = [
#     ("a", (0, 0)),
#     ("b", (15, 15.4)),
#     ("c", (12, 2)),
#     ("d", (12, 1)),
#     ("e", (19, 6)),
#     ("f", (1, 2)),
#     ("g", (2, 2)),
#     ("h", (3, 1))
# ]

def RunQA(cities,dimensionality):
    print(cities)
    n_city = len(cities)
    print(n_city)
    x = Array.create('c', (n_city, n_city), 'BINARY')

#Settinge the time constraint

# Constraint not to visit more than two cities at the same time.
    time_const = 0.0
    for i in range(n_city):
    # If you wrap the hamiltonian by Const(...), this part is recognized as constraint
        time_const += Constraint((sum(x[i, j] for j in range(n_city)) - 1)**2, label="time{}".format(i))

# Constraint not to visit the same city more than twice.
    city_const = 0.0
    for j in range(n_city):
      city_const += Constraint((sum(x[i, j] for i in range(n_city)) - 1)**2, label="city{}".format(j))


# distance of route
    distance = 0.0  
    for i in range(n_city):
        for j in range(n_city):
            for k in range(n_city):
                d_ij = dist(i, j, cities)
                distance += d_ij * x[k, i] * x[(k+1)%n_city, j]

    A = Placeholder("A")
    H = distance + A * (time_const + city_const)

    # Compile model
    model = H.compile()
    # Generate QUBO
    #Changing this changes the A in the place holder and therefore the affect that the time_const and city const have
    feed_dict = {'A': dimensionality}
    bqm = model.to_bqm(feed_dict=feed_dict)


#This is actaully Running the function
    sampler = LeapHybridSampler()
    sampleset = sampler.sample(bqm, label='TSP Test 2')
    bestsample = sampleset.first
    return bestsample


#Not needed but helps with the debuging 
def plot_cityQuantum(cities, sol=None):
    n_city = len(cities)
    print(f"plot function cities are {cities}")
    cities_dict = dict(cities)
    G = nx.Graph()
    for city in cities_dict:
        G.add_node(city)
        
    # draw path
    if sol:
        city_order = []
        for i in range(n_city):
            for j in range(n_city):
               if sol[0][f'c[{i}][{j}]'] == 1:
                   city_order.append(j)
                
        print(city_order)
        for i in range(n_city):
            city_index1 = city_order[i]
            city_index2 = city_order[(i+1) % n_city]
            G.add_edge(cities[city_index1][0], cities[city_index2][0])
    plt.figure(figsize=(3,3))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, cities_dict)
    plt.axis("off")
    plt.show()
    return plt
  

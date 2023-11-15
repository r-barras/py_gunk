import pandas as pd
from random import random as rnd
import random
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from binding_parameters import molecules, connectors
from settings import max_length

graph = {}
name_graph = {}


def create_element():
    element = len(graph)
    graph[element] = []
    name_element = random.choices(list(molecules.keys()), weights=[molecules[i][0] for i in molecules.keys()], k=1)[0]
    name_graph[element] = name_element


def check_binding_molecules(element):
    bindings = molecules[name_graph[element]][1]
    while len(graph[element]) < len(bindings):
        generate_element = rnd()
        if generate_element < bindings[len(graph[element])]:
            size_graph = len(graph)
            graph[size_graph] = [element]
            graph[element].append(len(graph) - 1)
            name_element = \
            random.choices(list(connectors.keys()), weights=[connectors[i][0] for i in connectors.keys()], k=1)[0]
            name_graph[size_graph] = name_element
        else:
            graph[element].append(np.nan)


def check_binding_connectors(element):
    bindings = connectors[name_graph[element]][1]
    while len(graph[element]) < len(bindings):
        generate_element = rnd()
        if generate_element < bindings[len(graph[element])]:
            size_graph = len(graph)
            graph[size_graph] = [element]
            graph[element].append(len(graph) - 1)
            name_element = \
            random.choices(list(molecules.keys()), weights=[molecules[i][0] for i in molecules.keys()], k=1)[0]
            name_graph[size_graph] = name_element
        else:
            graph[element].append(np.nan)


def fill_binding(element):
    while len(graph[element]) < 4:
        graph[element].append(np.nan)


def correct_name_connectors(element):
    if name_graph[element] in connectors.keys():
        name_graph[element] = list(connectors.keys())[len(graph[element])-1]


def main():
    # Create the first element
    create_element()

    # Create a pointer, initialized at 0
    pointer = 0

    # Iterate through the graph
    prev_len = -1
    while (len(graph) < max_length) & (pointer < len(graph)):
        if len(graph) <= prev_len:
            break
        else:
            if name_graph[pointer] in molecules.keys():
                check_binding_molecules(pointer)
                pointer += 1
            elif name_graph[pointer] in connectors.keys():
                check_binding_connectors(pointer)
                pointer += 1

    # Get different node colors for the molecules and connectors
    node_colors = ['purple' if element in connectors.keys() else 'teal' for key, element in name_graph.items()]

    # Continue to iterate until we reach the end of the length of the graph
    pointer = 0
    while pointer < len(graph):
        # Switch colors of terminators to red if they are terminators
        if len(graph[pointer]) - graph[pointer].count(np.nan) == 1:
            node_colors[pointer] = 'red'
        correct_name_connectors(pointer)
        fill_binding(pointer)
        pointer += 1

    df = pd.DataFrame(graph).T

    G = nx.DiGraph()

    # Add nodes to the graph
    G.add_nodes_from(df.index)

    # Add edges to the graph based on the connections in the DataFrame
    for i in df.index:
        connections = df.iloc[i].dropna().tolist()
        G.add_edges_from((i, c) for c in connections)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=node_colors, edge_color='gray',
            node_size=500)

    # Show the plot
    plt.show()

    # Print also the dictionary of digits:names
    for key, value in name_graph.items():
        print(f'Index {key} is {value}')

    return df


if __name__ == '__main__':
    main()

import pandas as pd
from random import random as rnd
import random
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from binding_parameters import molecules
from settings import max_length

graph = {}
name_graph = {}


def create_element():
    element = len(graph)
    graph[element] = []
    name_element = random.choices(list(molecules.keys()), weights=[molecules[i][0] for i in molecules.keys()], k=1)[0]
    name_graph[element] = name_element


def check_binding(element):
    bindings = molecules[name_graph[element]][1]
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
            graph[element].append('NA')


def fill_binding(element):
    while len(graph[element]) < 4:
        graph[element].append('NA')


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
            check_binding(pointer)
            pointer += 1

    # Continue to iterate until we reach the end of the length of the graph
    pointer = 0
    while pointer < len(graph):
        fill_binding(pointer)
        pointer += 1

    df = pd.DataFrame(graph).T

    df.replace({'NA': np.nan}, inplace=True)

    G = nx.DiGraph()

    # Add nodes to the graph
    G.add_nodes_from(df.index)

    # Add edges to the graph based on the connections in the DataFrame
    for i in df.index:
        connections = df.iloc[i].dropna().tolist()
        G.add_edges_from((i, c) for c in connections)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='teal', edge_color='gray', node_size=500)

    # Show the plot
    plt.show()

    return df


if __name__ == '__main__':
    main()

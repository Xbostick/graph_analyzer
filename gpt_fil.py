import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
import collections
import random
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt

def import_edge_connections(file_name: str) -> dict:
    """
    Given the name of a file containing information about edges in a graph,
    return a dictionary where the keys are the edge numbers and the values are lists
    containing the numbers of the nodes that the edge connects.
    """
    edge_connections = {}
    with open(file_name, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            edge_num = int(parts[0])
            connections = [int(c) for c in parts[1:]]
            edge_connections[edge_num] = connections
    return edge_connections


def import_restrictions(file_name: str) -> List[Tuple[int, int, int]]:
    """
    Given the name of a file containing information about restrictions in a graph,
    return a list of tuples where each tuple contains three integers:
    the numbers of the two edges that are restricted and the distance between them.
    """
    restrictions = []
    with open(file_name, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            edge1 = int(parts[0])
            edge2 = int(parts[1])
            prohibited = int(parts[2])
            restrictions.append((edge1, edge2, prohibited))
    return restrictions



def visualize_graph(edge_connections):
    """
    Given a dictionary containing information about the connections between edges in a graph,
    visualize the graph using networkx and matplotlib.
    """
    G = nx.Graph()
    for edge, connections in edge_connections.items():
        for connection in connections:
            G.add_edge(edge, connection)
    pos = nx.spring_layout(G, seed=42) # Layout nodes using the Fruchterman-Reingold force-directed algorithm
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', node_size=500)
    plt.show()


def check_condition(node1, node2, node3, path):
    if node1 in path and node2 in path and node3 not in path:
        return False
    elif node3 in path:
        return "Done"
    else:
      return True

def dfs(node: int, visited: List[bool], path: List[int], all_paths: List[List[int]], restrictions_local:  List[List[int]], depth: int):
        visited[node-1] = True
        path.append(node)

        sum_locked = 0
        len_start = len(restrictions_local)
        for restrict in restrictions_local:
          check_result =  check_condition(restrict[0], restrict[1], restrict[2], path)
          if not check_result:
            #print(f" decline {restrict[0], restrict[1], restrict[2], path}")
            sum_locked += 1
          elif check_result == "Done":
           # print(f"Done {restrict[0], restrict[1], restrict[2]}")
            #print(len(restrictions_local))
            restrictions_local.remove(restrict)

        if sum_locked:
            all_paths.append(path[:])
            #print(f"solved: {path}")
            path.pop()
            visited[node-1] = False
            return "Error"


        if path[-4:-2] == path[-2:]:
          #print(f'declined path {path}')
          path.pop()
          visited[node-1] = False
          return None

        if all(visited):
            #print(visited)
            all_paths.append(path[:])
            #print(f"solved: {path}")
            path.pop()
            visited[node-1] = False
            return "Done"

        elif depth >= 10 :
            path.pop()
            #print(depth)
            visited[node-1] = False
            return "Max"

        else:
          for neighbor in edge_connections[node]:
                result = dfs(neighbor, visited.copy(), path, all_paths, restrictions_local.copy(),depth+1)

        visited[node-1] = False
        path.pop()

def find_all_paths(edge_connections: dict, restrictions: List[List[int]]) -> List[List[int]]:
    """
    Given a dictionary of edge connections, return a list of all available paths for traversing
    the graph with repetitions, starting and ending at any node, and visiting all nodes.
    """
    all_nodes = list(edge_connections.keys())
    all_paths = []
    for start_node in tqdm(all_nodes):
        #print(f"start {start_node}")
        visited = [False] * len(all_nodes)
        path = []
        dfs(start_node, visited, path, all_paths, restrictions.copy(), 1)

    return all_paths

def clean_list(all_path, final_name):
  finall_results = {}
  final = []
  for path in all_path:
    name = ','.join(str(x) for x in np.unique(path))
    name = str(np.unique(path))
    # print(len(path))
    if name in finall_results.keys():
      if len(path) < len(finall_results[name]):
        finall_results[name] = path
    elif name == final_name:
      final.append(path)
    else:
      finall_results[name] = path
  print(final)
  if final:
    finall_results[final_name] = final
  return finall_results

edge_connections = import_edge_connections('./Links Толкатель.txt')
restrictions = import_restrictions('./Constraints Толкатель.txt')
visualize_graph(edge_connections)

all_paths = find_all_paths(edge_connections, restrictions)
final_name = ','.join(str(x) for x in edge_connections)
clean_paths = clean_list(all_paths,final_name)
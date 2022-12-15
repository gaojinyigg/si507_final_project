import json
import requests
import pprint
import csv
import graph
def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or
    dictionary if provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, "r", encoding=encoding) as file_obj:
        return json.load(file_obj)

def get_node(title, g):
    for n in g.nodes:
        if title == n.information['Title']:
            return n
    return None

def get_information(title, js):
    for i in js:
        if title == i['information']['Title']:
            return i['information']
    return None

def read_graph(filepath):
    js = read_json(filepath)
    G = graph.movieGraph()
    for i in js:
        node = graph.movieNode(i['information'])
        for neigh in i['neighbors']:
            if neigh in [n.information['Title'] for n in G.nodes]:
                temp_node = get_node(neigh, G)
                node.add_neighbors(temp_node)
                temp_node.add_neighbors(node)
            else:
                temp_node = graph.movieNode(get_information(neigh, js))
                node.add_neighbors(temp_node)
                temp_node.add_neighbors(node)
        G.add_node(node)
    return G


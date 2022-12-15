import json
import requests
import pprint
import csv
import webbrowser
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


class movieGraph:
    def __init__(self):
        self.nodes = []
    def add_node(self, node):
        self.nodes.append(node)

class movieNode:
    def __init__(self, information):
        self.information = information
        self.neighbors = []
    def add_neighbors(self, node):
        self.neighbors.append(node)
    def bfs(self, node):
        length = 1
        if(self == node):
            return 0
        queue = []
        seen = set()
        queue.append(self)
        seen.add(self)
        last = self
        next_last = self
        while (len(queue)>0):
            ver = queue.pop(0)
            notes = ver.neighbors
            for i in notes:
                if i not in seen:
                    if(i == node):
                        return length
                    queue.append(i)
                    seen.add(i)
                    next_last = i
            if(last == ver):
                length += 1
                last = next_last
        return -1

def build_graph(select):
    graph = movieGraph()
    movies = read_json('cache_data_detailed.json')
    if select == 1:
        for movie in movies:
            node = movieNode(movie)
            genre = movie['details']['Genre'].split(', ')
            if(movie['details']['Runtime']=='N/A'):
                continue
            for n in graph.nodes:
                temp_genre = n.information['details']['Genre'].split(', ')
                same = False
                for g in genre:
                    if g not in temp_genre:
                        same = True
                        break
                if same == False:
                    node.add_neighbors(n)
                    n.add_neighbors(node)
            graph.add_node(node)
    elif select == 2:
        for movie in movies:
            node = movieNode(movie)
            genre = movie['details']['Genre'].split(', ')
            actors = movie['details']['Actors'].split(', ')
            director = movie['details']['Director']
            for n in graph.nodes:
                temp_genre = n.information['details']['Genre'].split(', ')
                temp_actors = n.information['details']['Actors'].split(', ')
                temp_director = n.information['details']['Director']
                for g in actors:
                    if g in temp_actors or director == temp_director:
                        node.add_neighbors(n)
                        n.add_neighbors(node)
                        break
            graph.add_node(node)
    elif select == 3:
        for movie in movies:
            node = movieNode(movie)
            writers = movie['details']['Writer'].split(', ')
            for n in graph.nodes:
                temp_writers = n.information['details']['Writer'].split(', ')
                for g in writers:
                    if g in temp_writers:
                        node.add_neighbors(n)
                        n.add_neighbors(node)
                        break
            graph.add_node(node)
    else:
        for movie in movies:
            node = movieNode(movie)
            Language = movie['details']['Language'].split(', ')
            for n in graph.nodes:
                temp_Language = n.information['details']['Language'].split(', ')
                for g in Language:
                    if g in temp_Language:
                        node.add_neighbors(n)
                        n.add_neighbors(node)
                        break
            graph.add_node(node)
    return graph
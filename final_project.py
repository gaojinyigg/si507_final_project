import json
import requests
import pprint
import pandas as pd
import csv
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
    
    def bfs(self):
        queue = []
        res = []
        seen = set()
        queue.append(self)
        seen.add(self)
        while (len(queue)>0):
            ver = queue.pop(0)
            notes = ver.neighbors
            for i in notes:
                if i not in seen:
                    queue.append(i)
                    seen.add(i)
            res.append(ver.information['Title'])
        return res

def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    WARN: This function must be implemented using a list comprehension in order to earn points.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        # data = []
        # reader = csv.DictReader(file_obj, delimiter=delimiter)
        # for line in reader:
        #     data.append(line) # OrderedDict() | alternative: data.append(dict(line))
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        return [line for line in reader]

def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or
    dictionary if provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """
    # TODO
    # Uncomment the below lines and correct the mistakes

    with open(filepath, "r", encoding=encoding) as file_obj:
        return json.load(file_obj)

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is;
                            otherwise non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to
                      encoded JSON

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def get_movie_to_cache(filepath):
    movies = read_csv_to_dicts(filepath, 'utf-8')
    res = []
    target = "http://www.omdbapi.com/?apikey=9da705df&s="
    for movie in movies:
        title = movie['title']
        temp = requests.get(target+title).json()
        if 'Error' not in temp.keys():
            # pprint.pprint(temp['Search'][0])
            res.append(temp)
    write_json("cache_data.json", res)

def detail_cache(filepath):
    detailed_cache = []
    with open(filepath, encoding='utf-8') as f:
        movies = json.load(f)
        for movie in movies:
            temp = movie['Search'][0]
            id = temp['imdbID']
            temp['details'] = requests.get("http://www.omdbapi.com/?apikey=9da705df&i="+id).json()
            detailed_cache.append(temp)
    write_json("cache_data_detailed.json", detailed_cache)

def catch_data():
    pass





def main():
    # target = "http://www.omdbapi.com/?apikey=70aa0afa&i="
    # id = 100000
    # for i in range(0, 1000):
    #     result = requests.get(target+str(id)).json()
    #     pprint.pprint(result)
    #     id+=1 
    # movies = read_csv_to_dicts('archive/tmdb_5000_movies.csv')
    # write_json("origin_movies", movies)
    # get_movie_to_cache('archive/tmdb_5000_movies.csv')
    # detail_cache('cache_data.json')
    graph = movieGraph()
    movies = read_json('cache_data_detailed.json')
    for movie in movies:
        node = movieNode(movie)
        genre = movie['details']['Genre'].split(',')
        if(movie['details']['Runtime']=='N/A'):
            continue
        time  = int(movie['details']['Runtime'].split(' ')[0])
        for n in graph.nodes:
            temp_genre = node.information['details']['Genre'].split(',')
            temp_time  = int(n.information['details']['Runtime'].split(' ')[0])
            if abs(temp_time- time)<5:
                node.add_neighbors(n)
                n.add_neighbors(node)
            # for g in genre:
            #     if g in temp_genre:
            #         node.add_neighbors(n)
            #         n.add_neighbors(node)
            #         break
        graph.add_node(node)
    print("123")
    Node = graph.nodes[0]
    # # pprint.pprint(Node.informsation)
    pprint.pprint(len(Node.bfs()))
    # for n in graph.nodes:
    #     pprint.pprint(len(n.neighbors))
if  __name__ == "__main__":
    main()
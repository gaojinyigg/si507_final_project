import json
import requests
import pprint
import csv
import webbrowser
import read_graph
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


def get_music_data(user):
    target = "https://itunes.apple.com/search?term="+user+"&limit=1"
    data = requests.get(target).json()["results"]
    return data


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


def find_connected_node(graph, most):
    res = None
    if most:
        num = 0
        for n in graph.nodes:
            if len(n.neighbors) > num:
                res = n
                num = len(n.neighbors)
        print(len(res.neighbors))
        print(res.information['Title'])
        return res
    else:
        num = 5000
        for n in graph.nodes:
            if len(n.neighbors) < num:
                res = n
                num = len(n.neighbors)
        print(len(res.neighbors))    
        print(res.information['Title'])
        return res

def check_songs(title):
    target = "https://itunes.apple.com/search?term="+title+"&limit=5"
    data = requests.get(target).json()["results"][0]
    return data

def find_highest_movie(graph):
    res = []
    for n in graph.nodes:
        if n.information['details']['imdbRating']!='N/A' and  float(n.information['details']['imdbRating']) > 9:
            res.append(n)
    return res

def main():
    # target = "http://www.omdbapi.com/?apikey=70aa0afa&i="
    # movies = read_csv_to_dicts('archive/tmdb_5000_movies.csv')
    # write_json("origin_movies", movies)
    # get_movie_to_cache('archive/tmdb_5000_movies.csv')
    # detail_cache('cache_data.json')
    """coding above are used to save the data to the cache"""
    start = input("welcome to movie data set with top 5000 movies!\nselect what you want!\n0.exit\n1.build a graph based on the genre\n2.build a graph based on the characters\n3.build a graph based on the writer\n4.build a graph based on the language\n")
    while(start!="0"):
        if(start == "1"):
            graph = build_graph(1)
            # graph =read_graph.read_graph("graph.json")
            dic = []
            for node in graph.nodes:
                dic.append({"information": node.information, "neighbors": [i.information['Title'] for i in node.neighbors]})
            write_json("graph.json", dic)
            print("a graph based on the genre has been built")
            start = input("Now you can check the relationship among movies\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
            while(start!="0"):
                if(start ==   "1"):
                    node = find_connected_node(graph,True)
                    print("the most connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "2"):
                    node = find_connected_node(graph,False)
                    print("the most non-connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    else:
                        print("wrong input")
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "3"):
                    res = find_highest_movie(graph)
                    title = [i.information['Title'] for i in res]
                    pprint.pprint(title)
                    can1 = int(input("please enter the first movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    can2 = int(input("please enter the second movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    lenth = res[can1-1].bfs(res[can2-1])
                    print(f"the connectivity between two movies is {lenth}(need {lenth} steps to find the movie)")
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                else:
                    start = input("try one more time please\n")
        elif(start == "2"):
            graph = build_graph(2)
            print("a graph based on the characters has been built")
            start = input("Now you can check the relationship among movies\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
            while(start!="0"):
                if(start ==   "1"):
                    node = find_connected_node(graph,True)
                    print("the most connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "2"):
                    node = find_connected_node(graph,False)
                    print("the most non-connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "3"):
                    res = find_highest_movie(graph)
                    res.append(res[0].neighbors[0])
                    title = [i.information['Title'] for i in res]
                    pprint.pprint(title)
                    can1 = int(input("please enter the first movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    can2 = int(input("please enter the second movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    lenth = res[can1-1].bfs(res[can2-1])
                    print(f"the connectivity between two movies is {lenth}(need {lenth} steps to find the movie)")
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                else:
                    start = input("try one more time please\n")
        elif start == "3":
            graph = build_graph(3)
            print("a graph based on the writers has been built")
            start = input("Now you can check the relationship among movies\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
            while(start!="0"):
                if(start ==   "1"):
                    node = find_connected_node(graph,True)
                    print("the most connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "2"):
                    node = find_connected_node(graph,False)
                    print("the most non-connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "3"):
                    res = find_highest_movie(graph)
                    title = [i.information['Title'] for i in res]
                    pprint.pprint(title)
                    can1 = int(input("please enter the first movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    can2 = int(input("please enter the second movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    lenth = res[can1-1].bfs(res[can2-1])
                    print(f"the connectivity between two movies is {lenth}(need {lenth} steps to find the movie)")
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                else:
                    start = input("try one more time please\n")
        elif start == "4":
            graph = build_graph(4)
            print("a graph based on the languages has been built")
            start = input("Now you can check the relationship among movies\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
            while(start!="0"):
                if(start ==   "1"):
                    node = find_connected_node(graph,True)
                    print("the most connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "2"):
                    node = find_connected_node(graph,False)
                    print("the most non-connected movie is as follow:\n")
                    pprint.pprint(node.information)
                    choice = input("More options provided!\n0.exit\n1.check the poster\n2.check the link for watching the movie")
                    if(choice == "1"):
                        webbrowser.open_new(node.information['Poster'])
                    elif(choice == "2"):
                        data = check_songs(node.information['Title'])
                        webbrowser.open_new(data['collectionViewUrl'])
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                elif(start == "3"):
                    res = find_highest_movie(graph)
                    title = [i.information['Title'] for i in res]
                    pprint.pprint(title)
                    can1 = int(input("please enter the first movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    can2 = int(input("please enter the second movie you want to check connectivity(using index e.g. 1 represents the first movie)\n"))
                    lenth = res[can1-1].bfs(res[can2-1])
                    print(f"the connectivity between two movies is {lenth}(need {lenth} steps to find the movie)")
                    start = input("Do you want to try one more time?\n0.exit\n1.most connected movie\n2.most non_connected movie\n3.check connectivity between two movies from a set\n")
                else:
                    start = input("try one more time please\n")
        else:
            start = input("please enter one more time\n")
    print("Bye!\n")
if  __name__ == "__main__":
    main()
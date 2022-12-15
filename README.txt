API for movie dataset used in this project is "http://www.omdbapi.com/?apikey=9da705df".

If you want search the title url will be  "http://www.omdbapi.com/?apikey=9da705df&s=xx".

If you want seach the id url will be "http://www.omdbapi.com/?apikey=9da705df&i=xx".

For itunes the api used is "https://itunes.apple.com/search?term=xxx&limit=xxx".

Instructions for the interaction:

At the beginning, there will be four options for you build two different kinds of graph based on different connection. (genre, character, writer, language)

You must type "0", "1", "2", "3", "4" to continue

Then there will be three options. "1" is to check the most connected movie (the movie with most neighbors in the graph) and "2" is to check the most non-connected movie. In addtion, "3" is to check the connectivity between two movies.

If you choose "1" and "2", the basic information will be shown by the command line and you can also choose to look at the poster of the movie("1") or to watch the movie on itunes directly("2").  If you choose to watch, the webbrowser will open the corresponding link and show you the results.

If you choose "3", the system will provide you with a movie data set and you can choose two of them to check the connectivity (how many steps needed to find another movie ).

Once you finished one of these three options, you can try one more time.

For every step, "0" is for exit the whole system.

For different kinds of graphs, the system will show different results.
import xbmc
from xbmcaddon import Addon
from xbmcgui import Dialog
import requests
from bs4 import BeautifulSoup


class Addon(Addon):

    def __init__(self):
        super().__init__()

        self.addon_id = "script.myaddon"
        self.addon_name = "My Addon"
        self.addon_version = "1.0"
        self.watchlist = []

    def on_init(self):
        # Load the resources.
        self.resources = {}
        self.resources["movies"] = self.get_movies()

    def on_demand(self):
        # Get the user's input.
        action = Dialog.select("Select an action", ["Movies", "TV Shows", "Genres", "Top Rated", "Trending", "New Releases", "Search", "Watchlist", "Exit"])

        if action == 0:
            self.show_movies()
        elif action == 1:
            self.show_tv_shows()
        elif action == 2:
            self.show_genres()
        elif action == 3:
            self.show_top_rated()
        elif action == 4:
            self.show_trending()
        elif action == 5:
            self.show_new_releases()
        elif action == 6:
            self.search()
        elif action == 7:
            self.show_watchlist()
        elif action == 8:
            return

    def show_movies(self):
        # Display the list of movies.
        movies = self.resources["movies"]
        titles = [movie["title"] for movie in movies]
        selection = Dialog.select("Select a movie", titles)
        if selection != -1:
            self.play_movie(movies[selection])

    def show_tv_shows(self):
        # Display the list of TV shows.
        pass

    def show_genres(self):
        # Display the list of genres.
        pass

    def show_top_rated(self):
        # Display the list of top rated movies.
        pass

    def show_trending(self):
        # Display the list of trending movies.
        pass

    def show_new_releases(self):
        # Display the list of new releases.
        pass

    def search(self):
        # Search for movies or TV shows.
        query = Dialog.input("Enter search query:")
        if query:
            results = self.search_movies(query)
            titles = [result["title"] for result in results]
            selection = Dialog.select("Search results", titles)
            if selection != -1:
                self.play_movie(results[selection])

    def show_watchlist(self):
        # Display the watchlist.
        titles = [item["title"] for item in self.watchlist]
        selection = Dialog.select("Watchlist", titles)
        if selection != -1:
            self.play_movie(self.watchlist[selection])

    def play_movie(self, movie):
        # Play the selected movie.
        xbmc.play_video(movie["link"])

    def add_to_watchlist(self, movie):
        # Add a movie to the watchlist.
        self.watchlist.append(movie)

    def get_movies(self):
        # Get the list of movies from the website.
        response = requests.get("https://ww4.123moviesfree.net/")
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of movies.
        movies = []
        for movie in movie_list.children:
            title = movie.find("a").text
            year = movie.find("span", class_="year").text
            genre = movie.find("span", class_="genre").text
            link = movie.find("a")["href"]
            movies.append({
                "title": title,
                "year": year,
                "genre": genre,
                "link": link
            })

        return movies

    def search_movies(self, query):
        # Search for movies on the website.
        response = requests.get(f"https://ww4.123moviesfree.net/search/{query}")
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of search results.
        results = []
        for movie in movie_list.children:
            title = movie.find("a").text
            year = movie.find("span", class_="year").text
            genre = movie.find("span", class_="genre").text
            link = movie.find("a")["href"]
            results.append({
                "title": title,
                "year": year,
                "genre": genre,
                "link": link
            })

        return results

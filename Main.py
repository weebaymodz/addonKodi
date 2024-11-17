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
        self.resources["trending"] = self.get_trending_movies()
        self.resources["top_rated"] = self.get_top_rated_movies()
        self.resources["genres"] = self.get_genre_based_movies()
        self.resources["year_based"] = self.get_year_based_movies()

    def on_demand(self):
        # Get the user's input.
        action = Dialog.select("Select an action", ["Trending Movies/TV Shows", "Top Rated/Most Watched", "Genres", "Year-based Lists", "Search", "Watchlist", "Exit"])

        if action == 0:
            self.show_trending()
        elif action == 1:
            self.show_top_rated()
        elif action == 2:
            self.show_genres()
        elif action == 3:
            self.show_year_based()
        elif action == 4:
            self.search()
        elif action == 5:
            self.show_watchlist()
        elif action == 6:
            return

    def show_trending(self):
        # Display the list of trending movies.
        movies = self.resources["trending"]
        titles = [movie["title"] for movie in movies]
        selection = Dialog.select("Select a movie", titles)
        if selection != -1:
            self.show_movie_sources(movies[selection])

    def show_top_rated(self):
        # Display the list of top rated movies.
        movies = self.resources["top_rated"]
        titles = [movie["title"] for movie in movies]
        selection = Dialog.select("Select a movie", titles)
        if selection != -1:
            self.show_movie_sources(movies[selection])

    def show_genres(self):
        # Display the list of genres.
        genres = list(self.resources["genres"].keys())
        selection = Dialog.select("Select a genre", genres)
        if selection != -1:
            genre = genres[selection]
            self.show_genre_movies(genre)

    def show_genre_movies(self, genre):
        # Display the list of movies for a specific genre.
        movies = self.resources["genres"][genre]
        titles = [movie["title"] for movie in movies]
        selection = Dialog.select("Select a movie", titles)
        if selection != -1:
            self.show_movie_sources(movies[selection])

    def show_year_based(self):
        # Display the list of years.
        years = list(self.resources["year_based"].keys())
        selection = Dialog.select("Select a year", years)
        if selection != -1:
            year = years[selection]
            self.show_year_movies(year)

    def show_year_movies(self, year):
        # Display the list of movies for a specific year.
        movies = self.resources["year_based"][year]
        titles = [movie["title"] for movie in movies]
        selection = Dialog.select("Select a movie", titles)
        if selection != -1:
            self.show_movie_sources(movies[selection])

    def search(self):
        # Search for movies or TV shows.
        query = Dialog.input("Enter search query:")
        if query:
            results = self.search_movies(query)
            titles = [result["title"] for result in results]
            selection = Dialog.select("Search results", titles)
            if selection != -1:
                self.show_movie_sources(results[selection])

    def show_watchlist(self):
        # Display the watchlist.
        titles = [item["title"] for item in self.watchlist]
        selection = Dialog.select("Watchlist", titles)
        if selection != -1:
            self.show_movie_sources(self.watchlist[selection])

    def show_movie_sources(self, movie):
        # Display the list of available sources for the selected movie.
        sources = self.get_movie_sources(movie["link"])
        titles = [source["quality"] for source in sources]
        selection = Dialog.select("Select a source", titles)
        if selection != -1:
            self.play_movie(sources[selection])

    def play_movie(self, source):
        # Play the selected movie source.
        xbmc.play_video(source["link"])

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
                "link": link,
                "sources": self.get_movie_sources(link)
            })

        return movies

    def get_movie_sources(self, movie_link):
        # Get the list of available sources for a specific movie from the website.
        response = requests.get(movie_link)
        soup = BeautifulSoup(response.content, "html.parser")
        source_list = soup.find("ul", class_="source-list")

        # Create a list of sources.
        sources = []
        for source in source_list.children:
            quality = source.find("span", class_="quality").text
            link = source.find("a")["href"]
            sources.append({
                "quality": quality,
                "link": link
            })

        return sources

    def get_trending_movies(self):
        # Get the list of trending movies from the website.
        response = requests.get("https://ww4.123moviesfree.net/trending")
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of trending movies.
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
                "link": link,
                "sources": self.get_movie_sources(link)
            })

        return movies

    def get_top_rated_movies(self):
        # Get the list of top rated movies from the website.
        response = requests.get("https://ww4.123moviesfree.net/top-rated")
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of top rated movies.
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
                "link": link,
                "sources": self.get_movie_sources(link)
            })

        return movies

    def get_genre_based_movies(self):
        # Get the list of movies by genre from the website.
        response = requests.get("https://ww4.123moviesfree.net/genres")
        soup = BeautifulSoup(response.content, "html.parser")
        genre_list = soup.find("ul", class_="genre-list")

        # Create a dictionary of movies by genre.
        genres = {}
        for genre in genre_list.children:
            genre_name = genre.find("a").text
            genre_link = genre.find("a")["href"]
            genre_movies = self.get_movies_by_genre(genre_link)
            genres[genre_name] = genre_movies

        return genres

    def get_movies_by_genre(self, genre_link):
        # Get the list of movies for a specific genre from the website.
        response = requests.get(genre_link)
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of movies for the genre.
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
                "link": link,
                "sources": self.get_movie_sources(link)
            })

        return movies

    def get_year_based_movies(self):
        # Get the list of movies by year from the website.
        response = requests.get("https://ww4.123moviesfree.net/years")
        soup = BeautifulSoup(response.content, "html.parser")
        year_list = soup.find("ul", class_="year-list")

        # Create a dictionary of movies by year.
        years = {}
        for year in year_list.children:
            year_name = year.find("a").text
            year_link = year.find("a")["href"]
            year_movies = self.get_movies_by_year(year_link)
            years[year_name] = year_movies

        return years

    def get_movies_by_year(self, year_link):
        # Get the list of movies for a specific year from the website.
        response = requests.get(year_link)
        soup = BeautifulSoup(response.content, "html.parser")
        movie_list = soup.find("ul", class_="movie-list")

        # Create a list of movies for the year.
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
                "link": link,
                "sources": self.get_movie_sources(link)
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
                "link": link,
                "sources": self.get_movie_sources(link)
            })

        return results

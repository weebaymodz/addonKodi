import xbmc
from xbmcaddon import Addon
from xbmcgui import Dialog


class Addon(Addon):

    def __init__(self):
        super().__init__()

        self.addon_id = "script.myaddon"
        self.addon_name = "My Addon"
        self.addon_version = "1.0"

    def on_init(self):
        # Load the resources.
        self.resources = {}
        self.resources["movies"] = self.get_movies()

    def on_demand(self):
        # Get the user's input.
        action = Dialog.select("Select an action", ["Play a movie", "Exit"])

        # If the user selected "Play a movie", play the movie.
        if action == 0:
            title = Dialog.input("Enter the title of the movie:")
            if title:
                movie = self.resources["movies"].get(title)
                if movie:
                    xbmc.play_video(movie["link"])

    def get_movies(self):
        # Get the list of movies from the website.
        response = requests.get("https://ww4.solarmovie.to/")
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

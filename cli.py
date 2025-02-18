import cmd
import requests
import json
from typing import Optional, List, Dict, Any

class MovieCLI(cmd.Cmd):
    """Simple CLI for searching movies and actors."""
    
    intro = """
Welcome to the Movie Information Service!

Commands:
  search <title>     - Search for movies by title
  actor <name>       - Search for an actor's filmography
  help               - Show this help message
  quit               - Exit the program

Example:
  search Inception
  actor Tom Hanks
"""
    prompt = 'movies> '

    def do_search(self, title: str) -> None:
        """Search for movies by title."""
        if not title:
            print("Please provide a movie title to search for.")
            return

        try:
            response = requests.get(
                "http://localhost:5000/api/v1/movies/search",
                params={"q": title},
                headers={"Accept": "application/json"}
            )

            if response.status_code == 200:
                movies = response.json()
                for movie in movies:
                    print(f"\nTitle: {movie['title']} ({movie['year']})")
                    print(f"Rating: {movie['rating']}")
                    print(f"Genre: {', '.join(movie['genre'])}")
                    print(f"Released: {movie['released']}")
                    print("\nCast:")
                    for actor in movie['cast']:
                        print(f"- {actor}")
                    print("\nCrew:")
                    for crew_member in movie['crew']:
                        print(f"- {crew_member}")
            else:
                error = response.json().get('error', {})
                print(f"\nError: {error.get('message', 'Unknown error')}")
                if 'details' in error:
                    print(f"Details: {error['details']}")

        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to service: {e}")
            print("Please make sure the service is running (python service.py)")

    def do_actor(self, name: str) -> None:
        """Search for an actor's filmography."""
        if not name:
            print("Please provide an actor's name to search for.")
            return

        try:
            response = requests.get(
                "http://localhost:5000/api/v1/movies/search",
                params={"q": name, "type": "actor"},
                headers={"Accept": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"\nFilmography for {data['actor']}:")
                for movie in data['filmography']:
                    print(f"- {movie['title']} ({movie['year']})")
            else:
                error = response.json().get('error', {})
                print(f"\nError: {error.get('message', 'Unknown error')}")
                if 'details' in error:
                    print(f"Details: {error['details']}")

        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to service: {e}")
            print("Please make sure the service is running (python service.py)")

    def do_help(self, arg: str) -> None:
        """Show help message."""
        print(self.intro)

    def do_quit(self, arg: str) -> bool:
        """Exit the program."""
        print("\nGoodbye!")
        return True

    def do_exit(self, arg: str) -> bool:
        """Exit the program."""
        return self.do_quit(arg)

    def default(self, line: str) -> None:
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of commands.")

    def emptyline(self) -> bool:
        """Do nothing on empty line."""
        return False

if __name__ == '__main__':
    try:
        # Check if service is running
        requests.get("http://localhost:5000/health")
        MovieCLI().cmdloop()
    except requests.exceptions.ConnectionError:
        print("\nError: Movie service is not running!")
        print("Please start the service in another terminal with: python service.py")

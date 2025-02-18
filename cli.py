import cmd
import json
import requests
from datetime import datetime

class MovieCLI(cmd.Cmd):
    """Command-line interface for the Movie Information Service."""
    
    def show_commands(self):
        """Show available commands."""
        print("\nAvailable Commands:")
        print("  details <movie_id>  - Get details for a specific movie (e.g., details tt0468569)")
        print("  search <title>      - Search for movies by title (e.g., search Batman)")
        print("  health             - Check if the service is running")
        print("  help               - Show this help message")
        print("  quit/exit          - Exit the CLI")
    
    intro = """
Welcome to the Movie Information Service CLI!
This service provides movie information including details, cast, and release dates.
"""
    prompt = 'movies> '
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:5000/api/v1"
        self.show_commands()
    
    def do_details(self, movie_id):
        """Get details for a specific movie by ID.
        Usage: details tt0468569"""
        if not movie_id:
            print("Please provide a movie ID")
            self.show_commands()
            return
            
        try:
            response = requests.get(
                f"{self.base_url}/movies/{movie_id}",
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                movie = response.json()
                print("\nMovie Details:")
                print(f"Title: {movie['title']}")
                print(f"Year: {movie['year']}")
                print(f"Runtime: {movie['runtime']} minutes")
                print(f"Rating: {movie['rating']}")
                print("\nCast:")
                for actor in movie['cast']:
                    print(f"- {actor['name']} as {actor['role']}")
                print("\nRelease Dates:")
                for region, date in movie['release_dates'].items():
                    print(f"- {region}: {date}")
                self.show_commands()
            else:
                error = response.json()['error']
                print(f"\nError: {error['message']}")
                self.show_commands()
                
        except requests.exceptions.RequestException as e:
            print(f"\nError: Could not connect to service. Is it running?")
            print(f"Details: {str(e)}")
            self.show_commands()
    
    def do_search(self, title):
        """Search for movies by title.
        Usage: search Batman"""
        if not title:
            print("Please provide a search term")
            self.show_commands()
            return
            
        try:
            response = requests.get(
                f"{self.base_url}/movies/search",
                params={"title": title},
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                movies = response.json()
                if movies:
                    print("\nSearch Results:")
                    for movie in movies:
                        print(f"\nID: {movie['id']}")
                        print(f"Title: {movie['title']}")
                        print(f"Year: {movie['year']}")
                        print(f"Rating: {movie['rating']}")
                    self.show_commands()
                else:
                    print("\nNo movies found matching your search.")
                    self.show_commands()
            else:
                error = response.json()['error']
                print(f"\nError: {error['message']}")
                self.show_commands()
                
        except requests.exceptions.RequestException as e:
            print(f"\nError: Could not connect to service. Is it running?")
            print(f"Details: {str(e)}")
            self.show_commands()
    
    def do_health(self, arg):
        """Check if the service is running.
        Usage: health"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("\nService is healthy ✓")
            else:
                print("\nService health check failed!")
            self.show_commands()
        except requests.exceptions.RequestException:
            print("\nError: Could not connect to service. Is it running?")
            self.show_commands()
    
    def do_help(self, arg):
        """Show help message."""
        self.show_commands()
    
    def do_quit(self, arg):
        """Exit the CLI."""
        print("\nGoodbye!")
        return True
        
    def do_exit(self, arg):
        """Exit the CLI."""
        return self.do_quit(arg)

if __name__ == '__main__':
    MovieCLI().cmdloop()

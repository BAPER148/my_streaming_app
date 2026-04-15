import flet as ft
import requests
import threading

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.padding = 20
    
    # A simple search bar to find any movie
    search_field = ft.TextField(
        label="Search Movie or TV Show",
        border_color="red",
        expand=True
    )
    
    results_grid = ft.GridView(expand=1, runs_count=2, spacing=10)

    def search_movie(e):
        results_grid.controls.clear()
        query = search_field.value.replace(" ", "+")
        
        # We'll use an open movie database API to get posters/info
        # This is way more stable than scraping HDHub
        try:
            # Using a public search endpoint
            api_url = f"https://www.omdbapi.com/?s={query}&apikey=979435b0"
            res = requests.get(api_url).json()
            
            if res.get("Search"):
                for movie in res["Search"]:
                    imdb_id = movie["imdbID"]
                    # This is the "Magic Link" that aggregators use
                    stream_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
                    
                    results_grid.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=movie["Poster"], border_radius=10, height=220),
                                ft.Text(movie["Title"], size=12, weight="bold", no_wrap=True)
                            ]),
                            on_click=lambda e, url=stream_url: page.launch_url(url),
                            bgcolor="#1a1a1a",
                            padding=5,
                            border_radius=10
                        )
                    )
            else:
                results_grid.controls.append(ft.Text("No results found."))
        except:
            results_grid.controls.append(ft.Text("Connection error."))
        
        page.update()

    page.add(
        ft.Text("PIKACLONE PRO", size=32, weight="bold", color="red"),
        ft.Row([search_field, ft.IconButton(ft.Icons.SEARCH, on_click=search_movie)]),
        results_grid
    )

ft.app(target=main)

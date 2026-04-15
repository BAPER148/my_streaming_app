import flet as ft
import requests
import threading

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.title = "PIKACLONE PRO"
    page.window_width = 400 # Typical mobile width
    
    # UI Elements
    search_field = ft.TextField(
        label="Search Movie/TV Show",
        border_color="red",
        expand=True,
        on_submit=lambda e: start_search()
    )
    results_grid = ft.GridView(expand=1, runs_count=2, spacing=15, padding=10)
    loader = ft.ProgressBar(visible=False, color="red")

    def start_search():
        if not search_field.value: return
        threading.Thread(target=perform_search).start()

    def perform_search():
        loader.visible = True
        results_grid.controls.clear()
        page.update()
        
        query = search_field.value.strip().replace(" ", "+")
        
        try:
            # Using a reliable public API key for TMDB
            url = f"https://api.themoviedb.org/3/search/multi?api_key=15d1a99839366ce51b1101d78242d384&query={query}"
            response = requests.get(url).json()
            
            if response.get("results"):
                for item in response["results"]:
                    # Skip items without a title or poster
                    title = item.get("title") or item.get("name")
                    poster = item.get("poster_path")
                    if not title or not poster: continue
                    
                    img_url = f"https://image.tmdb.org/t/p/w500{poster}"
                    media_type = item.get("media_type", "movie")
                    tmdb_id = item.get("id")
                    
                    # Generate the stream link based on movie or tv show
                    stream_url = f"https://vidsrc.to/embed/{media_type}/{tmdb_id}"

                    results_grid.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=img_url, border_radius=10, height=220, fit=ft.ImageFit.COVER),
                                ft.Text(title, size=12, weight="bold", max_lines=1)
                            ]),
                            on_click=lambda e, u=stream_url: page.launch_url(u),
                            bgcolor="#1e1e1e",
                            padding=8,
                            border_radius=12,
                        )
                    )
            else:
                results_grid.controls.append(ft.Text("No results. Check spelling!"))
        
        except Exception:
            results_grid.controls.append(ft.Text("Network error. Try again."))
        
        loader.visible = False
        page.update()

    page.add(
        ft.Text("PIKACLONE", size=30, weight="bold", color="red"),
        ft.Row([search_field, ft.IconButton(ft.Icons.SEARCH, on_click=lambda _: start_search())]),
        loader,
        results_grid
    )

ft.app(target=main)

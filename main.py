import flet as ft
import requests
from bs4 import BeautifulSoup
import threading

HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212" # Solid background to avoid "pitch black" look
    
    movie_grid = ft.GridView(expand=1, runs_count=3, max_extent=150, spacing=10)
    loader = ft.ProgressBar(width=400, color="blue", visible=False)
    
    def scrape_site(url, name):
        loader.visible = True
        movie_grid.controls.clear()
        page.update()
        
        try:
            # We added a 15-second timeout in case the school/local network is slow
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                movie_grid.controls.append(ft.Text(f"Site blocked us (Error {res.status_code})"))
            else:
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.find_all(['article', 'div'], class_=['post-column', 'item', 'blog-post'])
                
                if not items:
                    movie_grid.controls.append(ft.Text("No movies found. Try another category."))
                
                for item in items[:12]:
                    img = item.find('img')
                    title = item.find(['h2', 'h3'])
                    if img and title:
                        img_url = img.get('src') or img.get('data-src')
                        movie_grid.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Image(src=img_url, border_radius=10, height=180, fit=ft.ImageFit.COVER),
                                    ft.Text(title.get_text()[:20], size=10)
                                ]),
                                bgcolor="#1e1e1e",
                                padding=5,
                                border_radius=10
                            )
                        )
        except Exception as e:
            movie_grid.controls.append(ft.Text(f"Connection Error: {str(e)[:20]}"))
        
        loader.visible = False
        page.update()

    page.add(
        ft.AppBar(title=ft.Text("PIKACLONE V2.1"), bgcolor="#1f1f1f"),
        loader,
        ft.Row([
            ft.TextButton("Hollywood", on_click=lambda _: threading.Thread(target=scrape_site, args=("https://vegamovies.wedding/", "Hollywood")).start()),
            ft.TextButton("NetMirror", on_click=lambda _: threading.Thread(target=scrape_site, args=("https://netmirror.world/", "NetMirror")).start()),
        ], scroll=ft.ScrollMode.ALWAYS),
        movie_grid
    )

ft.app(target=main)

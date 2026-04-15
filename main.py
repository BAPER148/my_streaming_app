import flet as ft
import requests
from bs4 import BeautifulSoup
import threading

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Referer": "https://new6.hdhub4u.fo/"
}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f0f0f"
    page.title = "PikaClone Pro"
    
    movie_grid = ft.GridView(expand=1, runs_count=2, max_extent=200, spacing=12, padding=10)
    progress_bar = ft.ProgressBar(width=400, color="yellow", visible=False)

    def scrape_hdhub(url):
        progress_bar.visible = True
        movie_grid.controls.clear()
        page.update()
        
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # HDHub4u usually wraps movies in 'figure' or 'div' with specific classes
            posts = soup.find_all(['article', 'div'], class_=['post-column', 'img-box', 'movie-post'])
            
            if not posts:
                # Fallback: Just look for any link that has an image and a title-like class
                posts = soup.find_all('a', class_='ml-mask')

            for post in posts[:20]:
                img_tag = post.find('img')
                # HDHub4u specific: check 'data-src', 'data-lazy-src', or 'src'
                img_url = img_tag.get('data-src') or img_tag.get('data-lazy-src') or img_tag.get('src')
                title = img_tag.get('alt') or "Untitled Movie"
                link = post.get('href') if post.name == 'a' else post.find('a').get('href')

                if img_url:
                    movie_grid.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=img_url, border_radius=12, height=220, fit=ft.ImageFit.COVER),
                                ft.Text(title[:30], size=12, weight="bold", overflow=ft.TextOverflow.ELLIPSIS)
                            ]),
                            on_click=lambda e, l=link: print(f"Opening: {l}"),
                            padding=5,
                            bgcolor="#1e1e1e",
                            border_radius=15,
                        )
                    )
            
            if not movie_grid.controls:
                movie_grid.controls.append(ft.Text("Empty-handed! The site might be blocking us.", color="red"))

        except Exception as e:
            movie_grid.controls.append(ft.Text(f"Connection timed out. Try again!"))
        
        progress_bar.visible = False
        page.update()

    page.add(
        ft.Text("HDHub4u Explorer", size=28, weight="bold", color="yellow"),
        progress_bar,
        ft.ElevatedButton("Load Latest Movies", 
            on_click=lambda _: threading.Thread(target=scrape_hdhub, args=("https://new6.hdhub4u.fo/",)).start(),
            bgcolor="yellow", color="black"
        ),
        movie_grid
    )

ft.app(target=main)

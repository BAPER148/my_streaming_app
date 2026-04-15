import flet as ft
import requests
from bs4 import BeautifulSoup
import threading

# We create a session to keep cookies, which makes us look more "human"
session = requests.Session()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    movie_grid = ft.GridView(expand=1, runs_count=2, max_extent=200, spacing=10)
    
    def stealth_scrape(url):
        movie_grid.controls.clear()
        movie_grid.controls.append(ft.Text("Bypassing security...", color="blue"))
        page.update()
        
        try:
            # First, we 'visit' the home page to get cookies
            session.get("https://new6.hdhub4u.fo/", headers=HEADERS, timeout=10)
            
            # Now we try to get the actual content
            res = session.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Look for ANY link that contains an image - very broad!
            links = soup.find_all('a')
            found = False
            
            for l in links:
                img = l.find('img')
                if img and l.get('href') and 'movie' in l.get('href'):
                    found = True
                    img_url = img.get('data-src') or img.get('src')
                    movie_grid.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=img_url, height=200, fit=ft.ImageFit.COVER),
                                ft.Text(img.get('alt', 'Movie')[:20], size=10)
                            ]),
                            on_click=lambda e, link=l.get('href'): print(f"Link: {link}")
                        )
                    )
            
            if not found:
                movie_grid.controls.clear()
                movie_grid.controls.append(ft.Text("Still blocked. Switching to backup source...", color="yellow"))
                # If HDHub4u fails, we could auto-trigger a NetMirror search here
        
        except Exception as e:
            movie_grid.controls.append(ft.Text("Connection reset. Check your Wi-Fi!"))
        
        page.update()

    page.add(
        ft.AppBar(title=ft.Text("PIKACLONE STEALTH"), bgcolor="#111111"),
        ft.ElevatedButton("Force Load HDHub", on_click=lambda _: threading.Thread(target=stealth_scrape, args=("https://new6.hdhub4u.fo/",)).start()),
        movie_grid
    )

ft.app(target=main)

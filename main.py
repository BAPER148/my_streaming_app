import flet as ft
import requests
from bs4 import BeautifulSoup
import threading

# Header to trick sites into thinking we are a mobile phone
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"
}

def main(page: ft.Page):
    page.title = "PikaClone"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    
    movie_grid = ft.GridView(
        expand=1,
        runs_count=3,
        max_extent=150,
        child_aspect_ratio=0.6,
        spacing=10,
    )

    # Status text to show loading progress
    status_text = ft.Text("Select a category to start", color="grey")

    def scrape_site(url, category_name):
        movie_grid.controls.clear()
        status_text.value = f"Scraping {category_name}..."
        page.update()
        
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # This logic targets common patterns in Vegamovies/MkvCinemas
            # It looks for 'article' tags or 'div' with movie classes
            items = soup.find_all(['article', 'div'], class_=['post-column', 'blog-post', 'item'])
            
            for item in items[:15]: # Limit to 15 items for speed
                title_tag = item.find(['h2', 'h3'])
                img_tag = item.find('img')
                link_tag = item.find('a')
                
                if title_tag and img_tag:
                    title = title_tag.get_text(strip=True)[:30] + "..."
                    img_url = img_tag.get('src') or img_tag.get('data-src')
                    video_url = link_tag.get('href') if link_tag else "#"
                    
                    movie_grid.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=img_url, border_radius=10, fit=ft.ImageFit.COVER),
                                ft.Text(title, size=11, weight="bold", max_lines=2)
                            ]),
                            on_click=lambda e, u=video_url: print(f"Link: {u}")
                        )
                    )
            
            status_text.value = f"Loaded {category_name} successfully!"
        except Exception as e:
            status_text.value = f"Error: {str(e)[:30]}"
        
        page.update()

    # Category buttons
    categories = ft.Row(
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.ElevatedButton("Hollywood", on_click=lambda _: threading.Thread(target=scrape_site, args=("https://vegamovies.wedding/category/hollywood-movies/", "Hollywood")).start()),
            ft.ElevatedButton("Bollywood", on_click=lambda _: threading.Thread(target=scrape_site, args=("https://mkvcinemas.ph/category/bollywood-movies/", "Bollywood")).start()),
            ft.ElevatedButton("NetMirror", on_click=lambda _: threading.Thread(target=scrape_site, args=("https://netmirror.world/", "NetMirror")).start()),
            ft.ElevatedButton("Sports/MMA", on_click=lambda _: print("MMA logic coming soon!")),
        ]
    )

    page.add(
        ft.AppBar(title=ft.Text("PIKACLONE v2"), center_title=True, bgcolor=ft.Colors.SURFACE_VARIANT),
        categories,
        status_text,
        movie_grid
    )

ft.app(target=main)

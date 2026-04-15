import flet as ft
import time
import threading

# This function runs in the background without freezing the UI
def background_tasks():
    while True:
        print("Background service is active...")
        # Put your scraper or local server logic here
        time.sleep(10)

def main(page: ft.Page):
    page.title = "PikaClone"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Start the background logic in a separate thread
    threading.Thread(target=background_tasks, daemon=True).start()

    page.add(
        ft.AppBar(title=ft.Text("PIKACLONE"), center_title=True),
        ft.Text("Service running in background!", color="green"),
        ft.ElevatedButton("Browse Movies", on_click=lambda _: print("Navigating..."))
    )

if __name__ == "__main__":
    ft.app(target=main)


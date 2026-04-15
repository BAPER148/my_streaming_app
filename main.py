import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    # This is the "Backdoor". It loads the actual site inside your app.
    # We use a mobile-friendly streaming search engine.
    wv = ft.WebView(
        "https://vidsrc.to/trending",
        expand=True,
        on_page_started=lambda _: print("Loading..."),
        on_page_ended=lambda _: print("Loaded!"),
    )

    page.add(
        ft.AppBar(
            title=ft.Text("PIKACLONE ULTIMATE"),
            bgcolor="#111111",
            actions=[
                ft.IconButton(ft.Icons.REFRESH, on_click=lambda _: wv.reload())
            ]
        ),
        wv
    )

ft.app(target=main)

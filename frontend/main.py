import flet as ft
import requests
import asyncio

BACKEND_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 20

    resposta_ia = ft.Text(
        value="Olá! Sou a LexIA. Em que posso ajudar?",
        color=ft.Colors.WHITE,
        size=16,
        selectable=True,
        text_align=ft.TextAlign.CENTER,
        expand=True,
    )

    titulo = ft.Text(
        "LexIA",
        color=ft.Colors.CYAN_200,
        size=36,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
    )

    sugestoes = [
        "Como abrir um processo?",
        "Direitos trabalhistas"
    ]

    sugestao_cards = [
        ft.Container(
            content=ft.Text(sugestao, color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_600),
            bgcolor=ft.Colors.BLUE_GREY_700,
            padding=20,
            border_radius=15,
            width=280,
            height=100,
            alignment=ft.alignment.center
        )
        for sugestao in sugestoes
    ]

    cards_row = ft.Row(
        controls=sugestao_cards,
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    campo_texto = ft.TextField(
        hint_text="Digite sua pergunta...",
        filled=True,
        expand=True,
        border_radius=15,
        bgcolor=ft.Colors.BLUE_GREY_900,
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
    )

    async def enviar_pergunta(event=None):
        pergunta = campo_texto.value.strip()
        if not pergunta:
            return

        resposta_ia.value = "Pensando..."
        page.update()

        try:
            response = requests.post(BACKEND_URL, json={"pergunta": pergunta})
            resposta = response.json().get("resposta", "Erro ao obter resposta.")
            resposta_ia.value = resposta
        except Exception as e:
            resposta_ia.value = f"Erro: {str(e)}"
        finally:
            page.update()

    enviar_btn = ft.IconButton(
        icon=ft.Icons.SEND,
        icon_color=ft.Colors.CYAN_200,
        on_click=lambda e: asyncio.run(enviar_pergunta(e))
    )

    campo_texto.on_submit = lambda e: asyncio.run(enviar_pergunta(e))

    input_area = ft.Row(
        controls=[campo_texto, enviar_btn],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    page.add(
        ft.Column(
            controls=[
                titulo,
                resposta_ia,
                cards_row,
                ft.Container(
                    content=input_area,
                    alignment=ft.alignment.bottom_center,
                    padding=10,
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)

import flet as ft
import httpx

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"  # Preto puro
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 15  # Melhor em telas pequenas

    txt_question = ft.TextField(
        label="Digite sua pergunta jurídica",
        multiline=True,
        expand=True,
        min_lines=1,
        max_lines=5,
        border_radius=12,
        border_color="#00BCD4",
        text_style=ft.TextStyle(size=14),
    )

    chat = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    def send_message(e=None):
        question = txt_question.value.strip()
        if not question:
            return

        chat.controls.append(
            ft.Text(f"Você: {question}", color="#00FFFF", size=14)
        )
        txt_question.value = ""
        page.update()

        try:
            response = httpx.post(API_URL, json={"pergunta": question})
            if response.status_code == 200:
                resposta = response.json().get("resposta", "Erro ao obter resposta.")
                chat.controls.append(
                    ft.Text(f"LexIA: {resposta}", color="#FFBF00", size=14)
                )
            else:
                chat.controls.append(ft.Text("Erro no servidor!", color="#FF0000", size=14))
        except Exception as err:
            chat.controls.append(ft.Text(f"Erro: {err}", color="#FF0000", size=14))

        page.update()

    page.add(
        ft.Container(
            content=chat,
            expand=True,
            padding=10
        ),
        ft.Container(
            content=ft.Row(
                controls=[
                    txt_question,
                    ft.IconButton(icon="send", on_click=send_message),
                ],
                spacing=10
            ),
            padding=10
        )
    )

ft.app(target=main)

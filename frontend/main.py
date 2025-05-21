import flet as ft
import httpx

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 10

    chat = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )

    txt_question = ft.TextField(
        label="Digite sua pergunta jurídica",
        multiline=True,
        expand=True,
        min_lines=1,
        max_lines=4,
        border_radius=10,
        border_color="#00BCD4",
        text_style=ft.TextStyle(size=14),
    )

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
            response = httpx.post(API_URL, json={"mensagem": question})
            if response.status_code == 200:
                resposta = response.json().get("resposta", "Erro ao obter resposta.")
                chat.controls.append(
                    ft.Text(f"LexIA: {resposta}", color="#FFBF00", size=14)
                )
            else:
                chat.controls.append(
                    ft.Text(f"Erro no servidor: {response.status_code} - {response.text}", color="#FF0000", size=14)
                )
        except Exception as err:
            chat.controls.append(ft.Text(f"Erro: {err}", color="#FF0000", size=14))

        page.update()

    # Interface principal organizada verticalmente
    page.add(
        ft.Column(
            controls=[
                ft.Text("LexIA", size=24, weight="bold", color="white"),
                ft.Container(
                    content=chat,
                    expand=True,
                    padding=10,
                ),
                ft.Row(
                    controls=[
                        txt_question,
                        ft.IconButton(icon="send", on_click=send_message),
                    ],
                    spacing=10,
                ),
            ],
            expand=True,
        )
    )

ft.app(target=main)

import flet as ft
import httpx

API_URL = "http://localhost:3001/pergunta"  # ou o seu endpoint

def main(page: ft.Page):
    page.title = "LexIA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.scroll = ft.ScrollMode.AUTO

    txt_question = ft.TextField(
        label="Digite sua pergunta jurídica",
        multiline=True,
        expand=True,
        min_lines=1,
        max_lines=5,
        border_radius=10,
    )

    chat = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    def send_message(e=None):
        question = txt_question.value.strip()
        if not question:
            return

        chat.controls.append(ft.Text(f"Você: {question}", color=ft.colors.CYAN))
        txt_question.value = ""
        page.update()

        try:
            response = httpx.post(API_URL, json={"pergunta": question})
            if response.status_code == 200:
                resposta = response.json().get("resposta", "Erro ao obter resposta.")
                chat.controls.append(ft.Text(f"LexIA: {resposta}", color=ft.colors.AMBER))
            else:
                chat.controls.append(ft.Text("Erro no servidor!", color=ft.colors.RED))
        except Exception as err:
            chat.controls.append(ft.Text(f"Erro: {err}", color=ft.colors.RED))

        page.update()

    page.add(
        ft.Container(
            content=chat,
            expand=True,
            padding=10
        ),
        ft.Row(
            controls=[
                txt_question,
                ft.IconButton(icon=ft.icons.SEND, on_click=send_message),
            ],
            spacing=10
        ),
    )

ft.app(target=main)

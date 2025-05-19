import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F5F5"
    page.scroll = "auto"
    page.padding = 20

    chat_history = ft.Column(
        expand=True,
        spacing=12,
        scroll="auto"
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Mensagem do usuário
            chat_history.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Container(
                            content=ft.Text(user_message, selectable=True, color="white"),
                            bgcolor="#1976D2",
                            padding=12,
                            border_radius=12,
                            margin=5,
                            max_width=500
                        )
                    ]
                )
            )

            # Indicador de "pensando"
            thinking = ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Text("LexIA está pensando...", color="black"),
                        bgcolor="#E0E0E0",
                        padding=12,
                        border_radius=12,
                        margin=5,
                        max_width=500
                    )
                ]
            )
            chat_history.controls.append(thinking)
            page.update()

            try:
                response = requests.post(
                    API_URL,
                    json={"pergunta": user_message},
                    timeout=60
                )
                if response.status_code == 200:
                    assistant_response = response.json().get("resposta", "Não consegui entender.")
                else:
                    assistant_response = f"Erro {response.status_code}: {response.text}"
            except requests.Timeout:
                assistant_response = "⏱️ O servidor demorou muito para responder."
            except requests.ConnectionError:
                assistant_response = "❌ Sem conexão com o servidor."
            except Exception as ex:
                assistant_response = f"⚠️ Erro inesperado: {str(ex)}"

            chat_history.controls.remove(thinking)
            chat_history.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Text("LexIA", weight="bold", size=12, color="#4CAF50"),
                                ft.Text(assistant_response, selectable=True, color="black"),
                            ]),
                            bgcolor="#F1F8E9",
                            padding=12,
                            border_radius=12,
                            margin=5,
                            max_width=500
                        )
                    ]
                )
            )
            message_input.value = ""
            message_input.focus()
            page.update()

    message_input = ft.TextField(
        hint_text="Digite sua dúvida jurídica aqui...",
        border_radius=20,
        content_padding=15,
        expand=True,
        on_submit=send_message,
        shift_enter=True,
    )

    send_button = ft.IconButton(
        icon="send",
        tooltip="Enviar",
        on_click=send_message,
        style=ft.ButtonStyle(shape=ft.BoxShape.CIRCLE),
    )

    message_row = ft.Row(
        controls=[message_input, send_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def set_message(text):
        message_input.value = text
        send_message(None)

    def get_suggestion_cards():
        return ft.Column(
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.TextButton(
                        text="📚 Direito Civil",
                        on_click=lambda _: set_message("Explique sobre direito civil")
                    ),
                    bgcolor="#E3F2FD",
                    border_radius=8,
                    padding=10
                ),
                ft.Container(
                    content=ft.TextButton(
                        text="⚖️ Direito Penal",
                        on_click=lambda _: set_message("Explique sobre direito penal")
                    ),
                    bgcolor="#E8F5E9",
                    border_radius=8,
                    padding=10
                ),
                ft.Container(
                    content=ft.TextButton(
                        text="📝 Contratos",
                        on_click=lambda _: set_message("Como fazer um contrato?")
                    ),
                    bgcolor="#FFFDE7",
                    border_radius=8,
                    padding=10
                )
            ]
        )

    page.add(
        ft.Container(
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                expand=True,
                width=700,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("🤖 LexIA - Assistente Jurídico", style="headlineMedium", text_align="center"),
                    ft.Divider(),
                    ft.Container(
                        content=chat_history,
                        expand=True,
                        bgcolor="white",
                        border_radius=12,
                        padding=15,
                    ),
                    ft.Container(height=10),
                    message_row,
                    ft.Container(height=20),
                    ft.Text("Sugestões rápidas:", size=14, weight="bold"),
                    get_suggestion_cards(),
                ]
            )
        )
    )

    message_input.focus()

ft.app(target=main, view=ft.WEB_BROWSER)

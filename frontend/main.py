import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F5F5"
    page.padding = 20
    page.scroll = "auto"
    max_content_width = 700

    chat_history = ft.Column(
        scroll="auto",
        expand=True,
        spacing=12,
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Exibir mensagem do usuário
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

            # Indicador de "pensando..."
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

            # Remove "pensando..." e exibe resposta
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
        icon=ft.icons.SEND,
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
        return ft.Wrap(
            spacing=10,
            run_spacing=10,
            controls=[
                ft.ElevatedButton(
                    "📚 Direito Civil",
                    on_click=lambda _: set_message("Explique sobre direito civil"),
                    bgcolor="#E3F2FD",
                    color="black"
                ),
                ft.ElevatedButton(
                    "⚖️ Direito Penal",
                    on_click=lambda _: set_message("Explique sobre direito penal"),
                    bgcolor="#E8F5E9",
                    color="black"
                ),
                ft.ElevatedButton(
                    "📝 Contratos",
                    on_click=lambda _: set_message("Como fazer um contrato?"),
                    bgcolor="#FFFDE7",
                    color="black"
                ),
            ]
        )

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Text("🤖 LexIA - Assistente Jurídico", style="headlineMedium", text_align="center"),
                    alignment=ft.alignment.center
                ),
                ft.Divider(),
                ft.Container(
                    content=chat_history,
                    expand=True,
                    height=500,
                    bgcolor="white",
                    border_radius=12,
                    padding=15,
                ),
                ft.Container(height=10),
                message_row,
                ft.Container(height=20),
                ft.Text("Sugestões rápidas:", size=14, weight="bold"),
                get_suggestion_cards(),
            ],
            width=max_content_width,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )

    message_input.focus()

ft.app(target=main, view=ft.WEB_BROWSER)

import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    max_content_width = 600

    chat_history = ft.Column(
        scroll='auto',
        expand=True,
        spacing=10,
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message, selectable=True, color=ft.colors.WHITE),
                    bgcolor=ft.colors.BLUE_700,
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_right
                )
            )
            thinking_indicator = ft.Container(
                content=ft.Text("Pensando...", selectable=True),
                bgcolor=ft.colors.BLUE_GREY_50,
                padding=10,
                border_radius=8,
                alignment=ft.alignment.center_left
            )
            chat_history.controls.append(thinking_indicator)
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
                    assistant_response = f"Erro no servidor: {response.status_code}"
                    if response.text:
                        assistant_response += f"\nDetalhes: {response.text}"
            except requests.Timeout:
                assistant_response = "⏱️ Tempo excedido ao aguardar resposta do servidor."
            except requests.ConnectionError:
                assistant_response = "❌ Não foi possível conectar ao servidor."
            except Exception as ex:
                assistant_response = f"⚠️ Erro inesperado: {str(ex)}"

            # Remove "Pensando..." e mostra resposta
            chat_history.controls.remove(thinking_indicator)
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(assistant_response, selectable=True, color=ft.colors.BLACK),
                    bgcolor=ft.colors.LIGHT_GREEN_50,
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_left
                )
            )
            message_input.value = ""
            message_input.focus()
            page.update()

    message_input = ft.TextField(
        label="Digite sua dúvida jurídica",
        hint_text="Digite sua dúvida jurídica aqui...",
        border_radius=8,
        expand=True,
        on_submit=send_message,
        shift_enter=True,
    )

    def set_message(text):
        message_input.value = text
        send_message(None)

    def get_suggestion_cards():
        if page.width and page.width < 500:
            return ft.Column(
                controls=[
                    ft.Container(
                        content=ft.TextButton(
                            text="Direito Civil\nTire suas dúvidas sobre direitos e obrigações",
                            on_click=lambda _: set_message("Explique sobre direito civil"),
                        ),
                        width=page.width * 0.9,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        bgcolor=ft.colors.WHITE,
                        padding=10,
                        margin=5,
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            text="Direito Penal\nEntenda crimes e penas no Brasil",
                            on_click=lambda _: set_message("Explique sobre direito penal"),
                        ),
                        width=page.width * 0.9,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        bgcolor=ft.colors.WHITE,
                        padding=10,
                        margin=5,
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            text="Contratos\nComo elaborar e entender contratos",
                            on_click=lambda _: set_message("Como fazer um contrato?"),
                        ),
                        width=page.width * 0.9,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        bgcolor=ft.colors.WHITE,
                        padding=10,
                        margin=5,
                    ),
                ]
            )
        else:
            return ft.Row(
                spacing=10,
                controls=[
                    ft.ElevatedButton(
                        "Direito Civil",
                        on_click=lambda _: set_message("Explique sobre direito civil"),
                    ),
                    ft.ElevatedButton(
                        "Direito Penal",
                        on_click=lambda _: set_message("Explique sobre direito penal"),
                    ),
                    ft.ElevatedButton(
                        "Contratos",
                        on_click=lambda _: set_message("Como fazer um contrato?"),
                    ),
                ]
            )

    page.add(
        ft.Column(
            [
                ft.Text("LexIA - Assistente Jurídico", style="headlineMedium"),
                chat_history,
                message_input,
                ft.Container(height=10),
                get_suggestion_cards(),
            ],
            width=max_content_width,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )

    message_input.focus()

ft.app(target=main, view=ft.WEB_BROWSER)

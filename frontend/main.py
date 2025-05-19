import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"  # Backend no Render

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "auto"
    max_content_width = 600

    chat_history = ft.Column(
        scroll='auto',
        expand=True,
        spacing=10,
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Exibe a mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message, color=ft.colors.WHITE, selectable=True),
                    bgcolor="#1976D2",
                    padding=12,
                    border_radius=8,
                    alignment=ft.alignment.center_right,
                    margin=5,
                )
            )
            # Indicador de carregamento da IA
            thinking_indicator = ft.Container(
                content=ft.Text("Pensando...", color=ft.colors.BLACK, selectable=True),
                bgcolor="#EEEEEE",
                padding=12,
                border_radius=8,
                alignment=ft.alignment.center_left,
                margin=5,
            )
            chat_history.controls.append(thinking_indicator)
            page.update()

            try:
                response = requests.post(
                    API_URL,
                    json={"pergunta": user_message},
                    timeout=60  # ⏱️ Timeout estendido
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

            chat_history.controls.remove(thinking_indicator)
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(assistant_response, color=ft.colors.BLACK, selectable=True),
                    bgcolor="#EEEEEE",
                    padding=12,
                    border_radius=8,
                    alignment=ft.alignment.center_left,
                    margin=5,
                )
            )
            message_input.value = ""
            message_input.focus()
            page.update()

    # Campo de entrada de pergunta
    message_input = ft.TextField(
        label="Digite sua dúvida jurídica",
        hint_text="Digite sua dúvida jurídica aqui...",
        border_radius=8,
        expand=True,
        on_submit=send_message,
        shift_enter=True,
    )

    # Sugestões rápidas
    def set_message(text):
        message_input.value = text
        page.update()

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
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                        bgcolor="#ffffff",
                        padding=10,
                        margin=5,
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            text="Direito Penal\nEntenda crimes e penas no Brasil",
                            on_click=lambda _: set_message("Explique sobre direito penal"),
                        ),
                        width=page.width * 0.9,
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                        bgcolor="#ffffff",
                        padding=10,
                        margin=5,
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            text="Contratos\nComo elaborar e entender contratos",
                            on_click=lambda _: set_message("Como fazer um contrato?"),
                        ),
                        width=page.width * 0.9,
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                        bgcolor="#ffffff",
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

    # Layout da página
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

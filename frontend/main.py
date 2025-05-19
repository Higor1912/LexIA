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
            # Adiciona a mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message, selectable=True),
                    bgcolor="#BBDEFB",
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_right
                )
            )
            thinking_indicator = ft.Container(
                content=ft.Text("Pensando...", selectable=True),
                bgcolor="#F5F5F5",
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
                    timeout=30
                )
                if response.status_code == 200:
                    assistant_response = response.json().get("resposta", "Não consegui entender.")
                else:
                    assistant_response = f"Erro no servidor: {response.status_code}"
                    if response.text:
                        assistant_response += f"\nDetalhes: {response.text}"
            except requests.Timeout:
                assistant_response = "Tempo excedido ao aguardar resposta do servidor."
            except requests.ConnectionError:
                assistant_response = "Não foi possível conectar ao servidor."
            except Exception as ex:
                assistant_response = f"Erro inesperado: {str(ex)}"

            chat_history.controls.remove(thinking_indicator)
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(assistant_response, selectable=True),
                    bgcolor="#F5F5F5",
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_left
                )
            )
            message_input.value = ""
            message_input.focus()
            page.update()

    # 🧠 Campo de entrada do usuário
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
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
        else:
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.TextButton(
                            text="Direito Civil\nTire suas dúvidas sobre direitos e obrigações",
                            on_click=lambda _: set_message("Explique sobre direito civil"),
                        ),
                        width=200,
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
                        width=200,
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
                        width=200,
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                        bgcolor="#ffffff",
                        padding=10,
                        margin=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                wrap=True,
            )

    suggestion_cards = get_suggestion_cards()

    def on_resize(e):
        nonlocal suggestion_cards
        suggestion_cards = get_suggestion_cards()
        main_column.controls[3] = suggestion_cards
        page.update()

    page.on_resize = on_resize

    input_row = ft.Row(
        controls=[
            message_input,
            ft.Container(
                content=ft.IconButton(
                    icon="send",
                    on_click=send_message,
                    bgcolor="#2196F3",
                    icon_color="white"
                ),
                margin=ft.margin.only(left=10),
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=20,
    )

    main_column = ft.Column([
        ft.Container(
            content=ft.Text("LexIA", size=24, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=ft.Image(
                src="assets/logo.png",
                width=150,
                height=150,
                opacity=0.3,
                fit=ft.ImageFit.CONTAIN,
            ),
            alignment=ft.alignment.center,
        ),
        chat_history,
        suggestion_cards,
        input_row
    ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=max_content_width)

    page.add(
        ft.Container(
            content=main_column,
            expand=True,
            alignment=ft.alignment.center,
        )
    )

# Executa como app web
ft.app(target=main, view=ft.WEB_BROWSER, port=10000)

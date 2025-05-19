import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Modo claro/escuro baseado no sistema
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    max_content_width = 700

    # Avatar para assistente e usuário
    def avatar(nome, cor):
        return ft.CircleAvatar(content=ft.Text(nome, size=12, weight=ft.FontWeight.BOLD), bgcolor=cor)

    chat_history = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=12,
    )

    # Mensagem de boas-vindas
    chat_history.controls.append(
        ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                avatar("L", "#1976D2"),
                ft.Container(
                    content=ft.Text("Olá! Sou a LexIA, sua assistente jurídica. Como posso te ajudar hoje?"),
                    bgcolor="#EEEEEE",
                    padding=12,
                    border_radius=10,
                    width=page.width * 0.6,
                )
            ]
        )
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if not user_message:
            return

        # Mensagem do usuário
        chat_history.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.Container(
                        content=ft.Text(user_message, selectable=True),
                        bgcolor="#BBDEFB",
                        padding=12,
                        border_radius=10,
                        width=page.width * 0.6,
                    ),
                    avatar("Você", "#2196F3")
                ],
            )
        )

        # Indicador de "pensando..."
        thinking_indicator = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                avatar("L", "#1976D2"),
                ft.Container(
                    content=ft.Text("Pensando..."),
                    bgcolor="#EEEEEE",
                    padding=12,
                    border_radius=10,
                    width=page.width * 0.6,
                )
            ],
        )
        chat_history.controls.append(thinking_indicator)
        page.update()

        try:
            response = requests.post(API_URL, json={"pergunta": user_message}, timeout=30)
            if response.status_code == 200:
                assistant_response = response.json().get("resposta", "Não consegui entender.")
            else:
                assistant_response = f"Erro {response.status_code}: {response.text}"
        except requests.Timeout:
            assistant_response = "Tempo excedido ao aguardar resposta do servidor."
        except requests.ConnectionError:
            assistant_response = "Erro de conexão com o servidor."
        except Exception as e:
            assistant_response = f"Erro inesperado: {str(e)}"

        chat_history.controls.remove(thinking_indicator)

        # Mensagem da IA
        chat_history.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    avatar("L", "#1976D2"),
                    ft.Container(
                        content=ft.Text(assistant_response, selectable=True),
                       bgcolor="#EEEEEE",
                        padding=12,
                        border_radius=10,
                        width=page.width * 0.6,
                    )
                ],
            )
        )

        message_input.value = ""
        message_input.focus()
        page.update()

    message_input = ft.TextField(
        hint_text="Digite sua dúvida jurídica...",
        border_radius=8,
        expand=True,
        on_submit=send_message,
        shift_enter=True,
    )

    def set_message(texto):
        message_input.value = texto
        page.update()

    def get_suggestions():
        suggestions = [
            ("Direito Civil", "Explique sobre direito civil"),
            ("Direito Penal", "Explique sobre direito penal"),
            ("Contratos", "Como fazer um contrato?"),
        ]

        if page.width < 500:
            return ft.Column(
                spacing=8,
                controls=[
                    ft.FilledButton(
                        text=title,
                        on_click=lambda e, msg=msg: set_message(msg),
                    ) for title, msg in suggestions
                ]
            )
        else:
            return ft.Row(
                spacing=10,
                wrap=True,
                controls=[
                    ft.FilledButton(
                        text=title,
                        on_click=lambda e, msg=msg: set_message(msg),
                    ) for title, msg in suggestions
                ]
            )

    content = ft.Column(
        [
            ft.Text("LexIA - Assistente Jurídico", style="headlineMedium", text_align="center"),
            ft.Container(chat_history, height=page.height * 0.6, bgcolor="#fafafa", border_radius=8, padding=10),
            message_input,
            ft.Container(height=10),
            get_suggestions()
        ],
        width=max_content_width,
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)
    message_input.focus()

ft.app(target=main, view=ft.WEB_BROWSER)

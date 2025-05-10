import flet as ft
import os

def main(page: ft.Page):
    # Configurações da página
    page.title = "LexIA"
    page.theme_mode = "light"
    page.padding = 20
    page.window_width = 400
    page.window_height = 600
    
    # Área de chat
    chat_history = ft.Column(
        scroll='auto',
        expand=True,
        spacing=10,
    )

    # Campo de entrada
    message_input = ft.TextField(
        hint_text="Digite sua dúvida jurídica aqui...",
        border_radius=8,
        expand=True
    )

    def send_message(e):
        user_message = message_input.value
        if user_message and user_message.strip():  # Verifica se há mensagem e não é só espaço
            # Adiciona mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message),
                    bgcolor="#BBDEFB",
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_right
                )
            )
            
            # Simula resposta do assistente
            response = "Esta é uma resposta simulada do assistente jurídico."
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(response),
                    bgcolor="#F5F5F5",
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_left
                )
            )
            
            message_input.value = ""  # Limpa o campo
            message_input.focus()  # Mantém o foco no campo de texto
            page.update()

    def set_message(text):
        message_input.value = text
        page.update()

    # Cards de sugestão
    suggestion_cards = ft.Row(
        controls=[
            ft.Container(
                content=ft.TextButton(
                    text="Direito Civil\nTire suas dúvidas sobre direitos e obrigações",
                    on_click=lambda _: set_message("Explique sobre direito civil"),
                    style=ft.ButtonStyle(
                        color={"": "#1a1a1a"},
                    ),
                ),
                width=200,
                height=100,
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
                    style=ft.ButtonStyle(
                        color={"": "#1a1a1a"},
                    ),
                ),
                width=200,
                height=100,
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
                    style=ft.ButtonStyle(
                        color={"": "#1a1a1a"},
                    ),
                ),
                width=200,
                height=100,
                border=ft.border.all(1, "#e0e0e0"),
                border_radius=8,
                bgcolor="#ffffff",
                padding=10,
                margin=5,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        wrap=True,  # Permite que os cards quebrem em múltiplas linhas
    )

    # Layout principal
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Container(  # Container para centralizar o título
                    content=ft.Text(
                        "LexIA",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),
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
                ft.Row(
                    controls=[
                        message_input,
                        ft.Container(  # Adicionando um Container em volta do IconButton
                            content=ft.IconButton(
                                icon="send",
                                on_click=send_message,
                                bgcolor="#2196F3",
                                icon_color="white"
                            ),
                            margin=ft.margin.only(left=10),  # Margem à esquerda do botão
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=40,  # Aumentado o espaçamento
                )
            ]),
            expand=True
        )
    )

ft.app(target=main)

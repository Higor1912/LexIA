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
        if message_input.value:
            # Adiciona mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(message_input.value),
                    bgcolor="#BBDEFB",  # Azul claro
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment_.center_right
                )
            )
            
            # Simula resposta do assistente
            response = "Esta é uma resposta simulada do assistente jurídico."
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(response),
                    bgcolor="#F5F5F5",  # Cinza claro
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment_.center_left
                )
            )
            
            message_input.value = ""
            page.update()

    # Layout principal
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("LexIA", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Image(
                        src="assets/logo.png",
                        width=150,
                        height=150,
                        opacity=0.3,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    alignment=ft.alignment_.center,
                ),
                ft.Divider(),
                chat_history,
                ft.Row(
                    controls=[
                        message_input,
                        ft.IconButton(
                            icon="send",
                            on_click=send_message,
                            bgcolor="#2196F3",  # Azul
                            icon_color="white"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ]),
            expand=True
        )
    )

ft.app(target=main)

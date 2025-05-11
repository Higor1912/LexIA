import flet as ft
import os
import subprocess
import requests

# Configuração da API
API_URL = "http://localhost:3001/pergunta"

subprocess.Popen(["node", "../backend/server.js"])

def main(page: ft.Page):
    # Configurações da página
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 800  # Largura fixa
    page.window_height = 600  # Altura fixa
    page.window_resizable = False  # Impede o redimensionamento
    page.window_maximizable = False  # Impede a maximização
    
    # Área de chat
    chat_history = ft.Column(
        scroll='auto',
        expand=True,
        spacing=10,
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Adiciona mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message, selectable=True),
                    bgcolor="#BBDEFB",
                    padding=10,
                    border_radius=8,
                    alignment=ft.alignment.center_right
                )
            )
            
            # Adiciona indicador de "pensando"
            thinking_indicator = ft.Container(
                content=ft.Text("Pensando...", selectable=True),
                bgcolor="#F5F5F5",
                padding=10,
                border_radius=8,
                alignment=ft.alignment.center_left
            )
            chat_history.controls.append(thinking_indicator)
            page.update()
            
            # Faz a requisição para a API
            try:
                response = requests.post(
                    API_URL, 
                    json={"pergunta": user_message},
                    timeout=30  # Adiciona timeout para evitar espera infinita
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

            # Remove o indicador de "pensando" e adiciona a resposta
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

    # Campo de entrada modificado
    message_input = ft.TextField(
        label="Digite sua dúvida jurídica",
        hint_text="Digite sua dúvida jurídica aqui...",
        border_radius=8,
        expand=True,
        on_submit=send_message,  # Adiciona o handler para o evento Enter
        shift_enter=True,  # Permite usar Shift+Enter para nova linha
    )

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

    # Layout da barra de entrada
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
        spacing=40,
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
                input_row  # Usa a nova Row configurada
            ]),
            expand=True
        )
    )

ft.app(target=main)

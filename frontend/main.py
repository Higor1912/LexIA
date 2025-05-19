import flet as ft
import requests

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F5F5"
    page.scroll = "auto"
    page.padding = 20

    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    def send_message(e):
        user_message = message_input.value.strip()
        if user_message:
            # Adiciona mensagem do usuário
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(user_message, color="white", selectable=True),
                    bgcolor="#1976D2",
                    padding=12,
                    border_radius=10,
                    alignment=ft.alignment.center_right
                )
            )

            # Mostra "Pensando..."
            thinking = ft.Container(
                content=ft.Text("LexIA está pensando..."),
                bgcolor="#EEEEEE",
                padding=12,
                border_radius=10,
                alignment=ft.alignment.center_left
            )
            chat_history.controls.append(thinking)
            page.update()

            # Chamada para API
            try:
                response = requests.post(API_URL, json={"pergunta": user_message}, timeout=60)
                if response.status_code == 200:
                    reply = response.json().get("resposta", "Desculpe, não entendi.")
                else:
                    reply = f"Erro {response.status_code}: {response.text}"
            except requests.Timeout:
                reply = "⏱️ Tempo de resposta excedido."
            except requests.ConnectionError:
                reply = "❌ Erro de conexão."
            except Exception as ex:
                reply = f"⚠️ Erro: {str(ex)}"

            # Remove "Pensando..." e mostra resposta
            chat_history.controls.remove(thinking)
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(reply, color="black", selectable=True),
                    bgcolor="#C8E6C9",
                    padding=12,
                    border_radius=10,
                    alignment=ft.alignment.center_left
                )
            )
            message_input.value = ""
            page.update()

    message_input = ft.TextField(
        hint_text="Digite sua dúvida jurídica...",
        expand=True,
        on_submit=send_message
    )

    send_button = ft.IconButton(
        icon="send",
        tooltip="Enviar",
        on_click=send_message
    )

    def set_message(text):
        message_input.value = text
        send_message(None)

    def get_suggestions():
        return ft.Column(
            controls=[
                ft.ElevatedButton("📚 Direito Civil", on_click=lambda _: set_message("Explique sobre direito civil")),
                ft.ElevatedButton("⚖️ Direito Penal", on_click=lambda _: set_message("Explique sobre direito penal")),
                ft.ElevatedButton("📝 Contratos", on_click=lambda _: set_message("Como fazer um contrato?")),
            ]
        )

    page.add(
        ft.Column([
            ft.Text("🤖 LexIA - Assistente Jurídico", style="headlineSmall"),
            ft.Container(chat_history, height=400, bgcolor="white", border_radius=10),
            ft.Row([message_input, send_button]),
            ft.Divider(),
            ft.Text("Sugestões rápidas:", weight="bold"),
            get_suggestions(),
        ], expand=True)
    )

    message_input.focus()

ft.app(target=main, view=ft.WEB_BROWSER)

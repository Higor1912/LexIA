import flet as ft
import requests
import os

API_URL = "https://lexia-backend.onrender.com/pergunta"

def main(page: ft.Page):
    page.title = "LexIA - Assistente Jurídico"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Componentes da interface
    titulo = ft.Text("LexIA", size=32, weight="bold", color="blue")
    subtitulo = ft.Text("Seu assistente jurídico com IA", size=18, italic=True)

    chat = ft.Column(expand=True, scroll="auto")
    pergunta_input = ft.TextField(
        label="Digite sua pergunta",
        multiline=False,
        autofocus=True,
        expand=True,
        on_submit=lambda e: enviar_pergunta(e)
    )

    enviar_btn = ft.ElevatedButton("Enviar", on_click=lambda e: enviar_pergunta(e))

    entrada_pergunta = ft.Row(
        controls=[pergunta_input, enviar_btn],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Adiciona tudo na página
    page.add(
        ft.Column([
            titulo,
            subtitulo,
            ft.Divider(),
            chat,
            entrada_pergunta
        ], expand=True)
    )

    # Função que envia a pergunta para o backend e mostra a resposta
    def enviar_pergunta(e):
        pergunta = pergunta_input.value.strip()
        if not pergunta:
            return
        chat.controls.append(ft.Text(f"👤 Você: {pergunta}", size=16, weight="w500"))
        pergunta_input.value = ""
        page.update()

        try:
            response = requests.post(API_URL, json={"pergunta": pergunta})
            if response.status_code == 200:
                resposta = response.json().get("resposta", "⚠️ Resposta não encontrada.")
            else:
                resposta = "❌ Erro na resposta da API."
        except Exception as ex:
            resposta = f"🚨 Erro de conexão: {ex}"

        chat.controls.append(ft.Text(f"🤖 LexIA: {resposta}", size=16))
        page.update()

# Execução compatível com Render
if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8000)), host="0.0.0.0")

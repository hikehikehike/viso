import requests
import time
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

BASE_URL = "http://localhost:8000/api/chat"
AUTH_URL = "http://localhost:8000/api-token-auth/"
console = Console()

session = requests.Session()


def login():
    username = input("Username: ")
    password = input("Password: ")

    response = session.post(AUTH_URL, data={
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        token = response.json()["token"]
        session.headers.update({"Authorization": f"Token {token}"})
        console.print("[bold green]✅ Logged in![/bold green]")
        return token
    else:
        console.print("[bold red]❌ Login failed. Check your credentials.[/bold red]")
        exit()


def print_history():
    response = session.get(f"{BASE_URL}/messages/")
    if response.status_code == 200:
        for msg in response.json():
            role = "🤖" if msg["is_assistant"] else "🧑"
            color = "magenta" if msg["is_assistant"] else "cyan"
            console.print(f"[bold {color}]{role}: {msg['content']}[/bold {color}]")
    else:
        console.print("[red]⚠️ Failed to fetch message history.[/red]")


def main():
    login()

    conv = session.post(f"{BASE_URL}/conversations/").json()
    conv_id = conv["id"]

    console.print(Panel.fit("[bold green]🟢 AI Chat started. Type /exit to quit.[/bold green]"))
    print_history()

    while True:
        user_input = console.input("[bold cyan]You[/bold cyan]: ")
        if user_input.strip().lower() in ["/exit", "/quit"]:
            break

        response = session.post(f"{BASE_URL}/messages/", json={
            "conversation": conv_id,
            "content": user_input
        })

        with console.status("[bold magenta]🤖 Assistant is typing...[/bold magenta]", spinner="dots"):
            time.sleep(1)
            data = response.json()
        assistant_reply = data["assistant_message"]["content"]
        console.print(Panel.fit(Markdown(assistant_reply), title="🤖 Assistant", style="bold magenta"))


if __name__ == "__main__":
    main()

# utils/display.py

import webbrowser
import time
from rich import box
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.table import Table
from .pagination import paginate_list
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def show_loader(message="Loading...", duration=1):
    with console.status(f"[bold green]{message}[/bold green]", spinner="dots"):
        time.sleep(duration)


def show_status_response(response: dict, title: str = "Server Status") -> None:

    status = response.get("status", "Unknown")
    code = response.get("code", "N/A")

    if str(status).lower() in ["up", "success", "ok"]:
        color = "green"
        emoji = "✅"
    elif str(status).lower() in ["down", "fail", "error"]:
        color = "red"
        emoji = "❌"
    else:
        color = "yellow"
        emoji = "⚠️"

    body = Text()
    body.append(f"{emoji} Status: ", style="bold")
    body.append(f"{status}\n", style=f"bold {color}")
    body.append("📟 Code: ", style="bold")
    body.append(f"{code}", style="cyan")

    console.print(
        Panel(
            body,
            title=f"[bold]{title}[/bold]",
            border_style=color,
            box=box.ROUNDED,
        )
    )


def prompt_open_links(items) -> None:
    show_loader("Preparing list...")

    page_size = 10
    pages = list(paginate_list(items, page_size))
    current_page = 0

    while True:
        console.clear()

        header_panel = Panel(
            f":globe_with_meridians: [bold cyan]Links Viewer[/bold cyan] — {len(items)} total",
            style="bold blue",
        )
        console.print(header_panel)

        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.SIMPLE_HEAVY,
            row_styles=["none", "dim"],
            title=f"Page {current_page + 1} of {len(pages)}",
            title_style="bold white on blue",
        )
        table.add_column("#", style="bold yellow", width=4, justify="right")
        table.add_column("Title", style="bold white")
        table.add_column("URL", style="green", overflow="fold")

        for idx, item in enumerate(
            pages[current_page], start=current_page * page_size + 1
        ):
            table.add_row(
                str(idx), item["title"], f"[link={item['url']}]{item['url']}[/link]"
            )

        console.print(table)
        console.print(
            "\n[bold cyan]Commands:[/bold cyan] [yellow]n[/yellow]=Next, [yellow]p[/yellow]=Prev, [yellow]q[/yellow]=Quit"
        )

        choice = (
            console.input("[bold green]Enter choice:[/bold green] ").strip().lower()
        )

        if choice == "q":
            console.print("[bold red]Exiting...[/bold red]")
            break
        elif choice == "n":
            current_page = min(current_page + 1, len(pages) - 1)
        elif choice == "p":
            current_page = max(current_page - 1, 0)
        else:
            try:
                num = int(choice)
                real_index = current_page * page_size + (num - 1)
                url = items[real_index]["url"]
                title = items[real_index]["title"]
                if Confirm.ask(f"Open '{title}'?"):
                    webbrowser.open(url)
            except:
                console.print("[bold red]Invalid input[/bold red]")


def interactive_download_prompt(data) -> None:
    show_loader("Loading download sections...")

    if data["status"] != "Success":
        console.print(
            Panel(
                f"[red]{data.get('message', 'Unknown error')}[/red]",
                title="Error",
                style="bold red",
            )
        )
        return

    console.print(
        Panel(
            f"[bold green]Download Links for:[/bold green] {data['title']}",
            style="green",
        )
    )
    sections = data["sections"]

    while True:
        console.print("\n[bold cyan]Available Sections:[/bold cyan]")
        for i, name in enumerate(sections.keys(), 1):
            console.print(
                f"[yellow]{i}.[/yellow] {name} ([green]{len(sections[name])} links[/green])"
            )
        console.print("[red]0.[/red] Exit")

        choice = console.input(
            "[bold green]Select section number:[/bold green] "
        ).strip()
        if choice == "0":
            break

        try:
            section = list(sections.keys())[int(choice) - 1]
        except:
            console.print("[red]Invalid choice[/red]")
            continue

        links = sections[section]
        if not links:
            console.print(f"[yellow]No links in {section}[/yellow]")
            continue

        table = Table(
            title=f"Section: {section}",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAVY,
        )
        table.add_column("#", style="bold yellow", width=4, justify="right")
        table.add_column("Title", style="white")
        table.add_column("URL", style="green", overflow="fold")

        for i, (url, title) in enumerate(links, 1):
            table.add_row(str(i), title, f"[link={url}]{url}[/link]")

        console.print(table)

        while True:
            link_choice = (
                console.input(
                    "[bold cyan]Enter link #[/bold cyan] to open or [red]'b'[/red] to go back: "
                )
                .strip()
                .lower()
            )
            if link_choice == "b":
                break
            try:
                idx = int(link_choice)
                webbrowser.open(links[idx - 1][0])
            except:
                console.print("[red]Invalid link number[/red]")

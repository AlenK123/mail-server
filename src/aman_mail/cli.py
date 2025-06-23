"""Console script for aman_mail."""
import aman_mail

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for aman_mail."""
    console.print("Replace this message by putting your code into "
               "aman_mail.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()

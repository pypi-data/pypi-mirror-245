from pathlib import Path
from typing import Annotated, Optional

import typer
from click import ClickException
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from check_keepass_passwords.checker import PasswordEvaluator, PasswordScore

app = typer.Typer()
console = Console()


@app.command(
    name="check",
    help="Checks a keepass 2.x database for passwords that are considered unsafe by design or have been compromised.",
)
def check(
        *,
        database: Annotated[typer.FileBinaryRead, typer.Argument(
            help="Path to keepass 2.x database file.",
        )],
        keyfile: Annotated[Optional[Path], typer.Option(
            "--keyfile", "-k",
            help="Path to the keyfile.",
        )] = None,
        no_password: Annotated[Optional[bool], typer.Option(
            "--no-password", "-n",
            help="Disables password prompt (usually in conjunction with --keyfile).",
        )] = False,
        show_all_passwords: Annotated[Optional[bool], typer.Option(
            "--show-all", "-a",
            help="Shows all passwords,  (usually in conjunction with --keyfile).",
        )] = False,
        disable_compromise_check: Annotated[Optional[bool], typer.Option(
            "--disable-compromise-check", "-C",
            help='Disable the check for compromised passwords.',
        )] = False,
        disable_scoring: Annotated[Optional[bool], typer.Option(
            "--disable-scoring", "-S",
            help="Disable password scoring.",
        )] = False,
        minimum_score_level: Annotated[Optional[int], typer.Option(
            "--min-score", "-m",
            help="Minimum score for a password to be considered safe. (on the 0-4 scale of zxcvbn).",
        )] = 2,
        show_entries: Annotated[Optional[bool], typer.Option(
            "--show-entries", "-e",
            help="List entries for each password.",
        )] = False,
):
    password = None if no_password else typer.prompt("Password", hide_input=True)
    minimum_score = PasswordScore.get_by_score(minimum_score_level)

    try:
        with PyKeePass(database, password=password, keyfile=keyfile) as kp:
            checker = PasswordEvaluator(
                kp,
                compromise_check_enabled=not disable_compromise_check,
                scoring_enabled=not disable_scoring,
            )

            table = Table(header_style='bold magenta', box=box.SIMPLE_HEAD)
            table.add_column("PASSWORD", style='blue')
            table.add_column("ENTRIES", style='cyan')

            if not disable_scoring:
                table.add_column("SCORE")

            if not disable_compromise_check:
                table.add_column("COMPROMISED")

            with Progress() as progress:
                task = progress.add_task("[cyan]Checking passwords", total=checker.count_passwords())

                for checked_password in checker.check_passwords():
                    progress.update(task, advance=1)
                    is_score_good = True if disable_scoring else checked_password.score >= minimum_score

                    if (
                            not show_all_passwords
                            and (disable_compromise_check or not checked_password.is_compromised)
                            and (disable_scoring or is_score_good)
                    ):
                        continue

                    row = [
                        checked_password.password,
                        "\n".join(sorted('/'.join(e.path) for e in checked_password.entries))
                        if show_entries
                        else f"{len(checked_password.entries)} entries",
                    ]

                    if not disable_scoring:
                        row.append(
                            f"[green]{checked_password.score.label} [dim]({checked_password.score.score})"
                            if is_score_good
                            else f"[red]{checked_password.score.label} [dim]({checked_password.score.score})",
                        )

                    if not disable_compromise_check:
                        row.append(
                            "[green]uncompromised[/green]"
                            if checked_password.compromise_count == 0
                            else f"[red]compromised [dim]({checked_password.compromise_count} times)",
                        )

                    table.add_row(*row)

            console.print(table)

    except CredentialsError as err:
        raise ClickException(str(err)) from err

from typing import Optional

import click

from src.cron import create_crontab, delete_crontab


@click.group()
def cli():
    """Create and manage MacOS custom notifications with crontabs."""
    pass


@cli.command()
@click.option("--title", type=str)
@click.option("--text", type=str)
@click.option(
    "--interval", help="Crontab interval, * * * * * or 21:00 or @5s every 5 seconds"
)
def create(title: Optional[str], text: Optional[str], interval: Optional[str]) -> None:
    """Create MacOS notifications in crontabs"""
    title_str = title if title else ""
    text_str = text if text else ""
    command_setup = len(title_str) != 0 and len(text_str) != 0

    while not command_setup:
        if len(title_str) == 0:
            title = click.prompt(
                click.style("Please type the title of the notification", fg="green"),
                type=str,
            )
        if len(text_str) == 0:
            text_str = click.prompt(
                click.style("Please add the text of the notification", fg="blue"),
                type=str,
            )

        click.echo()
        click.secho("Current notification setting:", fg="yellow", bold=True)
        click.secho("-----------------------------", fg="yellow")
        click.secho(f"Title: {title_str}", bold=True, fg="green")
        click.secho(f"Text: {text_str}", bold=True, fg="blue")
        click.echo()

        if click.confirm(click.style("Do you want to continue?", fg="red")):
            command_setup = True
        else:
            if click.confirm(click.style("Change the title?", fg="yellow")):
                title_str = ""
            if click.confirm(click.style("Change the text?", fg="yellow")):
                text_str = ""
        click.echo()

    if not interval:
        interval = click.prompt(
            click.style(
                "Enter crontab interval, * * * * * or 21:00 or @5s every 5 seconds",
                fg="green",
            ),
            type=str,
        )
    interval_str = interval if interval else "* * * * *"

    msg = create_crontab(title_str, text_str, interval_str)
    click.echo(click.style(msg, fg="yellow"))
    click.secho("Please make sure to cancel it :)", fg="yellow")


@cli.command()
@click.argument("job_id", required=False)
@click.option("--all/--no-all", "all_jobs", default=False, type=bool)
@click.option("--list/--no-list", "list_jobs", default=False, type=bool)
@click.option("--disable/--no-disable", "disable", default=False, type=bool)
@click.option("-s", "--search", "search_job", type=str)
def cancel(
    job_id: str, all_jobs: bool, list_jobs: bool, disable: bool, search_job: str
) -> None:
    """Cancel, list and deactivate jobs"""
    msg = delete_crontab(job_id, all_jobs, list_jobs, disable, search_job)
    click.echo(click.style(msg, fg="yellow"))


if __name__ == "__main__":
    cli()

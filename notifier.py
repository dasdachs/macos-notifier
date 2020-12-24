import re
import uuid

import click
from crontab import CronTab



INTERVAL_RE = re.compile(r"@(?P<value>\d+)(?P<unit>s|m|h|d)")

@click.group()
def cli():
    """Create and manage MacOS custom notifications with crontabs."""
    pass


@cli.command()
@click.option("--title", type=str)
@click.option("--text", type=str)
@click.option(
    "--interval", 
    help="Crontab interval, * * * * * or 21:00 or @5s every 5 seconds"
)
def create(title: str, text: str, interval: str) -> None:
    """Create MacOS notifications in crontabs"""
    command_setup = title and text

    while not command_setup:
        if not title or len(title) == 0:
            title = click.prompt(
                click.style("Please type the title of the notication", fg="green"), type=str
            )
        if not text or len(text) == 0:
            text = click.prompt(
                click.style("Plase add the text of the notification", fg="blue"), type=str
            )

        click.echo()
        click.secho("Current notification setting:", fg="yellow", bold=True)
        click.secho("-----------------------------", fg="yellow")
        click.secho(f"Title: {title}", bold=True, fg="green")
        click.secho(f"Text: {text}", bold=True, fg="blue")
        click.echo()

        if click.confirm(click.style("Do you want to continue?", fg="red")):
            command_setup = True
        else:
            if click.confirm(click.style("Change the title?", fg="yellow")):
                title = ""
            if click.confirm(click.style("Change the text?", fg="yellow")):
                text = ""
        click.echo()

    if not interval:
        interval = click.prompt(
            click.style(
               "Enter crontab interval, * * * * * or 21:00 or @5s every 5 seconds",
                fg="green"
            )
            , type=str
        )
    create_crontab(title, text, interval)
    click.echo("Create crontab, please make sure to cancle it :)")


@cli.command()
@click.option("--all/--no-all", "all_jobs", default=False, type=bool)
@click.option("--list/--no-list", "list_jobs", default=False, type=bool)
@click.option("--disable/--no-disable", "disable", default=False, type=bool)
@click.option("-s", "--search", "search_job", type=str)
@click.argument("job_id", required=False)
def cancel(
    job_id: str,
    list_jobs: bool,
    all_jobs: bool,
    disable: bool,
    search_job: str
) -> None:
    """Cancle jobs"""
    cron = CronTab(user=True)

    if all_jobs:
        cron.remove_all()
    elif list_jobs:
        for job in cron:
            print(job)
    elif search_job:
        cron.remove_all(search_job)
        cron.remove_all(comment=search_job)
    else:
        job = None
        for j in cron:
            if j.comment == job_id:
                job = j
        if job:
            if disable:
                job.enable(False)
            cron.remove(job)
    
    cron.write()



def create_crontab(title: str, text: str, interval: str) -> None:
    """Parses interval and creates the notification interval"""
    cron = CronTab(user=True)
    command = f"osascript -e 'display notification \"{text}\" with title \"{title}\"'"
    comment = f"JobID: {uuid.uuid4()}"

    job = cron.new(command=command, comment=comment)

    if "*" in interval:
        cron = CronTab(tab=f"""{interval} {command}""")
    elif "@" in interval:
        match = re.search(INTERVAL_RE, interval)
        # TODO: Handle empty values
        unit = match["unit"]
        value = match["value"]

        if unit == "m":
            job.minute.every(value)
        elif unit == "h":
            job.hour.every(value)
        elif unit == "d":
            job.day.every(value)
    else:
        raise Exception("Other formats currenty not suppoerted")
    cron.write()


if __name__ == "__main__":
    cli()

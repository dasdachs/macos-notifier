import os
import re
import uuid
from typing import Optional

from crontab import CronTab

from exceptions import InvalidNotificationIntervalException


TAB_FILE = "TAB_FILE"
INTERVAL_RE = re.compile(r"@(?P<value>\d+)(?P<unit>s|m|h|d)")


def create_crontab(title: str = "", text: str = "", interval: str = "") -> str:
    """Parses and interval and creates the notification interval"""
    cron = get_crontab()

    command = f'osascript -e \'display notification "{text}" with title "{title}"\''
    comment = f"mac-os-notifier-id: {uuid.uuid4()}"

    job = cron.new(command=command, comment=comment)

    if "*" in interval:
        job.setall(interval)
    elif "@" in interval:
        match = re.search(INTERVAL_RE, interval)

        if not match:
            raise InvalidNotificationIntervalException(
                f"Time interval {interval} is not valid. Interval should be like this: @10m."
            )

        unit = match["unit"]
        value = match["value"]

        if unit == "m":
            job.minute.every(value)
        elif unit == "h":
            job.hour.every(value)
        elif unit == "d":
            job.day.every(value)
    else:
        raise InvalidNotificationIntervalException(
            f"Time interval {interval} is not valid or not supported."
        )
    cron.write()

    return f"Created notification {title}: {text} with interval {job} (mac-os-notifier-id: {job.comment}) 🚀"


def delete_crontab(
    job_id: str,
    all_jobs: bool = False,
    list_jobs: bool = False,
    disable: bool = False,
    search_job: Optional[str] = None,
) -> str:
    """Removes or interval and creates the notification interval"""
    cron = get_crontab()

    msg = ""

    if all_jobs:
        lst = []

        for job in cron:
            if "mac-os-notifier-id" in job.comment:
                lst.append(str(job))
                cron.remove(job)
        jobs_list = "\n".join(lst)
        msg = f"Removed the following jobs:\n {jobs_list}"
    elif list_jobs:
        lst = []
        for job in cron:
            lst.append(str(job))

        msg = "\n".join(lst)
    elif search_job:
        cron.remove_all(search_job)
        cron.remove_all(comment=search_job)
        msg = f"Removed all cronjobs with comand or comment like {search_job}"
    else:
        job = None
        for j in cron:
            if job_id in j.comment:
                job = j
        if job:
            if disable:
                job.enable(False)
            cron.remove(job)
            msg = f"{'Deactivated' if disable else 'Removed'} cronjob with comment: `JobID:  {job_id}"
        else:
            msg = f"Could not find cronjob with id {job_id}"

    cron.write()

    return msg


def get_crontab() -> CronTab:
    """Helper function to setup the crontab object."""
    tab_file_name = os.environ.get(TAB_FILE)

    if tab_file_name:
        return CronTab(user=True, tabfile=tab_file_name)
    return CronTab(user=True)

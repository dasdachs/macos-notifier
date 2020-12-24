import os
from pathlib import Path

import pytest

from src.cron import TAB_FILE, get_crontab, create_crontab, delete_crontab


CRONTAB_FILE_NAME = "testing.tab"
MOCK_CREATE_PARAMS = [
    ["Test", "Test text", "@10m"],
    ["Test_2", "Test text", "@1d"],
    ["Test_3", "A longer string ", "@1d"],
    ["Test_4", "A longer string ", "* * * * *"],
]


@pytest.fixture
def setup():
    """Creates and removes a dummy crontab file"""
    os.environ[TAB_FILE] = CRONTAB_FILE_NAME

    p = Path(CRONTAB_FILE_NAME)
    p.touch()

    yield

    p.unlink()


@pytest.fixture(params=MOCK_CREATE_PARAMS)
def setup_with_parametes(request):
    """Creates and removes a dummy crontab file"""
    os.environ[TAB_FILE] = CRONTAB_FILE_NAME

    p = Path(CRONTAB_FILE_NAME)
    p.touch()

    yield request.param

    p.unlink()


def test_get_crontab(setup):
    """Test get_crontab with env set to TAB_FILE"""
    cron = get_crontab()

    assert cron.filen == CRONTAB_FILE_NAME


def test_create_crontab_sets_correct_command(setup_with_parametes):
    """Test get_crontab with env set to TAB_FILE"""
    title, text, interval = setup_with_parametes
    create_crontab(title, text, interval)
    expected_command = (
        f'osascript -e \'display notification "{text}" with title "{title}"\''
    )
    cron = get_crontab()

    assert cron.crons[0].command == expected_command


def test_delete_crontab_deletes_all_tabs(setup):
    """Test get_crontab with env set to TAB_FILE"""
    for param in MOCK_CREATE_PARAMS:
        title, text, interval = param
        create_crontab(title, text, interval)

    delete_crontab("", all_jobs=True)
    cron = get_crontab()

    assert len(cron.crons) == 0


def test_delete_crontab_deletes_single_tab(setup):
    """Test get_crontab with env set to TAB_FILE"""
    create_crontab("Test", "Test text", "@10m")

    cron = get_crontab()
    cron_tab_id = cron.crons[0].comment.replace("mac-os-notifier-id: ", "")

    delete_crontab(cron_tab_id)

    cron = get_crontab()

    assert len(cron.crons) == 0

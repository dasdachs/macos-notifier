from click.testing import CliRunner

from notifier import cli


def test_create_no_args():
    runner = CliRunner()
    result = runner.invoke(
        cli, 
        ["create", "--title", "Test", "--text", "Test text"]
    )

    assert result.output == 'Hello Peter!\n'

import pytest
from click.testing import CliRunner

import pandas_tab.cli
from pandas_tab.cli import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def ipython_scripts_dir(tmpdir):
    directory = tmpdir.mkdir("startup")
    yield directory


@pytest.fixture(autouse=True)
def mock_scripts_dir(monkeypatch, ipython_scripts_dir):
    monkeypatch.setattr(
        pandas_tab.cli,
        "get_ipython_startup_dir",
        lambda *args, **kwargs: ipython_scripts_dir.strpath
    )
    yield


def test_cli_base(cli_runner):
    res = cli_runner.invoke(cli)
    assert res.exit_code == 0


def test_cli_init(cli_runner, ipython_scripts_dir):
    res = cli_runner.invoke(cli, ["init"])
    assert res.exit_code == 0
    assert (ipython_scripts_dir / "50-pandas_tab_init.py").exists()


def test_cli_remove(cli_runner, ipython_scripts_dir):
    cli_runner.invoke(cli, ["init"])
    assert (ipython_scripts_dir / "50-pandas_tab_init.py").exists()

    res = cli_runner.invoke(cli, ["delete"])
    assert res.exit_code == 0
    assert not (ipython_scripts_dir / "50-pandas_tab_init.py").exists()

import os
import click


DEFAULT_JUPYTER_STARTUP_SCRIPT_NAME = "50-pandas_tab_init.py"
PANDAS_TAB_SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "scripts")
PANDAS_TAB_STARTUP_SCRIPT = "jupyter_init.py.jinja"


def get_ipython_startup_dir(profile_name: str) -> str:
    """Get the path to place startup scripts in."""
    from IPython.paths import get_ipython_dir
    from IPython.core.profiledir import ProfileDir
    profile_dir = ProfileDir.find_profile_dir_by_name(get_ipython_dir(), profile_name)
    return profile_dir.startup_dir


def create_jinja_env():
    """Lazy load jinja2 environment for scripts."""
    import jinja2
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(PANDAS_TAB_SCRIPTS_DIR)
    )


@click.group("pandas-tab")
def cli():
    """Manage IPython startup script for pandas_tab."""
    try:
        import IPython  # noqa: F401
        import jinja2  # noqa: F401
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"No module named {e.name!r}."
            " The Pandas-Tab CLI requires IPython and jinja2 to be installed."
            " You can `pip install pandas_tab[full]` to install these dependencies."
        )


@cli.command("init")
@click.option("--filename", "-f",
              type=click.STRING,
              default=DEFAULT_JUPYTER_STARTUP_SCRIPT_NAME)
@click.option("--profile-name", "-p",
              type=click.STRING,
              default="default",
              help="The name of the IPython profile to put the script in.")
@click.option("--noisy",
              is_flag=True,
              help="If set, the startup script will warn the user if pandas_tab"
                   " fails to load. By default, if pandas_tab fails to load"
                   "automatically in IPython, it will fail silently.")
@click.option("--overwrite",
              is_flag=True,
              help="Overwrite the script file if it already exists.")
def init(
        filename: str = DEFAULT_JUPYTER_STARTUP_SCRIPT_NAME,
        profile_name: str = "default",
        noisy: bool = False,
        overwrite: bool = False
):
    """Create startup script for IPython."""
    startup_dir = get_ipython_startup_dir(profile_name)
    script_file_path = os.path.join(startup_dir, filename)

    jinja_env = create_jinja_env()
    script = jinja_env.get_template("jupyter_init.py.jinja").render(noisy=noisy)

    if not overwrite and os.path.exists(script_file_path):
        raise FileExistsError(f"File {script_file_path} already exists.")

    with open(script_file_path, "w+") as f:
        f.write(script)

    click.echo(f"Created file {filename!r} in {startup_dir!r}")


@cli.command("delete")
@click.option("--filename", "-f",
              type=click.STRING,
              default=DEFAULT_JUPYTER_STARTUP_SCRIPT_NAME)
@click.option("--profile-name", "-p",
              type=click.STRING,
              default="default",
              help="The name of the IPython profile to look for the script in.")
def delete(
        filename: str = DEFAULT_JUPYTER_STARTUP_SCRIPT_NAME,
        profile_name: str = "default"
):
    """Delete startup script for IPython."""
    startup_dir = get_ipython_startup_dir(profile_name)
    script_file_path = os.path.join(startup_dir, filename)
    os.remove(script_file_path)
    click.echo(f"File {filename!r} deleted from {startup_dir}.")

import importlib
import os
import pathlib
import pkgutil
import shutil

import click

from markdata import markdata, __version__


@click.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path(), required=False)
@click.option(
    "--fm-type",
    type=click.Choice(["JSON", "YAML", "TOML"]),
    default=None,
    help="The type of front matter to parse.",
)
@click.option(
    "--root",
    type=click.Path(exists=True),
    default=None,
    help="The directory that paths will be resolved relative to.",
)
@click.option(
    "--directives",
    type=click.Path(exists=True),
    default=None,
    help="The directory containing your custom directives.",
)
@click.version_option(version=__version__.__version__)
def cli(source, destination, fm_type, root, directives):
    """A flavor-agnostic extension framework for Markdown.

    Reads from <SOURCE> and writes to <DESTINATION>.

    If <SOURCE> is a single file, it will be converted to Markdown and written
    to <DESTINATION> (default: stdout).

    If <SOURCE> is a directory, all child Markdata files will be converted to
    Markdown and written to <DESTINATION> (default: overwrite <SOURCE>).
    """
    loaded = {}
    if directives:
        loaded = {
            pkg: getattr(finder.find_module(pkg).load_module(pkg), "main")
            for finder, pkg, _ in pkgutil.iter_modules(path=[directives])
        }

    src_p = pathlib.Path(source)
    src_d = src_p.is_dir()

    if src_d and destination:
        shutil.copytree(source, destination)
        src_p = pathlib.Path(destination)

    files = src_p.glob("**/*.md") if src_d else [src_p]
    for src in files:
        with src.open() as f:
            markdown = markdata(f, loaded, fm_type, root)

        if src_d:
            # We're working on a directory.
            with src.open("w+") as f:
                f.write(markdown)
        elif destination:
            # We were given a single-file destination.
            with open(destination, "w+") as f:
                f.write(markdown)
        else:
            # stdin (single file default).
            click.echo(markdown)

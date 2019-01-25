import importlib
import pathlib
import pkgutil

import click

from markdata import markdata, __version__


@click.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path(), required=False)
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
def cli(source, destination, root, directives):
    """A flavor-agnostic extension framework for Markdown.

    Reads from <SOURCE> and writes to <DESTINATION>.

    If <SOURCE> is a directory, all child Markdata files will be converted to
    Markdown and written to <DESTINATION> (default: overwrite <SOURCE>).

    If <SOURCE> is a single file, it will be converted to Markdown and written
    to <DESTINATION> (default: stdout).
    """
    loaded = {}
    if directives:
        loaded = {
            name: getattr(importlib.import_module(value + "." + name), "main")
            for _, name, _ in pkgutil.iter_modules(path=[directives])
        }

    src_p = pathlib.Path(source)
    src_d = src_p.is_dir()

    files = src_p.glob("**/*.md") if src_d else [src_p]
    for src in files:
        if src_d and destination:
            dest = src_p.resolve().replace(src_p.name, destination)
        elif src_d:
            dest = src_p.name
        else:
            dest = destination

        with src.open() as f:
            markdown = markdata(f, loaded, root)

        if dest:
            with open(dest, "w+") as f:
                f.write(markdown)
        else:
            click.echo(markdown)

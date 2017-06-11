# -*- coding: utf-8 -*-

import click

from roundhouse import __version__


@click.command(context_settings=dict(
    help_option_names=['-h', '--help']
))
@click.version_option(version=__version__)
def main():
    """Console script for roundhouse"""
    click.echo("Replace this message by putting your code into "
               "roundhouse.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()

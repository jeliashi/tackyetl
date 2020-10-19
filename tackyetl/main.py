from typing import Iterable

import click

if __package__ is None or __package__ == "":
    # uses current directory visibility
    import db
    import owm
else:
    # uses current package visibility
    from . import db, owm


@click.command()
@click.argument("station_id", nargs=1, type=click.STRING)
@click.option("-s", "--to-stdout", "to_stdout", is_flag=True)
@click.option("-f", "--to-filename", "to_filename", type=str)
def get(station_id: str, to_stdout: bool = False, to_filename: str = None):
    # (TODO) add scheduling logic
    persistance_cls = db.StdOut if to_stdout else db.CSVDatabase
    with persistance_cls() as persistance:
        data = owm.postproc(owm.retrieve(station_id))
        persistance.create(data)


@click.command()
def meta():
    with db.CSVDatabase() as persistance:
        print(persistance.entries)


@click.command()
@click.argument("name", nargs=-1)
def read(name):
    with db.CSVDatabase() as persistance:
        print(persistance.read(name))
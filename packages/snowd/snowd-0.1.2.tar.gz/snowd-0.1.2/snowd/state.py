import logging
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import click

log = logging.getLogger(__name__)


def timestampfilestate(filename):
    file = Path(filename)

    lastrun = datetime.fromtimestamp(0)
    if file.is_file():
        try:
            timestamp = int(file.read_text())
            lastrun = datetime.fromtimestamp(timestamp)
        except Exception:
            log.warning(f"file {file} exists but with invalid content")

    def get():
        nonlocal lastrun
        return lastrun

    def save(date=None):
        nonlocal lastrun
        if not date:
            date = datetime.utcnow()
        lastrun = date
        print(f"Saving {lastrun}")
        file.write_text(str(int(lastrun.timestamp())))

    return get, save


@contextmanager
def timestampfile(filename):
    now = datetime.utcnow()
    file = Path(filename)

    lastrun = now
    if file.is_file():
        try:
            timestamp = int(file.read_text())
            lastrun = datetime.fromtimestamp(timestamp)
        except Exception:
            log.warning(f"file {file} exists but with invalid content")

    def savelast(date):
        nonlocal now
        now = date

    with open(file, "w") as f:
        f.write(str(int(now.timestamp())))
    try:
        yield lastrun, savelast
    finally:
        with open(file, "w") as f:
            f.write(str(int(now.timestamp())))


@click.command("hello")
@click.argument("name", default="(anonymous person)")
@click.option(
    "-a",
    "--adjective",
    type=click.Choice(["handsome", "smart"]),
    default="handsome",
)
def main(name, adjective):
    print(f"hello {adjective} {name}")

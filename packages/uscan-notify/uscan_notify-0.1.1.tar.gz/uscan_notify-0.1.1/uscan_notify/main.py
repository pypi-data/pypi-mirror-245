#!/usr/bin/env python3
# debian-rfs-stats - Calculate statistics regarding sponsorship requests.
# Copyright (c) 2023 Maytham Alsudany <maytha8thedev@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from platformdirs import user_data_dir
import sqlite3
from uscan_notify.versions import package_versions
import click
import os

__APP_NAME__ = "uscan-notify"
data_dir = user_data_dir(__APP_NAME__)


@click.command()
@click.option(
    "--db-path",
    default=f"{data_dir}/database.db",
    show_default=True,
    help="Location of SQLite3 database.",
)
@click.argument("packages", nargs=-1)
def main(db_path: str, packages: list[str]):
    if not os.path.exists(os.path.dirname(db_path)):
        os.mkdir(os.path.dirname(db_path))
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS versions(package, upstream)")

    for pkg in packages:
        versions = package_versions(pkg)
        results = cur.execute(
            "SELECT 1 FROM versions WHERE package = ? AND upstream = ?",
            (pkg, versions["upstream"]),
        ).fetchone()
        if results is None:
            print(f"{results[0]} !== {versions['upstream']}")
            if versions["debian"] != versions["upstream"]:
                print(f"\n== Package: {pkg} ==")
                print(f"Debian version is outdated ({versions['debian']})")
                print(f"New upstream version ({versions['upstream']}) available")
            cur.execute(
                "INSERT INTO versions VALUES (?,?)", (pkg, versions["upstream"])
            )
            con.commit()

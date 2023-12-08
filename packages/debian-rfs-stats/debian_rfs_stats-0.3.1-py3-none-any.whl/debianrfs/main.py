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

import click
import debianbts as bts
from debianrfs import bug, math
from debianrfs.cache import Cache


@click.command()
@click.option("--archived/--no-archived", default=False, help="Include archived bugs.")
@click.option(
    "--close-method",
    type=click.Choice(["bug", "upload"], case_sensitive=False),
    default="upload",
    help="The way the close date of RFS bugs are determined.",
)
@click.option(
    "--cache/--no-cache",
    "cache_enabled",
    default=True,
    help="Cache bugs for future analysis.",
)
@click.option("--cache-db", help="Location of sqlite3 cache database.")
def main(archived: bool, close_method: str, cache_enabled: bool, cache_db: str | None):
    """Calculate statistics regarding sponsorship requests."""

    bugs = bts.get_bugs(
        package="sponsorship-requests",
        status="done",
        archive="both" if archived else "0",
    )

    if cache_enabled:
        cache = Cache(cache_db)

    total = len(bugs)
    click.echo(f"{total} closed RFS bugs found")

    def waiting_period_map(bug_id, index):
        d = (
            cache.cached_waiting_period(bug_id, close_method)
            if cache_enabled and cache
            else bug.waiting_period(bug_id, close_method)
        )
        click.echo(f"[{round((index+1)/total*100)}%] processed bug#{bug_id}")
        return d

    def waiting_period_filter(x):
        return x != None

    waiting_periods_all = [waiting_period_map(x, i) for i, x in enumerate(bugs)]
    waiting_periods: list[int] = list(
        filter(waiting_period_filter, waiting_periods_all)
    )

    waiting_periods.sort()

    click.echo("\n\n\n=== RESULTS ===")
    click.echo("RFS waiting period (days)")
    click.echo("\nWith outliers")
    click.echo(f"Average: {math.average(waiting_periods)}")
    click.echo(f"Median: {math.median(waiting_periods)}")
    click.echo(f"Lower quartile: {math.lower_quartile(waiting_periods)}")
    click.echo(f"Upper quartile: {math.upper_quartile(waiting_periods)}")
    click.echo(f"IQR: {math.interquartile_range(waiting_periods)}")
    click.echo(f"Min: {waiting_periods[0]}")
    click.echo(f"Max: {waiting_periods[-1]}")

    waiting_periods = list(
        filter(math.filter_outliers(waiting_periods), waiting_periods)
    )
    waiting_periods.sort()

    click.echo("\nWithout outliers")
    click.echo(f"Average: {math.average(waiting_periods)}")
    click.echo(f"Median: {math.median(waiting_periods)}")
    click.echo(f"Lower quartile: {math.lower_quartile(waiting_periods)}")
    click.echo(f"Upper quartile: {math.upper_quartile(waiting_periods)}")
    click.echo(f"IQR: {math.interquartile_range(waiting_periods)}")
    click.echo(f"Min: {waiting_periods[0]}")
    click.echo(f"Max: {waiting_periods[-1]}")

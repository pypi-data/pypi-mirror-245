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

import platformdirs
import sqlite3
import os.path

from debianrfs.bug import waiting_period


class Cache:
    def __init__(self, cache_db: str | None) -> None:
        db_path = (
            cache_db
            if cache_db
            else os.path.join(
                platformdirs.user_cache_dir("debian-rfs-stats"), "cache.db"
            )
        )
        if not os.path.exists(os.path.dirname(db_path)):
            os.mkdir(os.path.dirname(db_path))
        self.conn = sqlite3.connect(db_path)
        cur = self.conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS cached_waiting_periods(bug_id, close_method, delta)"
        )
        cur.close()

    def cached_waiting_period(self, bug_id, close_method):
        """Calculate duration from submission of bug to when bug is completed in
        days, querying the cache first when doing so."""
        cur = self.conn.cursor()
        results = cur.execute(
            "SELECT delta FROM cached_waiting_periods WHERE bug_id = ? AND close_method = ?",
            (bug_id, close_method),
        ).fetchone()
        if results != None:
            cur.close()
            return results[0]
        else:
            delta = waiting_period(bug_id, close_method)
            cur.execute(
                "INSERT INTO cached_waiting_periods VALUES (?, ?, ?)",
                (bug_id, close_method, delta),
            )
            self.conn.commit()
            cur.close()
            return delta

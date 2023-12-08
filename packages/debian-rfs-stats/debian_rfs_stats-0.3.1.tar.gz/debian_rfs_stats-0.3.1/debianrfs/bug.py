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

from click import echo
import debianbts as bts
from datetime import datetime, timezone
from email.message import Message
from debianrfs.entry import get_recipient_email_addr, get_date
from debianrfs.uploads import package_first_upload, package_uploads


def bug_opened(bug_id) -> datetime:
    """Determine datetime when bug was submitted"""
    bug_status = bts.get_status([bug_id])[0]
    return bug_status.date.replace(tzinfo=timezone.utc)


def bug_closed(bug_id) -> datetime:
    """Determine datetime when bug was closed"""
    bug_log = bts.get_bug_log(bug_id)
    for entry in bug_log:
        message = entry["message"]
        if not isinstance(message, Message):
            raise TypeError(
                f"message property of bug#{bug_id} not an instance of Message"
            )
        address = get_recipient_email_addr(message)
        if address.endswith("-done@bugs.debian.org"):
            echo(f"found done message of bug#{bug_id}")
            return get_date(message)
        if address.endswith("-close@bugs.debian.org"):
            # -close is alias of -done, need to check as well
            echo(f"found close message of bug#{bug_id}")
            return get_date(message)
    # it was closed with an email to control@b.d.o (or Control pseudo-header),
    # use log_modified as fallback
    echo(f"falling back to log_modified date for bug#{bug_id}")
    bug_status = bts.get_status([bug_id])[0]
    return bug_status.log_modified.replace(tzinfo=timezone.utc)


def waiting_period(bug_id, close_method):
    """Calculate duration from submission of bug to when bug is completed in days"""
    opened = bug_opened(bug_id)
    if close_method == "bug":
        closed = bug_closed(bug_id)
    elif close_method == "upload":
        pkg = bts.get_status([bug_id])[0].subject.split(" ")[1].split("/")[0]
        upload = package_first_upload(package_uploads(pkg), opened)
        if not upload:
            return None
        closed = upload.date
    else:
        raise ValueError("Invalid close_method passed")
    delta = closed - opened
    return delta.days

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
#
# This file is inspired by the who-uploads bash script (in the devscripts
# Debian package).

import re
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timezone
import gnupg


def package_prefix(package: str) -> str:
    """Determine the prefix of a given package"""
    if package.startswith("lib"):
        return package[0:3]
    else:
        return package[0]


def extract_version(title: str):
    """Extract version from RSS feed title"""
    return title.split(" ")[1]


def parse_rss_date(date: str) -> datetime:
    """Parses date from RSS feed into datetime"""
    return datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z").replace(
        tzinfo=timezone.utc
    )


SIGNED_MESSAGE_REGEX = re.compile(
    r"(-----BEGIN PGP SIGNED MESSAGE-----[\S\s]+-----END PGP SIGNATURE-----)"
)


class PackageUpload:
    def __init__(self, version: str, date: datetime, url: str):
        self.version = version
        self.date = date
        self.url = url

    def uploader(self):
        html = requests.get(self.url).text.replace("&lt;", "<").replace("&gt;", ">")
        match = SIGNED_MESSAGE_REGEX.search(html)
        if not match:
            return None
        news_text: str = match.groups()[0]

        gpg = gnupg.GPG()
        v: gnupg.Verify = gpg.verify(news_text)
        if not v.key_id:
            return None
        key_id: str = v.key_id

        pub_key_text: str = requests.get(
            f"https://keyring.debian.org/pks/lookup?op=get&search=0x{key_id}"
        ).text
        key: gnupg.ScanKeys = gpg.scan_keys_mem(pub_key_text)

        return key.uids


def package_uploads(package: str):
    """Fetch the list of accepted uploads for a given package"""

    prefix = package_prefix(package)
    news_url = f"https://packages.qa.debian.org/{prefix}/{package}/news.rss20.xml"
    news_text = requests.get(news_url).text

    channel = BeautifulSoup(news_text, "xml").channel
    if not isinstance(channel, Tag):
        return None

    news = channel.find_all("item")

    def news_item_filter_accepted(news_item):
        return news_item.title.text.startswith("Accepted")

    uploads = list(filter(news_item_filter_accepted, news))
    uploads = [
        # {
        #     "version": extract_version(x.title.text),
        #     "date": parse_rss_date(x.pubDate.text),
        #     "url": x.link.text,
        # }
        PackageUpload(
            extract_version(x.title.text), parse_rss_date(x.pubDate.text), x.link.text
        )
        for _, x in enumerate(uploads)
    ]

    def sort_key(upload: PackageUpload):
        return upload.date

    uploads.sort(key=sort_key)

    return uploads


def package_first_upload(uploads: list[PackageUpload] | None, date: datetime):
    """Determine the first upload of a package since a given date"""
    if uploads == None:
        return None
    for upload in uploads:
        if upload.date >= date:
            return upload
    return None

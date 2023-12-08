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

import requests
import re

DEBIAN_VERSION_REGEX = re.compile(r"debian_mangled_uversion:\ <b>(.+)<\/b>")
UPSTREAM_VERSION_REGEX = re.compile(r"upstream_version:\ <b>(.+)<\/b>")


def package_versions(pkg: str) -> dict[str, str]:
    page_text = requests.get(f"https://qa.debian.org/cgi-bin/watch?pkg={pkg}").text

    match = DEBIAN_VERSION_REGEX.search(page_text)
    if not match:
        raise ValueError("No debian mangled version found")
    debian_version = match.groups()[0]

    match = UPSTREAM_VERSION_REGEX.search(page_text)
    if not match:
        raise ValueError("No upstream version found")
    upstream_version = match.groups()[0]
    return {"debian": debian_version, "upstream": upstream_version}

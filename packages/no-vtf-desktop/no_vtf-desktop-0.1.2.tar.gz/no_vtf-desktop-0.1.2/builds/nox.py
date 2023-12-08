# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import subprocess
import sys

from typing import NoReturn


def main() -> NoReturn:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "--quiet",
            "--no-input",
            "--disable-pip-version-check",
            "install",
            "--no-warn-script-location",
            "nox",
        ],
        check=True,
    )

    os.execl(sys.executable, sys.argv[0], "-m", "nox", *sys.argv[1:])


if __name__ == "__main__":
    main()

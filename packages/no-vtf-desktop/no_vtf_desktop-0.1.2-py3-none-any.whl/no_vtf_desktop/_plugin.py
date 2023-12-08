# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib

import filelock

import no_vtf_desktop.installation


def pre_main() -> None:
    with contextlib.suppress(filelock.Timeout):
        no_vtf_desktop.installation.integrate(
            lock_timeout=0,
        )

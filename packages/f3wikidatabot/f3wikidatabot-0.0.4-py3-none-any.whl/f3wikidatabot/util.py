# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import subprocess

log = logging.getLogger(__name__)


def sh_bool(command):
    try:
        sh(command)
        return True
    except subprocess.CalledProcessError:
        return False


def sh(command, input=None):
    log.debug(":sh: " + command)
    if input is None:
        stdin = None
    else:
        stdin = subprocess.PIPE
    proc = subprocess.Popen(
        args=command,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        bufsize=1,
    )
    if stdin is not None:
        proc.stdin.write(input.encode("ascii", "ignore"))
        proc.stdin.close()
    lines = []
    with proc.stdout:
        for line in iter(proc.stdout.readline, b""):
            line = line.decode("utf-8", "ignore")
            lines.append(line)
            log.debug(line.strip().encode("ascii", "ignore"))
    if proc.wait() != 0:
        raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=command)
    return "".join(lines)

# -*- mode: python; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess

import pytest

from f3wikidatabot import util


class TestUtil(object):
    def test_sh(self):
        assert "A" == util.sh("echo -n A")
        with pytest.raises(Exception) as excinfo:
            util.sh("exit 123")
        assert excinfo.value.returncode == 123

    def test_sh_progress(self, caplog):
        util.sh("echo AB ; sleep 5 ; echo C")
        records = caplog.records
        assert ":sh: " in records[0].message
        assert "b'AB'" == records[1].message
        assert "b'C'" == records[2].message

    def test_sh_input(self, caplog):
        assert "abc" == util.sh("cat", "abc")

    def test_sh_fail(self, caplog):
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            util.sh("/bin/echo -n AB ; /bin/echo C ; exit 111")
        assert excinfo.value.returncode == 111

        for record in caplog.records:
            if record.levelname == "ERROR":
                assert "replay full" in record.message or "ABC\n" == record.message

    def test_sh_bool__returns_true_on_exit_code_zero(self):
        assert True is util.sh_bool("true")

    def test_sh_bool__returns_false_on_non_zero_exit_code(self):
        assert False is util.sh_bool("false")

    def test_sh__returns_empty_string(self):
        assert "" == util.sh("true")

    def test_sh__handles_utf8(self):
        assert "€" == util.sh("echo -n €")

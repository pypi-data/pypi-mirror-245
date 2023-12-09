#!/usr/bin/env python

"""Dowload tests for `ta_bitwarden_cli` package."""

import pytest
import os

from pathlib import Path
from ta_bitwarden_cli import download_bitwarden as db


class TestDownload:
    """
    Test different bitwarden cli download methods
    """

    def teardown_method(self):
        Path(self.path).unlink(missing_ok=True)

    def test_incorrect_source(self):
        self.path = os.path.join(os.getcwd(), "bw")
        with pytest.raises(Exception) as e:
            db.DownloadBitwarden.download_bitwarden("incorrect")
        assert "Unknown download source" in str(e)

    def test_default(self):
        self.path = db.DownloadBitwarden.download_bitwarden()
        assert os.path.exists(self.path)
        assert round(Path(self.path).stat().st_size / 1024 / 1024) > 10

    def test_site(self):
        self.path = db.DownloadBitwarden.download_bitwarden("site")
        assert os.path.exists(self.path)
        assert round(Path(self.path).stat().st_size / 1024 / 1024) > 10

    def test_github(self):
        self.path = db.DownloadBitwarden.download_bitwarden("github")
        assert os.path.exists(self.path)
        assert round(Path(self.path).stat().st_size / 1024 / 1024) > 10

    def test_local(self):
        self.path = db.DownloadBitwarden.download_bitwarden("local")
        assert os.path.exists(self.path)
        assert round(Path(self.path).stat().st_size / 1024 / 1024) > 10

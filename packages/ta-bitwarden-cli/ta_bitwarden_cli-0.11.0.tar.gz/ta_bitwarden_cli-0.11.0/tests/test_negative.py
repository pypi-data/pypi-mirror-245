#!/usr/bin/env python

"""Negative tests for `ta_bitwarden_cli` package."""

import pytest
import os

from ta_bitwarden_cli import ta_bitwarden_cli as ta
from ta_bitwarden_cli import download_bitwarden as db
from ta_bitwarden_cli.ta_bitwarden_cli import BitwardenServerException


class TestNegative:
    """
    For succesfull execution you need to have such env vars with valid values available in your system:
      - BW_PASSWORD
      - BW_CLIENTID
      - BW_CLIENTSECRET
    """

    @classmethod
    def setup_class(cls):
        db.DownloadBitwarden.download_bitwarden()
        cls.bw = None
        cls.og_environ = os.environ.copy()

    def setup_method(self):
        os.environ.update(self.og_environ)

    def teardown_method(self):
        self.bw.bitwarden_exe("logout")

    def test_invalid_client_info(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": "123",
            "client_secret": "abc",
        }

        self.bw = ta.Bitwarden(bitwarden_credentials)
        with pytest.raises(ValueError) as e:
            self.bw.bitwarden_login()

        assert "Invalid bitwarden client_id or client_secret!" in str(e)

    def test_invalid_master_password(self):
        bitwarden_credentials = {
            "password": "invalid_password",
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }

        self.bw = ta.Bitwarden(bitwarden_credentials)
        with pytest.raises(ValueError) as e:
            self.bw.bitwarden_login()

        assert "Invalid master password!" in str(e)

    def test_invalid_collection(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        items = {
            "test": "invalid_collection",
        }
        self.bw = ta.Bitwarden(bitwarden_credentials)
        self.bw.bitwarden_login()
        with pytest.raises(BitwardenServerException) as e:
            self.bw.get_credentials(items)

        assert "Invalid bitwarden collection or key name or no access to collection for this user!" in str(e)
        assert "invalid_collection" in str(e)

    def test_valid_collection_no_otp(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        items = {
            "test": "Dependency bot",
        }
        self.bw = ta.Bitwarden(bitwarden_credentials)
        self.bw.bitwarden_login()
        self.bw.get_credentials(items)

        assert self.bw.data["test"]["otp"] == ""

    def test_invalid_attachment_file(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        items = {
            "test": "The Python Package Index",
        }

        self.bw = ta.Bitwarden(bitwarden_credentials)
        self.bw.bitwarden_login()
        with pytest.raises(ValueError) as e:
            self.bw.get_attachment(items["test"], "invalid_att.eol")

        assert "Attachment was not found!" in str(e)

    def test_invalid_attachment_item(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        items = {
            "test": "invalid_item",
        }

        self.bw = ta.Bitwarden(bitwarden_credentials)
        self.bw.bitwarden_login()
        with pytest.raises(Exception) as e:
            self.bw.get_attachment(items["test"], "att.txt")

        assert "Cannot find bitwarden item" in str(e)
        assert "invalid_item" in str(e)

    def test_two_attachment_items(self):
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        items = {
            "test": "Test_item Password Reset",
        }

        self.bw = ta.Bitwarden(bitwarden_credentials)
        self.bw.bitwarden_login()
        with pytest.raises(Exception) as e:
            self.bw.get_attachment(items["test"], "att.txt")

        assert "More than one result for item name was found" in str(e)

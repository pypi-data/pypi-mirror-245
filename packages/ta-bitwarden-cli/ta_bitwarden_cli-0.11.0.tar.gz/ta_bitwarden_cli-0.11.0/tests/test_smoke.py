#!/usr/bin/env python

"""Smoke tests for `ta_bitwarden_cli` package."""
import os
import re
import shutil

from ta_bitwarden_cli import ta_bitwarden_cli as ta
from ta_bitwarden_cli import download_bitwarden as db


class TestSmoke:
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

    def teardown_class(cls):
        shutil.rmtree("test_folder", ignore_errors=True)
        try:
            os.remove("ta-bitwarden-cli.log")
            os.remove("att.txt")
        except FileNotFoundError:
            pass

    def teardown_method(self):
        self.bw.bitwarden_exe("logout")

    def setup_method(self):
        os.environ.update(self.og_environ)
        bitwarden_credentials = {
            "password": os.getenv("BW_PASSWORD"),
            "client_id": os.getenv("BW_CLIENTID"),
            "client_secret": os.getenv("BW_CLIENTSECRET"),
        }
        self.bw = ta.Bitwarden(bitwarden_credentials)

    def test_logs_path(self):
        self.bw.bitwarden_exe("logout")
        assert os.path.exists("ta-bitwarden-cli.log")

    def test_exe(self):
        self.bw.bitwarden_exe("logout")
        app = self.bw.bitwarden_exe("logout")
        assert app.stderr == "You are not logged in."

    def test_login(self):
        self.bw.bitwarden_login()
        assert len(self.bw.session_key) > 80

    def test_get_data(self):
        items = {
            "test": "The Python Package Index",
            "aws": "Robocorp CodeArtifact AWS Role (PRD)",
        }
        self.bw.bitwarden_login()
        self.bw.get_data(items)
        assert self.bw.data["test"]["login"] == "thoughtfulautomation"
        assert self.bw.data["aws"]["domain"] == "thoughtful-automation"

    def test_get_data_with_otp(self):
        items = {
            "okta": "896b5777-f525-42aa-8035-adf10145021b",
        }
        self.bw.bitwarden_login()
        self.bw.get_data(items)
        assert re.match(r"\d+", self.bw.data["okta"]["otp"])

    def test_get_credentials(self):
        items = {
            "test": "The Python Package Index",
        }
        assert self.bw.get_credentials(items)["test"]["login"] == "thoughtfulautomation"

    def test_get_credentials_substring_name(self):
        items = {
            "test": "The Python Package Index",
        }
        assert self.bw.get_credentials(items)["test"]["name"] == "The Python Package Index"

    def test_get_attachment(self):
        items = {
            "test": "The Python Package Index",
        }
        self.bw.bitwarden_login()
        self.bw.get_attachment(items["test"], "att.txt")
        f = open("att.txt", "r")
        assert f.read() == "secret text\n"

    def test_get_attachment_to_folder(self):
        items = {
            "test": "The Python Package Index",
        }
        self.bw.bitwarden_login()
        self.bw.get_attachment(items["test"], "att.txt", f"{os.getcwd()}/test_folder")
        f = open("test_folder/att.txt", "r")
        assert f.read() == "secret text\n"

    def test_generate_new_password(self):
        self.bw.bitwarden_login()
        new_pass = self.bw.generate_new_password(length=12)
        assert len(new_pass) == 12

    def test_generate_new_password_and_update_item(self):
        self.bw.bitwarden_login()
        items = {
            "test": "Test_item Password Reset",
        }
        creds = self.bw.get_credentials(items)
        new_pass = self.bw.generate_new_password(length=12, update_item=True, item_id=creds["test"]["id"])
        assert self.bw.get_credentials(items)["test"]["password"] == new_pass

    def test_list_items_with_filters(self):
        self.bw.bitwarden_login()
        filter = {
            "collectionid": "5249c92b-b9f8-4385-aeee-ab96010b7840",
            "search": "Test",
        }
        assert len(self.bw.list("items", filter=filter)) >= 1

    def test_list_collections(self):
        self.bw.bitwarden_login()
        assert len(self.bw.list("collections")) >= 1

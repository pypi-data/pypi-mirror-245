import os
import re
import json
import logging
import subprocess

from subprocess import TimeoutExpired
from retry import retry

from .download_bitwarden import DownloadBitwarden


logger = logging.getLogger("ta-bitwarden-cli")


class BwErrorSamples:
    MULTI_RESULTS = (
        "More than one result was found. Try getting a specific object by "
        "`id` instead. The following objects were found:"
    )


class BitwardenServerException(Exception):
    pass


class RateLimitException(Exception):
    pass


class Bitwarden(object):
    """
    Main class that does all work
    """

    def __init__(self, bitwarden_credentials=None):
        """
        bitwarden_credentials - dict with 'password' / 'client_id' / 'client_secret' keys
        'bw' binary should be already in PATH
        """
        self.data = {}
        self.path_to_exe_file = "bw"
        self.session_key = ""

        if bitwarden_credentials:
            bitwarden_keys = ["client_id", "client_secret", "password"]
            if all(k in bitwarden_credentials.keys() for k in bitwarden_keys):
                os.environ["BW_CLIENTID"] = bitwarden_credentials["client_id"]
                os.environ["BW_CLIENTSECRET"] = bitwarden_credentials["client_secret"]
                self.bw_password = bitwarden_credentials["password"]
            else:
                raise ValueError("Missing client_id, client_secret, or password")
        else:
            if all(
                (
                    os.environ.get("BW_CLIENTID"),
                    os.environ.get("BW_CLIENTSECRET"),
                    os.environ.get("BW_PASSWORD"),
                )
            ):
                logger.info("no bitwarden credentials, using environment variables")
                self.bw_password = os.environ["BW_PASSWORD"]
            else:
                ValueError("No bitwarden credentials provided or in environment variables")
        self.bitwarden_get_version()

    @retry(RateLimitException, delay=65, tries=2, logger=logger)
    def bitwarden_exe(self, *command, input=None):
        """
        Provide coma-separated command line arguments that you want to provide to bw CLI binary
        Searches binary in PATH. If fails tries to run it from current working directory
        Examples:
          - bw.bitwarden_exe('logout')
          - bw.bitwarden_exe(
            "unlock",
            self.bw_password,
            "--raw",
            )
        :param input: payload to be sent to the command
        """
        strings_to_replace = [
            self.session_key,
            self.bw_password,
            os.environ.get("BW_CLIENTID"),
            os.environ.get("BW_CLIENTSECRET"),
            os.environ.get("BW_PASSWORD"),
        ]
        deducted_command = " ".join(tuple("<DEDUCTED>" if item in strings_to_replace else item for item in command))
        logger.debug(f"bw {deducted_command}")

        try:
            app = subprocess.run(
                [
                    self.path_to_exe_file,
                    *command,
                ],
                capture_output=True,
                input=input,
                text=True,
                timeout=180,
                env=os.environ,
            )
        except FileNotFoundError:
            self.path_to_exe_file = DownloadBitwarden.download_bitwarden()
            app = subprocess.run(
                [
                    self.path_to_exe_file,
                    *command,
                ],
                capture_output=True,
                input=input,
                text=True,
                timeout=180,
                env=os.environ,
            )

        if app.returncode != 0 and "Slow down!" in app.stderr:
            raise RateLimitException("Too many requests. Trying again in 1m...")

        return app

    def bitwarden_logout(self):
        return self.bitwarden_exe("logout")

    def bitwarden_get_version(self):
        app = self.bitwarden_exe("--version")
        logger.debug(f"STDOUT: {app.stdout.strip()}")

    @retry((TimeoutExpired, BitwardenServerException), delay=5, tries=3, logger=logger)
    def bitwarden_login(self):
        """
        Performs login opeartion via BitWarden CLI
        Requires password / client_id / client_secret already set when creation Bitwarden instance
        """
        self.bitwarden_logout()

        bitwarden_app = self.bitwarden_exe(
            "login",
            "--apikey",
        )

        if bitwarden_app.returncode == 0:
            logger.info(bitwarden_app.stdout.splitlines()[0])
            bitwarden_app = self.bitwarden_exe(
                "unlock",
                self.bw_password,
                "--raw",
            )

            if bitwarden_app.returncode == 0:
                self.session_key = bitwarden_app.stdout
            else:
                logger.error(f"STDOUT: {bitwarden_app.stdout}")
                logger.error(f"STDERR: {bitwarden_app.stderr}")
                raise ValueError("Invalid master password!")
        else:
            logger.error(f"STDOUT: {bitwarden_app.stdout}")
            logger.error(f"STDERR: {bitwarden_app.stderr}")
            raise ValueError("Invalid bitwarden client_id or client_secret!")

    def sync(self):
        bitwarden_app = self.bitwarden_exe(
            "sync",
            "--session",
            self.session_key,
        )

        if bitwarden_app.returncode != 0 or bitwarden_app.stdout != "Syncing complete.":
            logger.error(f"STDOUT: {bitwarden_app.stdout}")
            logger.error(f"STDERR: {bitwarden_app.stderr}")
            raise RuntimeError("Unable to sync bitwarden")

    def get_credentials(self, user_credentials_name):
        """
        This method is for backward compatibility
        """
        self.bitwarden_login()
        self.get_data(user_credentials_name)
        return self.data

    @retry((TimeoutExpired, BitwardenServerException), delay=5, tries=3, logger=logger)
    def get_data(self, data):
        """
        Core method
        Obtaining of data from bitwarden vault for provided Key Name
        Saves dict with results to self.data variable
        Each key in dict is your custom name
        Each value in dict is another dict with data from bitwarden vault

        Example:

          items = {
              "unicourt_api": "UniCourt API",
              "unicourt_alpha_api": "UniCourt Alpha API Dev Portal",
              "aws": "AWS Access Key & S3 Bucket",
          }
          bw.get_data(items)
          assert isinstance(bw.data['aws'],dict)
        """
        logger.info("Syncing bitwarden data...")
        bitwarden_app = self.bitwarden_exe(
            "sync",
            "--session",
            self.session_key,
        )

        logger.info("Getting bitwarden data...")
        if bitwarden_app.stdout != "Syncing complete.":
            logger.error(f"STDOUT: {bitwarden_app.stdout}")
            logger.error(f"STDERR: {bitwarden_app.stderr}")
            logger.warning("Unable to sync bitwarden")

        for credentials_key, credentials_name in data.items():
            command = ["get", "item", credentials_name, "--session", self.session_key]
            bitwarden_app = self.bitwarden_exe(*command)
            if bitwarden_app.returncode != 0 or bitwarden_app.stdout == "":
                logger.error(f"STDOUT: {bitwarden_app.stdout}")
                logger.error(f"STDERR: {bitwarden_app.stderr}")

                if BwErrorSamples.MULTI_RESULTS in bitwarden_app.stderr:
                    logger.info("attempting to parse and request IDs")
                    item_id_re = r"((?:[\d\w]+-){4}[\d\w]+)"
                    item_ids = re.findall(item_id_re, bitwarden_app.stderr)
                    if item_ids:
                        for item_id in item_ids:
                            command = [
                                "get",
                                "item",
                                item_id,
                                "--session",
                                self.session_key,
                            ]
                            bitwarden_app = self.bitwarden_exe(*command)
                            item_dict = self._parse_credential_response(bitwarden_app.stdout, credentials_key)
                            if item_dict["name"] == credentials_name or item_dict["id"] == credentials_name:
                                self.data[credentials_key] = item_dict
                                break
                            # if item
                        else:
                            raise BitwardenServerException(f"Failed to udentify exact match for  {credentials_name=}")
                else:
                    raise BitwardenServerException(
                        f"Invalid bitwarden collection or key name or no access to collection for this user! "
                        f"{credentials_name=} not found"
                    )

            item_dict = self._parse_credential_response(bitwarden_app.stdout, credentials_key)
            self.data[credentials_key] = item_dict

    def _parse_credential_response(self, bitwarden_stdout: str, credentials_key):
        bw_item = json.loads(bitwarden_stdout)
        item = {
            "id": bw_item["id"],
            "name": bw_item["name"],
            "login": bw_item["login"]["username"],
            "password": bw_item["login"]["password"],
            "url": bw_item["login"]["uris"][0]["uri"] if "uris" in bw_item["login"] else "",
        }

        if bw_item["login"]["totp"] is None:
            item["otp"] = ""
        else:
            bitwarden_app = self.bitwarden_exe(
                "get",
                "totp",
                bw_item["id"],
                "--session",
                self.session_key,
            )
            item["otp"] = bitwarden_app.stdout

        if "fields" in bw_item:
            for field in bw_item["fields"]:
                item[field["name"]] = field["value"]

        return item

    @retry((TimeoutExpired, BitwardenServerException), delay=5, tries=3, logger=logger)
    def get_attachment(self, item_name, file_name, output_folder=os.getcwd()):
        """
        Downloads attachment file from particular item to current working directory
        Item name should be unique
        File name should be unique
        Output folder path is absolute

        Example:

            items = {
                "test": "pypi.org",
            }
            self.bw.bitwarden_login()
            self.bw.get_attachment(items["test"], "att.txt")
            f = open("att.txt", "r")
            assert f.read() == "secret text\n"
        """
        if not isinstance(item_name, str) or not isinstance(file_name, str) or not isinstance(output_folder, str):
            raise TypeError("item_name / file_name / output_folder should be strings!")

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        logger.info("Syncing bitwarden data...")
        self.bitwarden_exe(
            "sync",
            "--session",
            self.session_key,
        )

        # Get item ID
        bitwarden_app = self.bitwarden_exe(
            "get",
            "item",
            item_name,
            "--session",
            self.session_key,
        )

        if bitwarden_app.returncode != 0:
            logger.error(f"STDOUT: {bitwarden_app.stdout}")
            logger.error(f"STDERR: {bitwarden_app.stderr}")
            if "A 404 error occurred while downloading the attachment" in bitwarden_app.stderr:
                raise BitwardenServerException("404 HTTP from bitwarden server occurred!")
            if "More than one result was found" in bitwarden_app.stderr:
                raise ValueError("More than one result for item name was found! Name should be unique!")
            if "Not found" in bitwarden_app.stderr:
                raise ValueError(f"Cannot find bitwarden item '{str(item_name)}'! Check the name")
            raise RuntimeError("Unknown error during items obtaining!")

        bitwarden_items = json.loads(bitwarden_app.stdout)
        item_id = str(bitwarden_items["id"])

        bitwarden_app = self.bitwarden_exe(
            "get",
            "attachment",
            file_name,
            "--itemid",
            item_id,
            "--session",
            self.session_key,
            "--output",
            os.path.join(output_folder, file_name),
        )

        if bitwarden_app.stderr:
            logger.error(f"STDOUT: {bitwarden_app.stdout}")
            logger.error(f"STDERR: {bitwarden_app.stderr}")
            if "More than one result was found" in bitwarden_app.stderr:
                raise ValueError("More than one result for item name was found! Name should be unique!")
            if "was not found" in bitwarden_app.stderr:
                raise ValueError("Attachment was not found!")

            raise RuntimeError("Unknown error during attachment downloading!")

        logger.info(f"Attachment '{file_name}' downloaded sucessfully!")

    def generate_new_password(
        self, length: int = 8, allowed_characters: str = "lusn", update_item: bool = False, item_id: str = ""
    ) -> str:
        """
        Generates a new password using Bitwarden CLI.
        Optionally update the item in Bitwarden with the new password (requires item_id)
        :param length: Length of the password
        :param allowed_characters: Allowed characters (l = lowercase, u = uppercase, s = special, n = numbers)
        :param update_item: Update the password in the item
        :param item_id: ID of the item to update
        :return: The new password
        """
        bitwarden_app = self.bitwarden_exe(
            "generate", f"-{allowed_characters}", "--length", str(length), "--session", self.session_key
        )
        new_password = bitwarden_app.stdout
        if update_item:
            self.update_item_password(item_id, new_password)
        return new_password

    def update_item_password(self, item_id: str, new_pass: str):
        """
        Updates the password in a Bitwarden item
        :param item_id: ID of the item to update
        :param new_pass: New password
        :return: The new password
        """
        if not item_id:
            raise ValueError("Item ID is required to update the item's password")
        try:
            # Get item from Bitwarden
            get_entity = self.bitwarden_exe("get", "item", item_id, "--session", self.session_key)
            entity_data = json.loads(get_entity.stdout)

            # Update password in JSON object
            entity_data["login"]["password"] = new_pass

            # Encode JSON object

            encoded_data = self.bitwarden_exe("encode", input=json.dumps(entity_data))

            # Update item in Bitwarden
            edit_entity = self.bitwarden_exe(
                "edit", "item", item_id, "--session", self.session_key, input=encoded_data.stdout
            )
            if edit_entity.stderr:
                raise RuntimeError(edit_entity.stderr)
            output_json = json.loads(edit_entity.stdout)

            logger.info("Password updated in Bitwarden")
        except Exception as e:
            raise RuntimeError(f"Error updating password in Bitwarden: {e}")
        return output_json["login"]["password"]

    def list(self, object_type: str = "items", filter: dict = None) -> dict:
        """
        List objects from Bitwarden
        :param object_type: Type of object to list (items, collections, folders, etc)
        :param filter: Dictionary of filters to apply
            Examples:
                filter = {
                    "collectionid": "2126163c-47e1-463f-9ed4-b09e00f6f367",
                }

                Search is also supported:

                filter = {
                    "collectionid": "2126163c-47e1-463f-9ed4-b09e00f6f367",
                    "search": "Test",
                }

        :return: Dictionary of objects
        """
        filters = ()
        if filter:
            for key, value in filter.items():
                filters += ("--" + key, value)

        bitwarden_app = self.bitwarden_exe("list", object_type, "--session", self.session_key, *filters)
        if bitwarden_app.stderr:
            if "Unknown object" in bitwarden_app.stderr:
                raise ValueError(bitwarden_app.stderr)
            raise RuntimeError(bitwarden_app.stderr)
        return json.loads(bitwarden_app.stdout)

"""Interface for logging to Google Sheets.

Target Google Sheets MUST GIVE EDITOR ACCESS to service account email where the
Service Account API came from.
"""

from dataclasses import dataclass
import logging
import os

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource

load_dotenv()

# If modifying these scopes, delete the file token.json.
# This is read and write access.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheets:
    def __init__(self, sheet_id: str = None) -> None:
        """Initialize Google Sheets interface.

        Args:
            sheet_id (str, optional): Sheet ID. Found in the URL. Defaults to
            None.
        """
        self.__sheets_range = os.getenv("SHEETS_RANGE_NAME")
        self.__spreadsheet_id = sheet_id or os.getenv("SHEETS_ID")
        self.__cred_file = os.getenv("SHEETS_CRED_FILE")

    def append_row(self, row_data: list[any]) -> None:
        """Write data to Google Sheets."""
        service: Resource = self.__build_service()
        service.spreadsheets().values().append(
            spreadsheetId=self.__spreadsheet_id,
            range=self.__sheets_range,
            # How the input data should be interpreted.
            # RAW - As-is
            # USER_ENTERED - Like user typed into the UI.
            #     Numbers as numbers, strings maybe converted to numbers, dates, etc.
            valueInputOption="USER_ENTERED",
            # INSERT_ROWS or OVERWRITE
            insertDataOption="INSERT_ROWS",
            # Must be in `{"values": [["First row"], ["Second row"]]}`
            body={"values": [row_data]},
        ).execute()

    def __build_service(self) -> Resource:
        creds = self.__handle_auth()
        return build("sheets", "v4", credentials=creds)

    def __handle_auth(self) -> Credentials:
        """Authenticate with Google Sheets using service account."""
        credentials = Credentials.from_service_account_file(self.__cred_file)
        scoped_credentials = credentials.with_scopes(SCOPES)
        logging.info(scoped_credentials)
        return scoped_credentials

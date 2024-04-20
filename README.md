# google_sheets

Use Google Sheets Python API to control a Google Sheet.

## Getting started

1. Create or use Google Cloud project.
1. Enable the _Sheets API_.
1. Create a Service Account.
1. Create credentials file for Service Account.
1. Rename credentials file to `credentials.json` and place in `keys/` directory.
1. Copy `.env.example` file to `.env`.
1. Add Google Sheet ID and a range to the `.env` file.
1. Give target Sheet access to the Service Account email in the Google Sheet.
1. Example implementation

   ```python
   row_data = ["My data", "100", "04-20-2024"]
   sheets = Sheets()
   sheets.append_row(row_data)
   ```

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from settings import config


# Authenticate with the Google API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

sheet = gc.open(config.GOOGLE_SHEET_TITLE)


async def update_sheet(sheet_name, *args):
    worksheet = sheet.worksheet(sheet_name)
    insert_row = args
    worksheet.insert_row(insert_row, 2)

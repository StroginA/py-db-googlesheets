from decimal import ROUND_HALF_EVEN, Decimal as D, setcontext, Context

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pycbrf import ExchangeRates

from datetime import date

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '13tzDdsy5xPXmv-8Ew9OSM51vPl3Xlwo2Bz80XZxyry4'
RANGE_NAME = 'A2:D'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    setcontext(Context(rounding=ROUND_HALF_EVEN))
    exchange_rate = ExchangeRates(date.today(), locale_en=True)['USD'].value
    print(exchange_rate)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        output = []
        for row in values:
            order_id = int(row[1])
            cost_USD = D(row[2])
            cost_RUB = D(row[2])*exchange_rate
            cost_RUB = cost_RUB.quantize(D(10)**-2)
            delivery_date = row[3].split('.')
            delivery_date = date(int(delivery_date[2]),int(delivery_date[1]),int(delivery_date[0]))
            output.append((order_id, cost_USD, cost_RUB, delivery_date))
            print(output)
    except HttpError as err:
        print(err)

def fetch():
    """
    Queries the test sheet for data, adds cost conversion to RUB and outputs a list of formatted row tuples.
    Output:
    [
        (
            order_id: integer,
            cost_USD: Decimal(),
            cost_RUB: Decimal(),
            delivery_date: datetime.date()
        )
    ]
    """

    setcontext(Context(rounding=ROUND_HALF_EVEN))
    exchange_rate = ExchangeRates(date.today(), locale_en=True)['USD'].value

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets.readonly'])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/spreadsheets.readonly'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId='13tzDdsy5xPXmv-8Ew9OSM51vPl3Xlwo2Bz80XZxyry4',
                                    range='A2:D').execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        output = []
        for row in values:
            order_id = int(row[1])
            cost_USD = D(row[2])
            cost_RUB = D(row[2])*exchange_rate
            cost_RUB = cost_RUB.quantize(D(10)**-2)
            delivery_date = row[3].split('.')
            delivery_date = date(int(delivery_date[2]),int(delivery_date[1]),int(delivery_date[0]))
            output.append((order_id, cost_USD, cost_RUB, delivery_date))
        
        return output
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
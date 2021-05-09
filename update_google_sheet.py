"""Fetch orders from ebay and paste their trackings to google sheets"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from cmd_args_settings import GSheetsSettings


def init_google_api(google_credentials_path):
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    :param google_credentials_path:
    :param ebay_order2tracking: {'order_id': 'tracking_num'}
    :return:
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                google_credentials_path, GSheetsSettings.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)


def update(google_credentials_path, ebay_order2tracking):
    service = init_google_api(google_credentials_path)
    # Call the Sheets API
    sheet = service.spreadsheets()
    order_sheet = sheet.values().get(spreadsheetId=GSheetsSettings.SAMPLE_SPREADSHEET_ID,
                                     range=GSheetsSettings.ORDER_SHEET_NAME).execute()
    order_sheet_values = order_sheet.get('values', [])
    df = pd.DataFrame(order_sheet_values[1:], columns=order_sheet_values[0])
    #ebay_order2tracking = [('20-04037-62337', '5'), ('19-04037-68336', '3')]
    ebay_order2tracking = [tuple(order_id, tracking) for order_id, tracking in ebay_order2tracking.items()]
    df_order2tracking = pd.DataFrame(ebay_order2tracking, columns=['Ebay order', 'Updated Tracking'])
    df_update_data = df.merge(df_order2tracking, left_on="eBay Order ID", right_on="Ebay order", how="inner")
    df_amazon2tracking = df_update_data[["Amazon Order ID", "Updated Tracking"]]
    # paste to sheet
    tracking_sheet = sheet.values().get(spreadsheetId=GSheetsSettings.SAMPLE_SPREADSHEET_ID,
                                        range=GSheetsSettings.TRACKING_SHEET_NAME).execute()
    tracking_sheet_values = tracking_sheet.get('values', [])
    df_tracking = pd.DataFrame(tracking_sheet_values)  # , columns=tracking_sheet_values[0])
    df_tracking.columns = df_tracking.iloc[0]
    df_tracking.drop(df_tracking.index[0], inplace=True)
    tracking_final_data = df_amazon2tracking.merge(df_tracking, how='outer', left_on="Amazon Order ID",
                                                   right_on="Amazon order-id")
    # update only trackings which we've got from ebay. nan in "Updated Tracking" means it wasn't got from ebay, just filled during merging
    tracking_final_data["Merged Trackings"] = tracking_final_data.apply(
        lambda row: row["Updated Tracking"] if not pd.isna(row["Updated Tracking"]) else row["tracking-number"],
        axis=1)
    # copy not None value of "Tracking" to "tracking-number" in tracking_final_data
    batch_update_values_request_body = {
        # How the input data should be interpreted.
        'value_input_option': 'USER_ENTERED',  # TODO: Update placeholder value.
        # 'value_input_option': 'INPUT_VALUE_OPTION_UNSPECIFIED',
        # The new values to apply to the spreadsheet.
        'data': [
            {"range": f"{GSheetsSettings.TRACKING_SHEET_NAME}!A2",
             "majorDimension": "COLUMNS",
             "values": [tracking_final_data["Amazon order-id"].tolist()]
             },

            {"range": f"{GSheetsSettings.TRACKING_SHEET_NAME}!G2",
             "majorDimension": "COLUMNS",
             "values": [tracking_final_data["Merged Trackings"].tolist()]
             }
            # TODO: Update placeholder value.
        ]
        # TODO: Add desired entries to the request body.
    }
    request = sheet.values().batchUpdate(spreadsheetId=GSheetsSettings.SAMPLE_SPREADSHEET_ID, body=batch_update_values_request_body)
    response = request.execute()
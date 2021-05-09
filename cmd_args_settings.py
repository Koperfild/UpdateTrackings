"""Sets cmd arguments for ebay and google sheets credentials"""


import argparse
import time
import sys


class EbaySettings:
    app_scopes = ['https://api.ebay.com/oauth/api_scope',
             'https://api.ebay.com/oauth/api_scope/sell.marketing.readonly',
             'https://api.ebay.com/oauth/api_scope/sell.marketing',
             'https://api.ebay.com/oauth/api_scope/sell.inventory.readonly',
             'https://api.ebay.com/oauth/api_scope/sell.inventory',
             'https://api.ebay.com/oauth/api_scope/sell.account.readonly',
             'https://api.ebay.com/oauth/api_scope/sell.account',
             'https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly',
             'https://api.ebay.com/oauth/api_scope/sell.fulfillment',
             'https://api.ebay.com/oauth/api_scope/sell.analytics.readonly',
             'https://api.ebay.com/oauth/api_scope/sell.finances',
             'https://api.ebay.com/oauth/api_scope/sell.payment.dispute',
             'https://api.ebay.com/oauth/api_scope/commerce.identity.readonly'
    ]

    DEFAULT_REFR_TOKENS_PATH = "refresh tokens.txt"
    DEFAULT_EBAY_DEV_CREDENTIALS_PATH = "ebay_dev_credentials.json"

class GSheetsSettings:
    DEFAULT_GSHEETS_CREDENTIALS_PATH = 'google_sheets_credentials.json'
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    ORDER_SHEET_NAME = "Order"
    TRACKING_SHEET_NAME = "Tracking"
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1idgxvBbdx46hIxEvlkOxVJ_Hf33dWfoCGYaCy3feCBI'

parser = argparse.ArgumentParser(description="Uses refresh token to get new access token and then get ebays orders and"
                                             "update google sheets with them")
parser.add_argument("-r",
                    "--refr_tokens_path",
                    help="path to json file {'email':'refr_key'",
                    default=EbaySettings.DEFAULT_REFR_TOKENS_PATH)
parser.add_argument("-d",
                    "--dev_creds_path",
                    help="path to json file with ebay app developer credentials",
                    default=EbaySettings.DEFAULT_EBAY_DEV_CREDENTIALS_PATH)
parser.add_argument("-g",
                    "--gcredentials",
                    help="Specify google credentials path(absolute or relative to the current working directory) which"
                         " you can download from google api tutorial",
                    default=GSheetsSettings.DEFAULT_GSHEETS_CREDENTIALS_PATH)

args = parser.parse_args()
#We require either both email and password or neither of the two
if len([x for x in [args.email,args.password] if x is not None]) == 1:
    print("Error in calling program. Either don't provide email and password or provide both")
    time.sleep(100)
    sys.exit(1)

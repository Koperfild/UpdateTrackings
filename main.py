"""Used after you have refresh tokens for ebay business accounts received by ebay-oauth-python-client app.
This 'UpdateTrackings' app queries tracking information of orders and then fills up this information to google sheets
where all required information for business managers is stored"""

import refresh_token
from cmd_args_settings import EbaySettings, GSheetsSettings, args
from oauthclient.model.model import environment
import ebay_manager
from oauthclient.credentialutil import credentialutil
import update_google_sheet


if __name__ == "__main__":
    #credentials are used in oauth2api() and get_ebay_orders
    credentialutil.load(args.dev_creds_path)
    dev_credentials = credentialutil.get_credentials(environment.PRODUCTION)

    email2acc_token = refresh_token.get_access_tokens(args.refr_tokens_path, environment.PRODUCTION, EbaySettings.app_scopes)
    order_id2tracking = {}
    for email, access_token in email2acc_token.items():
        order_id2tracking.update(ebay_manager.get_order2tracking(dev_credentials, access_token))
    update_google_sheet.update(GSheetsSettings.DEFAULT_GSHEETS_CREDENTIALS_PATH, order_id2tracking)

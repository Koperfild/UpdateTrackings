"""Gets access tokens for several emails providing refresh tokens to ebay's oauthclient.oauth2api"""

import json
from oauthclient.oauth2api import oauth2api
from oauthclient.credentialutil import credentialutil


def get_refresh_tokens(path):
    """
    Reads refresh tokens from json file.
    :param path: path to json file with refresh tokens
    :return: {'email': 'refr_token'}
    """
    with open(path, 'r') as f:
        return json.load(f)


def _get_access_tokens(email2refr_token, environment, app_scopes):
    oauth2api_inst = oauth2api()
    access_tokens = {}
    for email, refr_token in email2refr_token.items():
        access_token = oauth2api_inst.get_access_token(environment, refr_token, app_scopes)
        access_tokens[email] = access_token
    return access_tokens


def get_access_tokens(refr_tokens_path, environment, app_scopes):
    email2refr_token = get_refresh_tokens(refr_tokens_path)
    email2acc_tok = _get_access_tokens(email2refr_token, environment, app_scopes)
    return email2acc_tok


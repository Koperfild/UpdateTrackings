"""Requests ebay via ebay Trading API. Collects order ids and corresponding tracking numbers"""

from ebaysdk.trading import Connection as Trading
from datetime import datetime, timedelta


def get_order2tracking(dev_credentials, access_token):
    """Trading API is used with dev credentials and access token of ebay business account.
    :return { order_id: tracking }"""
    api = Trading(
        # iaf_token='v^1.1#i^1#I^3#r^0#p^3#f^0#t^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',
        iaf_token=access_token,
        config_file=None,
        # appid='AlexMoss-Tracking-PRD-138876c2a-4837a214',
        appid=dev_credentials.appid,
        # certid='PRD-38876c2ad8b8-53bb-4b68-981a-92f9',
        certid=dev_credentials.certid,
        # devid='7f33b712-4d3a-42e8-847d-e4bd3ca34b1f',
        devid=dev_credentials.devid,
        # proxy_host= '5.79.66.2',
        # proxy_port= '13010',
        warnings=True)
    try:
        response_test = api.execute('GetOrders',
                                    {'CreateTimeFrom': datetime.now() - timedelta(days=90), 'CreateTimeTo': datetime.now()})
        def extract_tracking(order):
            return order.TransactionArray.Transaction[0].ShippingDetails.ShipmentTrackingDetails.ShipmentTrackingNumber
        order_id2tracking = {order.OrderID: extract_tracking(order) for order in response_test.reply.OrderArray}
        return order_id2tracking
    except ConnectionError as e:
        print(e)
        print(e.response.dict())


    #DELETE: old
    # response = api.execute('GetOrders', {'OrderIDArray': {'OrderID': item_line}})
    # response_test = api.execute('GetOrders', {'OrderIDArray': ['05-04261-14511']})
    # track_number = response_test.reply.OrderArray.Order[0].TransactionArray.Transaction[0].ShippingDetails.ShipmentTrackingDetails.ShipmentTrackingNumber
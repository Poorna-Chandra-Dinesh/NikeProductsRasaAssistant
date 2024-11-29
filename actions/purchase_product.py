##########################################################################################
##########################################################################################
#
#       Developed by Atef Bader,PhD
#       Last Edit: 11/13/2024
#
##########################################################################################
##########################################################################################




from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.db import get_product
from actions.Using_GPT4_Vision_With_Function_Calling import delivery_exception_support_handler

import json
import random

product_purchased_path = "db/my_products_purchased.json"

class PurchaseProduct(Action):

    def name(self) -> str:
        return "purchase_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):

        customer_name = tracker.get_slot("customer_name")
        customer_preferences = tracker.get_slot("customer_preferences_for_product_purchase")
        customer_shipping_address = tracker.get_slot("customer_shipping_address")
        customer_payment_info = tracker.get_slot("customer_payment_info")

        if customer_name is None or customer_preferences is None \
            or customer_shipping_address is None or customer_payment_info is None:
            return [SlotSet("return_value", "data_not_present")]
        

        purchase_order_number = random.randint(1000000,2000000)
        #Create the list of dictionary
        result = [{'customer_name': customer_name, \
                   'customer_shipping_address': customer_shipping_address, \
                        'customer_payment_info':customer_payment_info, \
                        'purchase_order_number':purchase_order_number
                 }]



        with open(product_purchased_path) as feedsjson:
                feeds = json.load(feedsjson)

        feeds.append(result)
        with open(product_purchased_path, mode='w') as f:
                f.write(json.dumps(feeds, indent=2))

   
        return [SlotSet("return_value", "order_processed"),
                SlotSet("purchase_order_number", purchase_order_number)]
    

##########################################################################################
##########################################################################################
#
#   Developed by Atef Bader, PhD
#   Last Edit: 11/13/2024
#
##########################################################################################
##########################################################################################




from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.db import get_product
from actions.db import get_product_orders

from actions.Using_GPT4_Vision_With_Function_Calling import delivery_exception_support_handler
import pandas as pd


class CheckOrderStatus(Action):

    def name(self) -> str:
        return "check_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):



        df = pd.read_json('db/my_product_orders.json')



        customer_name = tracker.get_slot("customer_name")
        order_number = tracker.get_slot("order_number")


        if customer_name is None or order_number is None:
            return [SlotSet("return_value", "data_not_present")]
        
        gpt_evaluate_picture = df.loc[df['order_number'] == int(order_number), 'picture_name'].values[0]
        print('\n gpt_evaluate_picture=', gpt_evaluate_picture, '\n')


        if delivery_exception_support_handler(gpt_evaluate_picture).action == "replace_order":
            print('Sorry about that,  we will replace your order at no charge')
            return [SlotSet("return_value", "replace_order")]

        if delivery_exception_support_handler(gpt_evaluate_picture).action == "refund_order":
            print('Sorry about that,  we will refund your order at no charge')
            return [SlotSet("return_value", "refund_order")]

        if delivery_exception_support_handler(gpt_evaluate_picture).action == "escalate_to_agent":
            print('Sorry about that,  but you need to follow up with a human-agent on this')
            return [SlotSet("return_value", "escalate_to_agent")]
           

        return [SlotSet("customer_name", customer_name), 
                SlotSet("order_number", order_number), 
                SlotSet("photo", "severly-damaged-nike-box")
                ]
    

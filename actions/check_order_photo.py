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
from actions.Using_GPT4_Vision_With_Function_Calling import delivery_exception_support_handler
from actions.db import get_product_orders
import pandas as pd

class CheckOrderPhoto(Action):

    def name(self) -> str:
        return "check_order_photo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):


        customer_name = tracker.get_slot("customer_name")
        order_number = tracker.get_slot("order_number")


        if customer_name is None or order_number is None:
            return [SlotSet("return_value", "data_not_present")]
        

        df = pd.read_json('db/my_product_orders.json')

        print('\n Dataframe picture=', df.loc[[0], 'picture'], '\n')
        print('\n Dataframe order_number=', df.loc[[0], 'order_number'], '\n')
        print('\n Type Dataframe order_number=', type(df.loc[[0], 'order_number']), '\n')
        print('\n Slot Read order_number=', order_number, '\n')
        print('\n Type Slot Read order_number=', type(order_number), '\n')


     
        df2 = df.set_index(['order_number'])

        if not (int(order_number) in df2.index): 
            print('\n NOT a valid Order Number=', order_number, '\n')
            return [SlotSet("customer_name", customer_name), 
                SlotSet("order_number", order_number), 
                SlotSet("order_number_validation", "invalid")
                ]
        else:
            print('\n Valid Order Number=', order_number, '\n')

           

        picture_to_evaluate = df.loc[df['order_number'] == int(order_number), 'picture'].values[0]
        print('\n picture_to_evaluate=', picture_to_evaluate, '\n')

 

        return [SlotSet("customer_name", customer_name), 
                SlotSet("order_number", order_number), 
                SlotSet("photo", picture_to_evaluate)
                ]
    

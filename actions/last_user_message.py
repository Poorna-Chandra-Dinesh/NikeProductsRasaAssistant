
##########################################################################################
##########################################################################################
#
#   Developed by Atef Bader,PhD
#   Last Edit: 11/13/2024
#
##########################################################################################
##########################################################################################



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionLastUserMessage(Action):
    def name(self) -> Text:
        return "last_user_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve the last user message
        last_user_message = tracker.latest_message.get('text')
        
     
        if "Nike shorts" in last_user_message:
            valid_request = "Nike shorts"
            print("Buy Nike Shoes")
        elif "order status" in last_user_message:
            valid_request = "order status"
            print("Order Status")
        else:
            valid_request = "out of scope"
            print("Out of Scope")


 
        if valid_request :
            return [ SlotSet("request_type", valid_request)]
    
    

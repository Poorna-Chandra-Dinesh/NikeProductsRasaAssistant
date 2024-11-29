from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.db import get_product
from actions.Using_GPT4_Vision_With_Function_Calling import delivery_exception_support_handler
from actions.Recommender_Embeddings.Recommendations_using_embedding import print_recommendations_from_strings

import pandas as pd

product_catalog_path = "actions/Recommender_Embeddings/data/Products_Catalog-002.csv"

class RecommendProductWithIntentRanking(Action):

    def name(self) -> str:
        return "recommend_product_with_intent_ranking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]) -> list:

        # Load data
        df = pd.read_csv(product_catalog_path)

        # Retrieve slots
        customer_name = tracker.get_slot("customer_name")
        customer_preferences = tracker.get_slot("customer_preferences_for_product_purchase")

        # Get intent ranking from the tracker
        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        top_intent = intent_ranking[0]["name"] if intent_ranking else "unknown"

        # Log the intent ranking for debugging
        print("\nIntent Ranking:", intent_ranking)
        print("Top Intent:", top_intent, "\n")

        if customer_name is None or customer_preferences is None:
            return [SlotSet("return_value", "data_not_present")]

        print('\nPreferences =', customer_preferences, '\n')
        
        # Call the recommendation function
        recommended_product_indices = print_recommendations_from_strings(customer_preferences, 1)
        print('\nRecommended Product Indices =', recommended_product_indices, '\n')

        # Get product details from the dataframe
        recommended_product_photo = df.loc[recommended_product_indices[0], 'Photo']
        print('\nModel Recommended =', recommended_product_photo, '\n')

        recommended_product_name = df.loc[recommended_product_indices[0], 'Model']
        recommended_product_price = df.loc[recommended_product_indices[0], 'Price']

        # Dispatch intent ranking information for conversational context
        dispatcher.utter_message(text=f"Intent '{top_intent}' was identified with a ranking of: {intent_ranking}")

        return [
            SlotSet("product_name", recommended_product_name), 
            SlotSet("product_number", recommended_product_price), 
            SlotSet("photo", recommended_product_photo),
            SlotSet("intent_ranking", intent_ranking),  # Save intent ranking to a slot if needed later
        ]

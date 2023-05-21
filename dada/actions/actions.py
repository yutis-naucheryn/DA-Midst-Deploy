# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

import arrow 
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pytube
from typing import Any, Text, Dict, List

city_db = {
    'brussels': 'Europe/Brussels', 
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific',
    'malaysia': 'Asia/Kuala_Lumpur'
}

class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []
        
        current_place_lower = current_place.lower() # convert to lower case
        
        tz_string = city_db.get(current_place_lower, None)
        if not tz_string:
            msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
                
        tz = arrow.now(tz_string).tzinfo
        current_time = utc.to(tz).format('HH:mm')
        msg = f"It's {current_time} in {current_place} now."
        dispatcher.utter_message(text=msg)
        
        return []


"""
class ActionRememberProblem(Action):

    def name(self) -> Text:
        return "action_remember_problem"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_problem = next(tracker.get_latest_entity_values("problem"), None)
        utc = arrow.utcnow()
        
        #msg = f"I can see you are feeling {current_mood} now, lets figure out how to overcome this."
        #dispatcher.utter_message(text=msg)
        
        return [SlotSet("problem", current_problem)]
"""

class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Sorry, I don't understand. Let's talk about managing stress. How can I help you today?")
        return []

# tutorial
class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        current_place_lower = current_place.lower() # convert to lower case
        
        if not current_place:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(current_place_lower, None)
        if not tz_string:
            msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        msg = f"Sure thing! I'll remember that you live in {current_place}."
        dispatcher.utter_message(text=msg)
        
        return [SlotSet("location", current_place)]


class ActionTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        timezone_to = next(tracker.get_latest_entity_values("place"), None)
        timezone_in = tracker.get_slot("location")
        
        if not timezone_in:
            msg = "To calculuate the time difference I need to know where you live."
            dispatcher.utter_message(text=msg)
            return []
        
        if not timezone_to:
            msg = "I didn't the timezone you'd like to compare against. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string_to = city_db.get(timezone_to, None)
        if not tz_string_to:
            msg = f"I didn't recognize {timezone_to}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string_in = city_db.get(timezone_in, None)
        if not tz_string_in:
            msg = f"I didn't recognize {timezone_in}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        t1 = arrow.utcnow().to(tz_string_to).shift(days=1).replace(hour=0, minute=0, second=0, microsecond=0)
        t2 = arrow.utcnow().to(tz_string_in).shift(days=1).replace(hour=0, minute=0, second=0, microsecond=0)
        max_t, min_t = max(t1, t2), min(t1, t2)
        diff = max_t - min_t
        diff_hours = abs(diff.total_seconds()) // 3600
        
        msg = f"There is a {diff_hours}H time difference."
        dispatcher.utter_message(text=msg)
        
        return []
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
from __future__ import print_function
import webbrowser
from requests          import Session
from typing            import Any, Text, Dict, List
from rasa_sdk          import Action, Tracker
from rasa_sdk.events   import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction
import logging
import arrow 
from flask import Flask, render_template, jsonify
from flask import request
import dateparser
import datetime
from datetime import datetime
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
import os
from twilio.rest import Client
# importing the APIs
from API.wikiapi import wiki_extract_summary_part
from API.newsapi import news_from_subject_or_category, headlines_from_subject_or_category, just_news
# from actions.app import jules
import jinja2
ALLOWED_TYPE_OF_CALL = ["facetime", "ft", "phone", "vocal"]
ALLOWED_NICKNAME = ["Jules", "Jason", "Samuel", "Tanel", "Antony"]
account_sid = 'AC8a035385c4d448ed90aca6616ae6d3ec'
auth_token = '3b29601162031119daecf5ab1aab9d48'
client = Client(account_sid, auth_token)


import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

class ValidateSimpleCallForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_call_form"
    

    def validate_type_of_call(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `type_of_call` value."""

        if slot_value.lower() not in ALLOWED_TYPE_OF_CALL:
            dispatcher.utter_message(text=f"On ne fait que des facetime ou appels vocaux.")
            return {"type_of_call": None}
        dispatcher.utter_message(text=f"OK! Tu veux un appel {slot_value}.")
        return {"type_of_call": slot_value}

    def validate_nickname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `nickname` value."""

        if slot_value not in ALLOWED_NICKNAME:
            dispatcher.utter_message(text=f"Je ne reconnais pas cette personne. On peut appeler {'/'.join(ALLOWED_NICKNAME)}.")
            return {"nickname": None}
        dispatcher.utter_message(text=f"OK! Tu veux appeler {slot_value}.")
        destinataire = slot_value
        with open("actions/numbersdb.txt","r") as numbers :
            a=dict()
            for line in numbers:
                data = line.split()
                a[str(data[0])]=data[1]
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
                        to=str(a[str(destinataire)]),
                        from_='+19897488459'
                        )
        print(call.sid)
        return {"nickname":slot_value}
    
class Nice_phone_call(Action):
    def name(self) -> Text:
        return "action_show_call"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = next(tracker.get_latest_entity_values("personnality"), None)
        # exec("./actions/app.py")
        app = Flask(__name__)
        @app.route('/')
        def index():
            return render_template('/index.html', number= +33633829480)
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'##Force à ouvrir sur Google Chrome par défaut
        webbrowser.get(chrome_path).open("http://127.0.0.1:5000/")
        print("a fonctionné ")

        return []


class ActionWiki(Action):

    def name(self) -> Text:
        return "action_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = next(tracker.get_latest_entity_values("personnality"), None)
        ##récupère le nom de la personnalité recherchée
        print(subject)
        print("problème de reconnaissance")
        
        if not subject: ##si il ne reconnait pas la personnalité
            msg = f"I haven't recognized what you were looking for. Can you rephrase ? Or find synonyms ?"
            dispatcher.utter_message(text=msg)
            return []
        subject_process = subject.lower()
        summary = wiki_extract_summary_part(subject_process,0.6)
        if summary == "": 
            msg = f"I don't know yet about it.."
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"I found this about {subject} : \n {summary}"#Renvoi un résumé de la page wikipedia de la personnalité
        dispatcher.utter_message(text=msg)
        
        return []


class ActionSimpleInfo(Action):
    def name(self) -> Text:
        return "action_tell_simple_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        session = Session()

        search = tracker.get_slot("info") 
        print(search)
        with open("actions/user_info.txt","r") as infos: #récupère les infos dans le fichier user_info.txt
            a=dict()
            for line in infos:
                data = line.split()#doublet composé du nom de l'info et de sa valeur
                a[str(data[0])]=data[1]
        dispatcher.utter_message(a[str(search)])

        return []

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class ActionGoogleDrive(Action):
    def name(self) -> Text:
        return "action_find_doc"
    
    def run(self, dispatcher: CollectingDispatcher, tacker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
        session = Session()
        creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                'actions/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
            results = service.files().list(
                pageSize=50, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            for item in items:
                if item['name']=='2022-01-28.png':
                # request = service.files().get_media(fileId=item['id'])
                # fh = io.BytesIO()
                # downloader = MediaIoBaseDownload(fh, request)
                # done = False
                # while done is False:
                #     status, done = downloader.next_chunk()
                #     print(F'Download {int(status.progress() * 100)}.')
                    content = service.files().get_media(fileId=item['id']).execute()
                    with open('out2.png', 'wb') as f:
                        f.write(content)
                    img = mpimg.imread('out2.png')
                    imgplot = plt.imshow(img)
                    plt.show()
          ##récupère le corps du file mentionné, le renvoi dans out2 et l'affiche à l'écran      
          
            # print(u'{0} ({1})'.format(item['name'], item['id']))

        except HttpError as error:
        
            print(f'An error occurred: {error}')


class ValidateMemoryTestForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_memory_test_form"
    

    def validate_age_of_son(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `age_of_son` value."""

        if slot_value==str(33):
            dispatcher.utter_message(text=f"Tout va bien.")
            return {"age_of_son": slot_value}
        dispatcher.utter_message(text=f"Tu as faux, tu as besoin d'aide.")
        return {"age_of_son": None}  

class ActionNews(Action):

    def name(self) -> Text:
        return "action_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = next(tracker.get_latest_entity_values("subject"), None)
        
        print(subject)
        print("problème de reconnaissance")
        
        if not subject:
            news = just_news()
            msg = f"Here are the top headlines : {news}"
            dispatcher.utter_message(text=msg)
            return []
        subject_process = subject.lower()
        ## ajouter la date en format us pour chercher dans les 5 derniers jours
        news = news_from_subject_or_category(q=subject_process,) 
        if news == '': # not recognized
            msg = f"It seems I haven't found any news on the {str(subject)} topic.."
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"I found this in the press : \n{news}"
        dispatcher.utter_message(text=msg)
        
        return []
 
from geopy import geocoders 
from geopy.geocoders import Nominatim 
from tzwhere import tzwhere
from timezonefinder import TimezoneFinder
from time import strftime

def get_local_zone(city):
    tf = TimezoneFinder()
    loc = Nominatim(user_agent="GetLoc") 
    getLoc = loc.geocode(str(city))
    return(tf.timezone_at(lng=getLoc.longitude, lat=getLoc.latitude))


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("city"), None)
        
        print(current_place)
        utc = arrow.utcnow()
        if not current_place:
            msg = f"Il est {utc} utc chez toi. Je n'ai pas reconnu la localisation."
            dispatcher.utter_message(text=msg)
            return []
        tz_string = get_local_zone(current_place)
        if not tz_string: # not recognized
            msg = f"Je n'ai pas reconnu {current_place}. Est-ce épeller correctement? \n C'est peut être hors de portée pour moi"
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"Il est {utc.to(get_local_zone(current_place)).format('HH:mm')} à {current_place} ."
        dispatcher.utter_message(text=msg)
        
        return []
    


            
        

  



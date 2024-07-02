import os
import json
import datetime as dt
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# The scope for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    token_path = 'token.json'
    
    # Check if token.json exists and load credentials from it
    if os.path.exists(token_path):
        try:
            with open(token_path, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
        except (json.decoder.JSONDecodeError, ValueError):
            print("The token file is invalid. Deleting and re-authenticating.")
            os.remove(token_path)
    
    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error during authentication: {e}")
                return
        
        # Save the credentials for the next run
        if creds:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        else:
            print("Failed to obtain credentials.")
            return
    
    # Build the service
    try:
       service = build('calendar', 'v3', credentials=creds)
       event={
           "summary": "My evnt high",
           "location" : "online",
           "description": " mast even it will be",
           "coloID":6,
           "start":{
               "dateTime": "2024-07-22T09:00:00+05:30",
               "timeZone":"Asia/Kolkata"
           },
           "end":{
               "dateTime": "2024-07-22T09:09:00+05:30",
               "timeZone":"Asia/Kolkata"
           },
           "recurrence":[
               "RRULE:FREQ=DAILY;COUNT=3"
           ],
           "attendees": [
               {"email":"purabgupta2205@gmail.com"},
               {"email":"purabgupta2204@gmail.com"}

           ]


       }

       event= service.events().insert(calendarId="primary",body=event).execute()
       print(f"Event crdeated {event.get('htmlLink')}")

       
    except Exception as error:
        print(f"Error fetching events: {error}")
        return

    
    

if __name__ == '__main__':
    main()
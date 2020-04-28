from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from datetime import datetime
import base64
import email
import quopri
import requests
import json
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def loginToService():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    # Call the Gmail Label API 
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

    return service

def ListMessagesMatchingQuery(service, user_id, max_result ,query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token, maxResults = max_result).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    # print('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    # print ('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def main():
 
    #retrieve message from gmail
    service = loginToService()

    msgs = ListMessagesMatchingQuery(service,"me", 1 ,"from:pauljung@ymail.com")    
    msg = GetMessage(service,"me",msgs[0].get('id'))
    
    #retrieve title
    subject = msg['payload']['headers'][18]['value']
    date = subject.split('주보')[0]
    year = datetime.datetime.now().year
    title = str(year) + "년 " + date + "교회소식"
    

    rm1 = msg['payload']['parts'][0]['parts'][0]['body']['data']
    rm2 = msg['payload']['parts'][0]['parts'][1]['body']['data']
        
    #decode content to plain text    
    plTxt = base64.urlsafe_b64decode(rm1).decode("utf-8")

    #decode content to html text
    qtprt = quopri.decodestring(base64.urlsafe_b64decode(rm2))
    htmlTxt = qtprt.decode("utf-8")

    #cleaning up the content
    tmpHtml = htmlTxt.split("교회소식")[1].replace('<br>', '')
    fHtml = rreplace(tmpHtml,'&nbsp;', '', 1)
    
    #post to wordpress api
    wordPressUrl = "http://arkmumc.org/wp-json/wp/v2"
    user = "mikesungunkim"
    password = "vQX3 aKUm eL07 4tyf VdGc 7TwB"

    cred = user + ":" + password
    token = base64.b64encode(cred.encode())
    
    header = {
        'Authorization' : 'Basic ' + token.decode('utf-8'),
        'User-Agent': 'XY'
    }
    
    post = {
        'title' : title,
        'status' : 'publish',
        'content' : fHtml,
        'categories' :[25,22]
    }

    newPostRequest = requests.post(wordPressUrl + "/posts",headers=header, json = post)
    print(newPostRequest)


if __name__ == '__main__':
    main()
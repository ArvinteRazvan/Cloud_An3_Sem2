from __future__ import print_function
import httplib2
import os
import base64
import email

from apiclient import errors
from mapcoordinates import get_coordonates

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import webapp2

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

SCOPES_C = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE_C = 'client_secret_c.json'
APPLICATION_NAME_C = 'Google Calendar API Python Quickstart'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('Hello world!')
        main(self)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


def get_credentials_c(output):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_C, SCOPES_C)
        flow.user_agent = APPLICATION_NAME_C
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        output.response.write('Storing credentials to ' + credential_path)
    return credentials


def get_credentials(output):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        output.response.write('Storing credentials to ' + credential_path)
    return credentials


def GetMessage(service, user_id, msg_id, output):
    """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        output.response.write('Message snippet: %s' % message['snippet'])

        return message
    except errors.HttpError:
        output.response.write('An error occurred:')


def createvent(service, name, description, output):
    location = get_coordonates()
    # print(location)
    event = {
        'summary': name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': '2018-04-05T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2018-04-05T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },

    }
    event = service.events().insert(calendarId='andreipaulmagu@gmail.com', body=event).execute()
    output.response.write('Event created: %s' % (event.get('htmlLink')))


def main(output):
    # idmesaj='16291a3a319cad82'
    """Shows basic usage of the Gmail API.
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials(output)
    credentials_c = get_credentials_c(output)
    http = credentials_c.authorize(httplib2.Http())
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    service_c = discovery.build('calendar', 'v3', http=http)

    logare = input("dati id'ul de logare")
    idmesaj = input("dati id mesaj")
    description = GetMessage(service, logare, idmesaj, output)

    name = input("dati numele evenimentului")

    createvent(service_c, name, description, output)

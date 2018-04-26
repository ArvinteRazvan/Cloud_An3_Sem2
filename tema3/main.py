from __future__ import print_function
from google.cloud import storage
import os
from oauth2client.file import Storage
import google_auth_httplib2 as goo
from apiclient import discovery
import base64
from apiclient import errors
from oauth2client import client, tools



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
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
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_attachments(service, A_id):
    try:
        message = service.users().messages().get(userId='me', id=A_id).execute()

        for part in message['payload']['parts']:
            #print (part)
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=A_id,
                                                                       id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

                #file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                path = ''.join(['C:/Users/scandurel/Desktop/faculty and tech/clowd/t3/remastered/', part['filename']])

                f = open(path, 'w')
                f.write(str(file_data))
                f.close()
    except errors.HttpError:

        print('An error occurred:')
    return path

def upload(name,titlu):
    storage_client = storage.Client.from_service_account_json('Tema3-8d2d1c837720.json')
    #buckets = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket('gateata')
    blob2 = bucket.blob(titlu)
    blob2.upload_from_filename(filename=name)

def upload_drive(document,titlu):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(goo._make_default_http()))

    FILES = (
        #(document, None),
        (document, 'application/vnd.google-apps.document'),
    )

    for filename, mimeType in FILES:
        metadata = {'name': titlu}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))




def main():
    credentials = get_credentials()
    http = credentials.authorize(goo._make_default_http())
    service = discovery.build('gmail', 'v1', http=http)
    id=input('dati id email')
    attachment=get_attachments(service,id)
    titlu=input('dati titlu pt document')
    upload(attachment,titlu)
    upload_drive(attachment,titlu)



if __name__ == '__main__':
    main()

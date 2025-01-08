import base64
import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL
import pprint
import mimetypes
from pathlib import Path




def signed_in_user(access_token):
    if not access_token:
        load_dotenv()
        APPLICATION_ID = os.getenv('APPLICATION_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    endpoint = f'{MS_GRAPH_BASE_URL}/me'

    response = httpx.get(endpoint, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Failed to retrieve emails: {response.text}')

    json_response = response.json()

    return json_response


def search_emails(access_token, search_query=None, filter_list=None, folder_id=None, fields='*', top=5, max_results=100):
    if not access_token:
        load_dotenv()
        APPLICATION_ID = os.getenv('APPLICATION_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    if folder_id is None:
        endpoint = f'{MS_GRAPH_BASE_URL}/me/messages'
    else:
        endpoint = f'{MS_GRAPH_BASE_URL}/me/mailFolders/{folder_id}/messages'

    params = {
        '$select' : fields,
        '$top' : min(top, max_results)
    }

    if search_query:
        params['$search'] = f'"{search_query}"'

    if filter_list:
        params['$filter'] = filter_list

    messages = []
    next_link = endpoint

    while next_link and len(messages) < max_results:
        response = httpx.get(next_link, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception(f'Failed to retrieve emails": {response.json()}')

        json_response = response.json()
        messages.extend(json_response.get('value', []))
        next_link = json_response.get('@odata.nextLink', None)
        params = None

        if (next_link and len(messages) + top  > max_results):
            params = {
                '$top' : max_results - len(messages)
            }

    return messages[:max_results]


def read_emails(access_token, filter=None):
    endpoint = f'{MS_GRAPH_BASE_URL}/me/messages'
    try:
        if not access_token:
            load_dotenv()
            APPLICATION_ID = os.getenv('APPLICATION_ID')
            CLIENT_SECRET = os.getenv('CLIENT_SECRET')
            SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

            access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization' : 'Bearer ' + access_token
        }

        for i in range(0, 4, 2):
            params = {
                '$top': 2,
                '$select': '*',
                '$skip': i,
                '$orderby': 'receivedDateTime desc'
            }

            response = httpx.get(endpoint, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception(f'Failed to retrieve emails: {response.text}')

            json_response = response.json()

            for message in json_response.get('value', []):
                print('Subject: ', message['subject'])
                print('To: ', message['toRecipients'])
                if not message['isDraft']:
                    print('From: ', message['from']['emailAddress']['name'], f"({message['from']['emailAddress']['name']}")
                print('Is Read: ', message['isRead'])
                print('Received Date Time: ', message['receivedDateTime'])
                print()
            print('-' * 150)

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f'Error: {e}')



def send_email(subject, body, recipient_email, access_token=None, include_attachments=False):
    endpoint = f'{MS_GRAPH_BASE_URL}/me/sendMail'
    try:
        if not access_token:
            load_dotenv()
            APPLICATION_ID = os.getenv('APPLICATION_ID')
            CLIENT_SECRET = os.getenv('CLIENT_SECRET')
            SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

            access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        attachments = None
        if include_attachments:
            dir_attachments = Path('./attachments')
            attachments = [create_attachment(attachment) for attachment in dir_attachments.iterdir() if attachment.is_file()]

        message = {
            'message' : draft_message_body(subject, body, attachments, recipient_email)
        }

        response = httpx.post(endpoint, headers=headers, json=message)

        return response
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f'Error: {e}')


def draft_message_body(subject, body, attachments, recipient_email_address):
    message = {
        'subject' : subject,
        'body' : {
            'contentType' : 'HTML',
            'content' : body
        },
        'toRecipients' : [
            {
                'emailAddress' : {
                    'address' : recipient_email_address
                }
            }
        ]
    }

    if attachments is not None:
        message['attachments'] = attachments

    return message

def create_attachment(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode('utf-8')

    return {
        '@odata.type' : 'microsoft.graph.fileAttachment',
        'name' : os.path.basename(file_path),
        'contentType' : get_mime_type(file_path),
        'contentBytes' : encoded_content
    }


def get_mime_type(file_path):
    mime_tyoe, _ = mimetypes.guess_type(file_path)
    return mime_tyoe




def tester_function(access_token=None):
    try:
        if not access_token:
            load_dotenv()
            APPLICATION_ID = os.getenv('APPLICATION_ID')
            CLIENT_SECRET = os.getenv('CLIENT_SECRET')
            SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']

            access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        # filter_list = "from/emailAddress/address eq 'azure-noreply@microsoft.com'&$count=true",
        email_address = 'azurey@microsoft'
        search_query = f"from:{email_address}"
        messages = search_emails(access_token, headers, search_query=search_query)

        print("Messages size: " + str(len(messages)))
        for idx, message in enumerate(messages):
            print('Subject: ', message['subject'])
            print('To: ', message['toRecipients'])
            print('From: ', message['from']['emailAddress']['name'], f"({message['from']['emailAddress']['name']}")
            print('Received Date Time: ', message['receivedDateTime'])
            print()

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f'Error: {e}')


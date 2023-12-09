import json
import base64
import logging
import os
import requests
from tqdm import tqdm
from dateutil.parser import parse
from datetime import datetime, timezone, timedelta
import pytz

logging.basicConfig(format='[%(asctime)s]:[%(levelname)s]:[%(filename)s %(lineno)d]:[%(funcName)s]:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_access_token(client_id, client_secret, refresh_token):
    url = "https://login.microsoftonline.com/d6454b9f-4ca2-4392-b62f-20e21e54335a/oauth2/v2.0/token"

    payload = f'client_id={client_id}&scope=offline_access%20Mail.ReadWrite%20Mail.send&grant_type=refresh_token&client_secret={client_secret}&redirect_uri=https%3A%2F%2Flocalhost&refresh_token={refresh_token}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'buid=0.AXIAn0tF1qJMkkO2LyDiHlQzWv8X8zrAVMtPqebAWud5G3tyAAA.AQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-kZ5EkppMdTFRuYfniN_3y8-Xd4UdnOxoj73wJ1eZZCaKAT8JgDNpeqo0oFp59_urEfHRgAmxblfrvqZtteL87F0uVuBqo0iR-vyvN064OsAgAA; esctx=PAQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-P8XcBu5-Z0yzoAJsYjHRoOrKnytCJJQZgtooKwI6-pwI0SH2MDCLXDXZbbdMx66FO30bZMF3OHeT5bL1TAdiQ4VV253aXWPOxep_3bDQ51hSp_8t3O5-_onUpGnU8RcuxnipsDXB1JojtTrJv8z5wQjGcGTbcAT1ttYODVqDMgIgAA; esctx-FbQVuPalhqg=AQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-3CuntieqvcMk6UUaMPDkg0albmtVMGDKcYBLElzQlZY5BuS8kjO13PYFuvM631jlMLKFAtIxhAhe-6ffmXxJ7FIvp6zkgdlCdjY3zoSgYxAmMXLDc8II0tV8QHkyO8MN_C-kClYgVW8qHbel_H_FjCAA; fpc=Am86eFjVZTxGmw3t5Z7iqnHZjOJlAQAAAAuHAt0OAAAAlaghQQEAAABQhwLdDgAAAP8yaQoCAAAA5IgC3Q4AAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return result['access_token']


def read_mail(access_token=None, from_email=None, top=1):
    subject = r"Arvind Fashions Limited: Storewise Inventory Report - ODIN"
    endpoint = f'https://graph.microsoft.com/v1.0/me/messages'
    params = {"$search": f'"from:{from_email}"', "top": top}

    r = requests.get(endpoint, headers={'Authorization': 'Bearer ' + access_token}, params=params)
    r.raise_for_status()  # Raise an exception if request fails

    if r.ok:
        print('Retrieved emails successfully')
        result_json = r.json()["value"]
        # import pdb; pdb.set_trace();
        if top < 10:
            received_date = parse(result_json[0]['receivedDateTime'])
            return received_date, result_json[0]['body']['content']
        else:
            received_date = parse(result_json[0]['receivedDateTime'])
            return received_date, result_json

        # for data in result_json:
        #     print(data['receivedDateTime'])
        #     print(data['subject'])
        #     print(data['bodyPreview'])
        #     # print(data['body']['content'])
        #     print(data['hasAttachments'])


def download_attachment(access_token=None, email_date=None, from_email=None, filename=None, email_object=None):
    endpoint = f'https://graph.microsoft.com/v1.0/me/messages'
    received_date = None
    if email_object is None:
        params = {"$search": f'"from:{from_email}"', "top": 4}

        r = requests.get(endpoint, headers={'Authorization': 'Bearer ' + access_token}, params=params)
        r.raise_for_status()  # Raise an exception if request fails

        if r.ok:
            print('Retrieved emails successfully')
            result_json = r.json()["value"]
            first_received_date = parse(result_json[0]['receivedDateTime'])
            received_date = first_received_date
            for data in result_json:
                received_date = parse(data['receivedDateTime'])
                if received_date.date() == email_date and data['hasAttachments']:
                    # getting message id
                    message_id = data["id"]

                    endpoint_attachment = endpoint + "/" + message_id + "/attachments/"
                    r = requests.get(endpoint_attachment, headers={'Authorization': 'Bearer ' + access_token})
                    r.raise_for_status()  # Raise an exception if request fails
                    # Getting the last attachment id
                    attachment_id = r.json().get('value')[-1].get('id')

                    endpoint_attachment_file = endpoint_attachment + "/" + attachment_id + "/$value"

                    res = requests.get(url=endpoint_attachment_file,
                                       headers={'Authorization': 'Bearer ' + access_token}, stream=True)
                    res.raise_for_status()  # Raise an exception if request fails

                    file_size = len(r.content)
                    with open(f"{filename}", 'wb') as f, tqdm(unit='iB', unit_scale=True, unit_divisor=1024,
                                                              total=file_size,
                                                              desc=f"Downloading {filename}") as pbar:
                        for data in res.iter_content(chunk_size=1024):
                            pbar.update(len(data))
                            f.write(data)
                    return received_date, True
            return first_received_date, False
    if email_object:
        received_date = parse(email_object['receivedDateTime'])
        if received_date.date() == email_date and email_object['hasAttachments']:
            # getting message id
            message_id = email_object["id"]

            endpoint_attachment = endpoint + "/" + message_id + "/attachments/"
            r = requests.get(endpoint_attachment, headers={'Authorization': 'Bearer ' + access_token})
            r.raise_for_status()  # Raise an exception if request fails
            # Getting the last attachment id
            attachment_id = r.json().get('value')[-1].get('id')

            endpoint_attachment_file = endpoint_attachment + "/" + attachment_id + "/$value"

            res = requests.get(url=endpoint_attachment_file,
                               headers={'Authorization': 'Bearer ' + access_token}, stream=True)
            res.raise_for_status()  # Raise an exception if request fails

            file_size = len(r.content)
            with open(f"{filename}", 'wb') as f, tqdm(unit='iB', unit_scale=True, unit_divisor=1024,
                                                      total=file_size,
                                                      desc=f"Downloading {filename}") as pbar:
                for data in res.iter_content(chunk_size=1024):
                    pbar.update(len(data))
                    f.write(data)
            return received_date, True

    return  received_date, False


def draft_attachment(files):
    if not os.path.exists(files):
        logger.info('File is not found')
        return

    with open(files, 'rb') as upload:
        media_content = base64.b64encode(upload.read())

    data_body = {
        '@odata.type': '#microsoft.graph.fileAttachment',
        'contentBytes': media_content.decode('utf-8'),
        'name': os.path.basename(files),
    }
    return data_body


def send_small_file_email_attachment(senders_email, subject, files, mail_text, access_token):
    html_content = f"""
    <html>
    <body>
        {mail_text}
    </body>
    </html>
    """

    if files is not None:
        request_body = {
            'message': {
                # recipient list
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': senders_email
                        }
                    }
                ],
                # email subject
                'subject': subject,
                'importance': 'normal',

                # include attachments
                'attachments': [
                    draft_attachment(files)

                ]
            }
        }
    else:
        request_body = {
            'message': {
                # recipient list
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': senders_email
                        }
                    }
                ],
                # email subject
                'subject': subject,
                "body": {
                    "contentType": "html",
                    "content": html_content
                },
                'importance': 'normal',

            }
        }

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    endpoint = GRAPH_ENDPOINT + '/me/sendMail'

    try:
        response = requests.post(endpoint, headers=headers, json=request_body)
        response.raise_for_status()  # Raise an exception if request fails

        if response.status_code == 202:
            logger.info(f"Email sent to: {senders_email}")
        else:
            logger.exception(f"Email not sent to: {senders_email}")

    except requests.exceptions.RequestException as e:
        logger.exception("An error occurred while sending the email")

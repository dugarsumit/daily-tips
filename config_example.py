config = {
    "SLACK_WEBHOOK": "",
    "PAYLOAD": {
        "text": "",
        "channel": "#testc",
        "username": "webhookbot",
        "icon_emoji": ":ghost:",
    },
    "GOOGLE_SHEET_NAME": "coding-tips",
    "GOOGLE_CLIENT_SECRET_JSON": {
        "type": "service_account",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "",
    },
    "SCOPES": [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ],
}

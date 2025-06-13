import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def autenticar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credenciales.json', SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # ← importante
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        print("🔐 Abre este enlace en tu navegador:")
        print(auth_url)
        code = input("✏️ Ingresa el código de autorización aquí: ")
        flow.fetch_token(code=code)
        creds = flow.credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def subir_archivo(nombre_archivo):
    servicio = autenticar()
    file_metadata = {'name': os.path.basename(nombre_archivo)}
    media = MediaFileUpload(nombre_archivo, resumable=True)
    archivo = servicio.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Archivo subido con ID: {archivo.get('id')}")

if __name__ == '__main__':
    subir_archivo('respaldo.zip')

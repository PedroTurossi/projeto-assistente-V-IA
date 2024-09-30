import datetime
import os.path
import tkinter as tk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import threading

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def obter_credenciais():
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário e é
    # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Se não houver credenciais válidas disponíveis, o usuário deve fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "chave_agenda.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para a próxima execução
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    return creds

def return_calendario():
    try:
        creds = obter_credenciais()
    except Exception as error:
        return f'erro ao obter token: {error}'
    
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        return events

    except HttpError as error:
        print(f"erro: {error}")
        
def tela_adicionar_evento():
    global root
    root = tk.Tk()
    root.configure(background="gray")
    root.geometry('400x300+05-50')
    root.title('Adicionar Evento - BitBot')

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    label_titulo = tk.Label(root, text="Título:", bg='gray')
    label_titulo.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
    input_titulo = tk.Entry(root, width=30, bg='white', fg='black')
    input_titulo.grid(column=1, row=0, padx=10, pady=10)

    label_descricao = tk.Label(root, text="Descrição:", bg='gray')
    label_descricao.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
    input_descricao = tk.Entry(root, width=30, bg='white', fg='black')
    input_descricao.grid(column=1, row=1, padx=10, pady=10)

    label_data_inicio = tk.Label(root, text="Data de Início (AAAA-MM-DD):", bg='gray')
    label_data_inicio.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
    input_data_inicio = tk.Entry(root, width=30, bg='white', fg='black')
    input_data_inicio.grid(column=1, row=2, padx=10, pady=10)

    label_data_fim = tk.Label(root, text="Data de Fim (AAAA-MM-DD):", bg='gray')
    label_data_fim.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
    input_data_fim = tk.Entry(root, width=30, bg='white', fg='black')
    input_data_fim.grid(column=1, row=3, padx=10, pady=10)

    label_hora_inicio = tk.Label(root, text="Hora de Início (Hh:Mm):", bg='gray')
    label_hora_inicio.grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
    input_hora_inicio = tk.Entry(root, width=30, bg='white', fg='black')
    input_hora_inicio.grid(column=1, row=4, padx=10, pady=10)

    label_hora_fim = tk.Label(root, text="Hora de Fim (Hh:Mm):", bg='gray')
    label_hora_fim.grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
    input_hora_fim = tk.Entry(root, width=30, bg='white', fg='black')
    input_hora_fim.grid(column=1, row=5, padx=10, pady=10)

    botao_inserir = tk.Button(root, text="Inserir Evento", bg='blue', fg='white',
                              command=lambda: adicionar_evento(
                                  input_titulo.get(), input_descricao.get(), input_data_inicio.get(),
                                  input_hora_inicio.get(), input_data_fim.get(), input_hora_fim.get()))
    botao_inserir.grid(column=0, row=6, columnspan=2, padx=10, pady=20)

    root.mainloop()

def adicionar_evento(titulo, descricao, data_inicio, hora_inicio, data_fim, hora_fim):
    try:
        creds = obter_credenciais()
        service = build("calendar", "v3", credentials=creds)
        
        GMT_OFF = '-03:00'  # Hora padrão de Brasília
        inicio = f'{data_inicio}T{hora_inicio}:00{GMT_OFF}'
        fim = f'{data_fim}T{hora_fim}:00{GMT_OFF}'

        evento = {
            'summary': titulo,
            'description': descricao,
            'start': {
                'dateTime': inicio,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': fim,
                'timeZone': 'America/Sao_Paulo',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        evento_inserido = service.events().insert(calendarId='primary', body=evento).execute()
        print(f"Evento criado: {evento_inserido.get('htmlLink')}")
        root.destroy()

    except HttpError as error:
        print(f"Erro ao adicionar o evento: {error}")

def deletar_evento(event_id, painel_evento):
    def deletar_evento_thread():
        try:
            creds = obter_credenciais()
            service = build("calendar", "v3", credentials=creds)

            service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"Evento {event_id} deletado com sucesso!")

            # Destruir o painel do evento após exclusão
            painel_evento.destroy()

        except HttpError as error:
            print(f"Erro ao deletar o evento: {error}")

    # Inicia a thread
    thread = threading.Thread(target=deletar_evento_thread)
    thread.start()
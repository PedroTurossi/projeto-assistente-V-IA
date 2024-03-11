import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from configparser import ConfigParser

def ouvir():
    microfone = sr.Recognizer()

    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print('o rajeh é ')
        audio = microfone.listen(source)
    try:
        frase = microfone.recognize_google(audio, language = "PT-BR")
        print('voce falo:' + frase)
        return frase
    except sr.UnknownValueError:
        print('repete mais devegar')
        return None
def chatbot(texto):
    config = ConfigParser()
    config.read('chave_google.ini')
    api_key = config['API_KEY']['google_api_key']
    genai.configure(api_key=api_key)
    model_gemini = genai.GenerativeModel('gemini-pro')
    promp = "--- "+texto+" (no maximo um paragrafo)---"
    resposta = model_gemini.generate_content(promp)
    return resposta.text
def falar(texto):
    fala = texto
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[0].id)
    rate = speaker.getProperty('rate')
    speaker.setProperty('rate', rate - 25)
    speaker.say(fala)
    print(fala)
    speaker.runAndWait()


frase = ouvir()
conversa =chatbot(frase)
falar(conversa) 
print(conversa)
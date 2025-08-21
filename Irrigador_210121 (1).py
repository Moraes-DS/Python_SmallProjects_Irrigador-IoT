#!/usr/bin/env python3

#BIBLIOTECAS
import time
import datetime
import math
import smtplib
import RPi.GPIO as GPIO
import threading
import time
import datetime
import math
import smtplib
import RPi.GPIO as GPIO
import threading
from time import sleep
from datetime import timedelta

3CONFIGURAÇÃO DA DEFINIÇÃO DOS PINOS DO RASPBERRY PI
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#PINAGEM DO RASPBERRY PI
boia_pin = 5  # terra = 9
led_verm_pin = 13  # terra = 14
led_verd_pin = 22  # terra = 20
solo_pin = 32  # terra = 30
bomba_pin = 23  # terra = 25 NA VERDADE É O PINO DO RELÉ
# O positivo do relé deve ser conectado no pino de 5V do Raspberry pi
led_solo_pin = 37

#CONFIGURAÇÃO DOS PINOS DO RASPBERRY PI
GPIO.setup(boia_pin, GPIO.IN)
GPIO.setup(led_verm_pin, GPIO.OUT)
GPIO.setup(led_verd_pin, GPIO.OUT)
GPIO.setup(solo_pin, GPIO.IN)
GPIO.setup(bomba_pin, GPIO.OUT)
GPIO.setup(led_solo_pin, GPIO.OUT)

#FUNÇÕES
def atualizar_led_umidade(_=None):
    if GPIO.input(solo_pin) == 0: #0 = Solo úmido | 1 = solo seco
        GPIO.output(led_solo_pin, GPIO.HIGH)
    else:
        GPIO.output(led_solo_pin, GPIO.LOW)
atualizar_led_umidade()
GPIO.add_event_detect(solo_pin, GPIO.BOTH, callback=atualizar_led_umidade, bouncetime=1000)

def contador_regressivo(tempo_espera_min):
    """
    Mostra um contador regressivo no formato HH:MM:SS.
    Argumento:
        tempo_espera_min (int): tempo de espera em minutos.
    """
    tempo_espera_seg = tempo_espera_min * 60  # converte minutos para segundos
    
    for restante in range(tempo_espera_seg, 0, -1):
        horas = restante // 3600
        minutos = (restante % 3600) // 60
        segundos = restante % 60
        print(f"\r Tempo restante até religar: {horas:02d}:{minutos:02d}:{segundos:02d}", end="", flush=True)
        time.sleep(1)

#INÍCIO
print("Inicializando a irrigação automática, aguarde...")

while True:
#AGUARDANDO O HORÁRIO DE FUNCIONAMENTO: 8H > funcionamento < 21h
    #Guardando a hora local
    now = datetime.datetime.now()
    hora_agora = now.hour
    print(f"\nAgora são {hora_agora}hs")

    if hora_agora < 8:
        segundos = int(((8 - hora_agora) * 3600) + 5)
        horas_espera1 = (segundos/360)
        print(f"Tempo em segundos: {segundos}")
        print("Aguardando horário ativo (8-21h)-1")
        time.sleep(segundos)

    elif hora_agora >= 21:
        segundos = int((((24 - hora_agora) + 8) * 3600) + 5)
        horas_espera2 = (segundos/360)
        print(f"Tempo em espera: {horas_espera2}")
        print(f"Aguardando horário ativo (8-21h)")
        time.sleep(segundos)
    
#VERIFICAÇÃO DE ÁGUA NO RESERVATÓRIO --> CONTÉM ÁGUA
    elif GPIO.input(boia_pin) == 0:
        now = datetime.datetime.now()
        print("Reservatório com água", now.strftime(f'%d/%m/%Y %H:%M:%S'))
        GPIO.output(led_verd_pin, GPIO.HIGH)
        GPIO.output(led_verm_pin, GPIO.LOW) 
        
#VERIFICAÇÃO DE UMIDADE DO SOLO --> SOLO SECO  
        if GPIO.input(solo_pin) == 1:
            now = datetime.datetime.now()
            print("Solo seco!!! Ligar a Bomba D'água")

#IRRIGAÇÃO
            GPIO.output(bomba_pin, True)  # Ligando a Bomba!
            tempo_led_piscando = 16
            print(f"Bomba ligada por {tempo_led_piscando - 1} segundos!!!", now.strftime(f'%H:%M:%S'))
           
            contador = 0
            #Contador de espera
            while contador < tempo_led_piscando:
                GPIO.output(led_verd_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(led_verd_pin, GPIO.LOW)
                time.sleep(0.5)
                contador = contador + 1
            
            print(f"{tempo_led_piscando - 1} segundos de irrigação...")
            GPIO.output(led_verd_pin, GPIO.HIGH)
            GPIO.output(bomba_pin, False)
            
#ESPERA ATÉ A PRÓXIMA IRRIGAÇÃO
            now = datetime.datetime.now()
            tempo_espera = 360 #Minutos
            tempo_bomba_desligada = (tempo_espera/60)
            print(f"\nBomba desligada... por {tempo_bomba_desligada} horas. Agora são: {now.strftime(f'%H:%M:%S')}")
            contador_regressivo(tempo_espera)
            
#VERIFICAÇÃO DE UMIDADE DO SOLO --> SOLO ÚMIDO               
        else:
            now = datetime.datetime.now()
            GPIO.output(bomba_pin, False)
            tempo_desligada_umido = 240 #Minutos
            print(f"Solo úmido... Bomba desligada por {tempo_desligada_umido / 60} horas. Agora são: {now.strftime(f'%H:%M:%S')}")
            contador_regressivo(tempo_desligada_umido)

#VERIFICAÇÃO DE ÁGUA NO RESERVATÓRIO --> NÃO CONTÉM ÁGUA            
    else:
        now = datetime.datetime.now()
        print("Reservatório vazio! Encher...!!!", now.strftime(f'%H:%M:%S'))
        GPIO.output(led_verd_pin, GPIO.LOW)
        GPIO.output(led_verm_pin, GPIO.HIGH)
        GPIO.output(bomba_pin, False)
        tempo_tentativa_bomba = 240
        print(f"Próxima tentativa de ligar a bomba em {tempo_tentativa_bomba / 60} horas!")
        contador_regressivo(tempo_tentativa_bomba)
        





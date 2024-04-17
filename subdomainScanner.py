#!/usr/bin/python3
import socket,sys,time
import requests

################################################################################
# Titulo    : Subdomain Scanner                                                #
# Versao    : 1.1                                                              #
# Data      : 17/04/2024                                                       #
# Tested on : Linux/Windows10                                                  #
# created by: Charli Castelli.                                                 #
# -----------------------------------------------------------------------------#
# Descrição:                                                                   #
#   Esse programa tem a função de descobrir subdominios.                       #
#   Através de ataque baseado em dicionário (Necessita passar uma wordlist.)   #
# -----------------------------------------------------------------------------#
# Nota da Versão:                                                              #
# Adicionado User-Agent personalizado.                                         #
################################################################################

#Constantes cores
RED   = "\033[1;31m"  
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

#Icones
iconSuccess = BOLD + BLUE + "[+]" + RESET
iconSuccessGreen = GREEN + "[+]" + RESET
iconSuccessRed = RED + "[+]" + RESET
iconSuccessYellow = YELLOW + "[+]" + RESET
iconError = BOLD + RED + "[-]" + RESET
iconHelp = BLUE + "[?]" + RESET

#Menssagens
example = f"{iconError} Exemplo de uso da ferramenta --> " + GREEN + f"python3 {sys.argv[0]} businesscorp.com.br wordlist.txt\n\n" + RESET
close = "\n\n🛑 Execução interrompida pelo usuário!"
stop = f"{iconHelp} Para interromper a execução, pressione Ctrl + C"

#User-Agent personalizado
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

#Banner
print(RED + """
            _         _                       _                                             
           | |       | |                     (_)                                            
  ___ _   _| |__   __| | ___  _ __ ___   __ _ _ _ __    
 / __| | | | '_ \ / _` |/ _ \| '_ ` _ \ / _` | | '_ \  
 \__ \ |_| | |_) | (_| | (_) | | | | | | (_| | | | | |    
 |___/\__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_|    
  ___  ___ __ _ _ __  _ __   ___ _ __
 / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
 \__ \ (_| (_| | | | | | | |  __/ |
 |___/\___\__,_|_| |_|_| |_|\___|_|                                                                                           
                                                                                            
""" + RESET)

def validation():
    #Verificações
    if len(sys.argv) < 2:
        print(f"{example}")
        sys.exit()
    elif len(sys.argv) == 2 or len(sys.argv) < 3:
        print(f"{example}")
        sys.exit()
    elif len(sys.argv) > 3:
        print(f"{example}")
        sys.exit()


def scanner():
    try:
        validation()

        text = f"{iconSuccessGreen} Iniciando varredura no Host: {sys.argv[1]}"
        print(f"{stop}")
        time.sleep(2)
        print(f"{text}\n\n")
        time.sleep(2)

        #Cabeçalho
        print("-"*71)
        print(f'{iconSuccess:<3} {"Subdomínio":<39} {"IP":<20} {"Status":<5}')
        print("-"*71)

        with open(sys.argv[2], "r") as file:
            for result in file:
                host = sys.argv[1] 
                subdomain = (result.strip() + host)    
                try:
                    resolver = socket.gethostbyname(subdomain)
                    try:
                        response = requests.get(f"http://{subdomain}", headers=headers, timeout=5)
                        if response.status_code == 200:
                            print(f"{iconSuccessGreen} {subdomain:.<40}",end="")
                            print(f"{resolver: <20}",end="")
                            print(BOLD + GREEN + f" [{response.status_code}]" + RESET)
                        elif response.status_code == 404:
                            print(f"{iconSuccessRed} {subdomain:.<40}",end="")
                            print(f"{resolver: <20}",end="")
                            print(BOLD + RED + f" [{response.status_code}]" + RESET)
                        elif response.status_code > 399 and response.status_code < 500 and response.status_code != 404:
                            print(f"{iconSuccessYellow} {subdomain:.<40}",end="")
                            print(f"{resolver: <20}",end="")
                            print(BOLD + YELLOW + f" [{response.status_code}]" + RESET)
                        else:
                            print(f"{iconSuccess} {subdomain:.<40}",end="")
                            print(f"{resolver: <20}",end="")
                            print(BOLD + BLUE + f" [{response.status_code}]" + RESET)
                    except requests.exceptions.RequestException:
                        print(f"{iconSuccess} {subdomain:.<40}",end="")
                        print(f"{resolver: <20}")
                        #print() #Se a variavel response não conseguir obter o status-code faz um print() para pular uma linha.
                        
                except socket.gaierror:
                    pass

    except KeyboardInterrupt:
        print(close) #Se o usuário precionar Ctrl + c vai interromper a execução do script.

    print()
    print()

#Função principal
scanner()
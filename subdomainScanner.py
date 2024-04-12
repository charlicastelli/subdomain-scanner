#!/usr/bin/python3
import socket,sys,time
import requests

################################################################################
# Titulo    : Subdomain Scanner                                                #
# Versao    : 1.0                                                              #
# Data      : 10/04/2024                                                       #
# Tested on : Linux/Windows10                                                  #
# created by: Charli Castelli.                                                 #
# -----------------------------------------------------------------------------#
# Descrição:                                                                   #
#   Esse programa tem a função de descobrir subdominios.                       #
#   Necessita passar uma wordlist.                                             #
################################################################################

#Constantes cores
RED   = "\033[1;31m"  
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
BLUE = "\033[34m"
GREEN = "\033[32m"

#Icones
iconSuccess = BOLD + BLUE + "[+]" + RESET
iconSuccessGreen = GREEN + "[+]" + RESET
iconError = BOLD + RED + "[-]" + RESET
iconHelp = BLUE + "[?]" + RESET

#Menssagens
example = f"{iconError} Exemplo de uso da ferramenta --> " + GREEN + f"python3 {sys.argv[0]} businesscorp.com.br wordlist.txt\n\n" + RESET
close = "\n\n🛑 Execução interrompida pelo usuário!"
stop = f"{iconHelp} Para interromper a execução, pressione Ctrl + C"

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

try:
    wordlist = sys.argv[2]
    ip = sys.argv[1]
    infoHost = sys.argv[1]
    text = f"{iconSuccessGreen} Iniciando varredura no Host: {infoHost}"
    print(f"{stop}")
    time.sleep(2)
    print(f"{text}\n\n")
    time.sleep(2)

    #Cabeçalho
    print("-"*71)
    print(f'{iconSuccess:<3} {"Subdomínio":<39} {"IP":<20} {"Status":<5}')
    print("-"*71)
    
    with open(wordlist, "r") as arquivo:
            for resultado in arquivo: 
                    host = (resultado.strip() + ip)    
                    try:
                        socket.gethostbyname(host)
                        print(f"{iconSuccess} {host:.<40}",end="")
                        print(f"{socket.gethostbyname(host): <20}",end="")
                        try:
                            response = requests.get(f"http://{host}", timeout=5)
                            if response.status_code == 200:
                                print(BOLD + GREEN + f" [{response.status_code}]" + RESET)
                            else:
                                print(BOLD + BLUE + f" [{response.status_code}]" + RESET)
                        except requests.exceptions.RequestException:
                            print() #Se a variavel response não conseguir obter o status-code faz um print() para pular uma linha.
                    except socket.gaierror:
                        pass
except KeyboardInterrupt:
    print(close) # Se o usuário precionar Ctrl + c vai interromper a execução do script.

print()
print()
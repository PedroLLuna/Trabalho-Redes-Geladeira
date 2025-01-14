import socket
import time

# Configuração do atuador
HOST = '127.0.0.1'
PORT = 5000

# Identificação do atuador
TIPO_ATUADOR = "LUZ"  # Pode ser "LUZ", "ALARME" ou "REFRIGERADOR"
ID_ATUADOR = "1"  # Identificador único do atuador

def conectar_gerenciador():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        return cliente
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao Gerenciador: {e}")
        return None

def reconectar_gerenciador(cliente):
    print(f"[{TIPO_ATUADOR}] Tentando reconectar ao Gerenciador...")
    return conectar_gerenciador()

def registrar_atuador(cliente):
    mensagem = f"REGISTRAR_ATUADOR {TIPO_ATUADOR} {ID_ATUADOR}"
    cliente.sendall(mensagem.encode('utf-8'))
    print(f"[REGISTRADO] Atuador {TIPO_ATUADOR} com ID {ID_ATUADOR} registrado no Gerenciador.")

def escutar_comandos(cliente):
    while True:
        try:
            comando = cliente.recv(1024).decode('utf-8')
            if not comando:
                break

            # Processa o comando recebido
            print(f"[COMANDO RECEBIDO] {comando}")
            processar_comando(comando)
        except Exception as e:
            print(f"[ERRO] Conexão perdida: {e}")
            cliente = reconectar_gerenciador(cliente)
            if not cliente:
                break

def processar_comando(comando):
    if comando.startswith(f"ACIONAR {TIPO_ATUADOR} {ID_ATUADOR}"):
        acao = comando.split()[-1]
        if acao == "LIGAR":
            print(f"[ATIVO] {TIPO_ATUADOR} está ligado.")
        elif acao == "DESLIGAR":
            print(f"[DESATIVADO] {TIPO_ATUADOR} está desligado.")
        else:
            print(f"[ERRO] Comando inválido: {acao}")
    elif comando.startswith(f"STATUS {TIPO_ATUADOR} {ID_ATUADOR}"):
        print(f"[STATUS] {TIPO_ATUADOR} está ativo.")
    else:
        print(f"[ERRO] Comando não reconhecido para este atuador.")

def iniciar_atuador():
    cliente = conectar_gerenciador()
    if not cliente:
        return

    try:
        registrar_atuador(cliente)
        escutar_comandos(cliente)
    except KeyboardInterrupt:
        print("\n[FINALIZANDO] Atuador encerrado.")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_atuador()

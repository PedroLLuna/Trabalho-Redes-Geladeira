import socket
import threading

# Configuração do Gerenciador
HOST = '127.0.0.1'
PORT = 5000

# Armazena as leituras mais recentes de cada sensor
leituras_sensores = {}

# Armazena os atuadores conectados
atuadores = {}

# Função para lidar com conexões de sensores
def lidar_com_sensor(conexao, endereco):
    print(f"[NOVA CONEXÃO] Sensor conectado: {endereco}")
    try:
        while True:
            mensagem = conexao.recv(1024).decode('utf-8')
            if not mensagem:
                break

            # Processa a mensagem recebida
            print(f"[MENSAGEM RECEBIDA] {mensagem}")
            processar_mensagem(mensagem)
    except Exception as e:
        print(f"[ERRO] Conexão com o sensor encerrada: {e}")
    finally:
        conexao.close()
        print(f"[DESCONECTADO] Sensor desconectado: {endereco}")

# Função para lidar com conexões de atuadores
def lidar_com_atuador(conexao, endereco):
    print(f"[NOVA CONEXÃO] Atuador conectado: {endereco}")
    try:
        while True:
            mensagem = conexao.recv(1024).decode('utf-8')
            if not mensagem:
                break

            # Processa a mensagem recebida
            print(f"[MENSAGEM RECEBIDA] {mensagem}")
            processar_mensagem(mensagem)
    except Exception as e:
        print(f"[ERRO] Conexão com o atuador encerrada: {e}")
    finally:
        conexao.close()
        print(f"[DESCONECTADO] Atuador desconectado: {endereco}")

# Função para processar mensagens recebidas (sensores e atuadores)
def processar_mensagem(mensagem):
    global leituras_sensores
    global atuadores

    partes = mensagem.split()
    if len(partes) < 3:
        print("[ERRO] Mensagem inválida.")
        return

    # Tipos de mensagens esperadas
    if partes[0] == "REGISTRAR":
        tipo_dispositivo = partes[1]
        id_dispositivo = partes[2]
        
        if tipo_dispositivo == "SENSOR":
            print(f"[REGISTRO] Sensor {tipo_dispositivo} com ID {id_dispositivo} registrado.")
        elif tipo_dispositivo == "ATUADOR":
            atuadores[f"{tipo_dispositivo}_{id_dispositivo}"] = partes[1]
            print(f"[REGISTRO] Atuador {tipo_dispositivo} com ID {id_dispositivo} registrado.")
            
    elif partes[0] == "SENSOR":
        tipo_sensor = partes[1]
        id_sensor = partes[2]
        valor = " ".join(partes[3:])
        leituras_sensores[f"{tipo_sensor}_{id_sensor}"] = valor
        print(f"[LEITURA ARMAZENADA] {tipo_sensor} ID {id_sensor}: {valor}")
    
    elif partes[0] == "ACIONAR":
        tipo_atuador = partes[1]
        id_atuador = partes[2]
        acao = partes[3]
        
        chave_atuador = f"{tipo_atuador}_{id_atuador}"
        if chave_atuador in atuadores:
            print(f"[AÇÃO] Atuador {tipo_atuador} ID {id_atuador}: {acao}")
            # Simula a ativação/desativação do atuador
            if acao.lower() == "ligar":
                print(f"Atuador {tipo_atuador} ID {id_atuador} foi ligado.")
            elif acao.lower() == "desligar":
                print(f"Atuador {tipo_atuador} ID {id_atuador} foi desligado.")
            else:
                print(f"[ERRO] Ação desconhecida: {acao}")
        else:
            print(f"[ERRO] Atuador {tipo_atuador} ID {id_atuador} não registrado.")

    else:
        print("[ERRO] Tipo de mensagem desconhecido.")

# Função principal do servidor Gerenciador
def iniciar_gerenciador():
    print("[INICIANDO] Gerenciador em execução...")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f"[ESPERANDO CONEXÕES] Gerenciador ouvindo em {HOST}:{PORT}")

    try:
        while True:
            conexao, endereco = servidor.accept()
            ## BUG ENCONTRADO PELO ICARO: O TIPO DE DISPOSITIVO NÃO ESTÁ INDICANDO SENSOR OU ATUADOR
            ## O TIPO DE DISPOSITIVO ESTÁ VINDO COMO: "REGISTRAR porta 3"
            tipo_dispositivo = conexao.recv(1024).decode('utf-8')  # Recebe o tipo do dispositivo
            ## PARA TESTAR SEM BUGS, DESCOMENTE A LINHA ABAIXO:
            tipo_dispositivo = "SENSOR"
            if tipo_dispositivo == "SENSOR":
                # Inicia uma nova thread para lidar com o sensor
                thread = threading.Thread(target=lidar_com_sensor, args=(conexao, endereco))
            elif tipo_dispositivo == "ATUADOR":
                # Inicia uma nova thread para lidar com o atuador
                thread = threading.Thread(target=lidar_com_atuador, args=(conexao, endereco))
            thread.start()
    except KeyboardInterrupt:
        print("\n[FINALIZANDO] Encerrando o Gerenciador...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_gerenciador()

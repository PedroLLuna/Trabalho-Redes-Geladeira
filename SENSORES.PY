import socket
import time
import random

# Configuração do Gerenciador
GERENCIADOR_HOST = '127.0.0.1'
GERENCIADOR_PORT = 5000

# Classe base para Sensores
class Sensor:
    def __init__(self, tipo, id_sensor):
        self.tipo = tipo
        self.id_sensor = id_sensor
        self.conexao = None

    def conectar_gerenciador(self):
        try:
            self.conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conexao.connect((GERENCIADOR_HOST, GERENCIADOR_PORT))
            print(f"[{self.tipo.upper()}] Conectado ao Gerenciador.")
            self.conexao.sendall(f"REGISTRAR {self.tipo} {self.id_sensor}".encode('utf-8'))
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao Gerenciador: {e}")

    def reconectar_gerenciador(self):
        print(f"[{self.tipo.upper()}] Tentando reconectar ao Gerenciador...")
        self.conectar_gerenciador()

    def enviar_leitura(self, leitura):
        if not self.conexao:
            self.reconectar_gerenciador()
        try:
            mensagem = f"SENSOR {self.tipo} {self.id_sensor} {leitura}"
            self.conexao.sendall(mensagem.encode('utf-8'))
            print(f"[{self.tipo.upper()}] Leitura enviada: {leitura}")
        except Exception as e:
            print(f"[ERRO] Falha ao enviar leitura: {e}")
            self.reconectar_gerenciador()

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
            print(f"[{self.tipo.upper()}] Desconectado do Gerenciador.")

# Sensor de Temperatura Interna
class SensorTemperatura(Sensor):
    def __init__(self, id_sensor):
        super().__init__("temperatura", id_sensor)

    def gerar_leitura(self):
        # Simula uma temperatura entre -5°C e 10°C
        return round(random.uniform(-5, 10), 2)

# Sensor de Nível de Estoque
class SensorEstoque(Sensor):
    def __init__(self, id_sensor):
        super().__init__("estoque", id_sensor)

    def gerar_leitura(self):
        # Simula um nível de estoque entre 0% e 100%
        return random.randint(0, 100)

# Sensor de Status da Porta
class SensorPorta(Sensor):
    def __init__(self, id_sensor):
        super().__init__("porta", id_sensor)

    def gerar_leitura(self):
        # Simula o status da porta: "ABERTA" ou "FECHADA"
        return random.choice(["ABERTA", "FECHADA"])

# Função principal para rodar os sensores
def iniciar_sensores():
    sensores = [
        SensorTemperatura(id_sensor=1),
        SensorEstoque(id_sensor=2),
        SensorPorta(id_sensor=3)
    ]

    # Conectar sensores ao Gerenciador
    for sensor in sensores:
        sensor.conectar_gerenciador()

    try:
        while True:
            for sensor in sensores:
                leitura = sensor.gerar_leitura()
                sensor.enviar_leitura(leitura)
            time.sleep(10)  # Envia leituras a cada 10 segundos
    except KeyboardInterrupt:
        print("\n[FINALIZANDO] Desconectando sensores...")
        for sensor in sensores:
            sensor.desconectar()

if __name__ == "__main__":
    iniciar_sensores()

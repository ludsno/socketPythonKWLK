import socket

# Configurações do cliente
PORT = 12345

def obter_ip_local():
    """
    Detecta automaticamente o IP local da máquina para uso em rede local.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectando-se a um servidor externo para descobrir o IP local
        s.connect(("8.8.8.8", 80))  # Usando o Google DNS para uma conexão de rede
        ip_local = s.getsockname()[0]  # Obtém o IP da máquina
    finally:
        s.close()
    return ip_local

def jogar_wordle(client):
    print(client.recv(1024).decode('utf-8'))  # Exibe a mensagem inicial do servidor

    while True:
        tentativa = input("Digite sua tentativa (5 letras): ").strip().lower()
        
        if len(tentativa) != 5:
            print("Por favor, insira uma palavra de exatamente 5 letras.")
            continue

        client.send(tentativa.encode('utf-8'))
        resposta = client.recv(1024).decode('utf-8')
        print(resposta)

        if "Parabéns" in resposta or "Game over" in resposta:
            break

def main():
    print("Bem-vindo ao jogo definitelyNotWordle!")
    
    # Solicita o IP do servidor ao usuário
    host = input("Digite o IP do servidor para conectar (pode ser 127.0.0.1 se local): ").strip()
    ip_local = obter_ip_local()  # Obtém o IP local da máquina
    print(f"Conectando ao servidor com o IP local: {ip_local}")

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, PORT))  # Conecta-se ao servidor
            jogar_wordle(client)
        except ConnectionError:
            print("Erro de conexão com o servidor. Tente novamente mais tarde.")
            break
        finally:
            client.close()

        jogar_novamente = input("Deseja jogar novamente? (s/n): ").strip().lower()
        if jogar_novamente != 's':
            print("Obrigado por jogar! Até a próxima.")
            break

if __name__ == "__main__":
    main()

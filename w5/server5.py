import socket
import threading
import random

# Configurações do servidor
HOST = ''  # Permite que o servidor aceite conexões de qualquer IP na rede local
PORT = 12345  # Porta na qual o servidor vai escutar

# Lista de palavras para o jogo
palavras = [
    'luzes', 'moral', 'navio', 'outra', 'prato', 'quase', 'rumor', 'sabor', 'treno', 'urubu',
    'vigor', 'xales', 'zíper', 'acaso', 'barco', 'chuva', 'dedos', 'fugaz', 'globo', 'honra',
    'ideia', 'janta', 'lobby', 'manso', 'nuvem', 'ojiva', 'pacto', 'quilo', 'rival', 'suave',
    'tarde', 'urgir', 'vista', 'xampu', 'abalo', 'baixa', 'cegas', 'dados', 'falso', 'gosto',
    'haste', 'inata', 'juros', 'limpo', 'mover', 'nível', 'oásis', 'plano', 'quero', 'ruiva',
    'atual', 'beijo', 'carta', 'dente', 'feroz', 'genro', 'haste', 'inova', 'judeu', 'laico',
    'mural', 'ninja', 'ordem', 'páreo', 'renda', 'salve', 'tempo', 'vazio', 'abriu', 'brisa',
    'corpo', 'deusa', 'finca', 'grato', 'hobby', 'inter', 'justo', 'litro', 'macho', 'nobre',
    'opaco', 'prazo', 'quase', 'reino', 'senso', 'turma', 'valer', 'xeque', 'zorra', 'amplo',
    'brejo', 'caixa', 'digno', 'farol', 'gente', 'hífen', 'inato', 'jovem', 'letal', 'morte'
]

def obter_ipv4_local():
    """
    Detecta o endereço IPv4 da máquina no qual o servidor está sendo executado.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    try:
        # Conectando-se a um servidor externo para descobrir o IP local
        s.connect(("8.8.8.8", 80))  # Usando o Google DNS para uma conexão de rede
        ip_local = s.getsockname()[0]  # Obtém o IP da máquina
    finally:
        s.close()  # Fecha o socket
    return ip_local

def verificar_palavra(palavra_secreta, tentativa):
    """
    Verifica a tentativa do jogador e retorna um feedback com quadrados ao redor das letras.
    """
    feedback = ""

    COR_CORRETA = '\033[32m'  # Verde para letras corretas
    COR_POSICAO_ERRADA = '\033[33m'  # Amarelo para letras corretas mas na posição errada
    COR_INCORRETA = '\033[31m'  # Vermelho para letras incorretas
    RESET = '\033[0m'  # Reset para cor padrão

    for i in range(len(palavra_secreta)):
        letra = tentativa[i].upper()
        # Adicionando quadrado ao redor da letra
        if tentativa[i] == palavra_secreta[i]:
            feedback += f"{COR_CORRETA}[ {letra} ]{RESET}"  # Letra correta na posição correta
        elif tentativa[i] in palavra_secreta:
            feedback += f"{COR_POSICAO_ERRADA}[ {letra} ]{RESET}"  # Letra correta na posição errada
        else:
            feedback += f"{COR_INCORRETA}[ * ]{RESET}"  # Letra incorreta
    return feedback


def gerenciar_cliente(conn, addr):
    """
    Gerencia a conexão com um cliente.
    """
    print(f"Cliente conectado: {addr}")

    while True:
        palavra_secreta = random.choice(palavras)  # Escolhe uma palavra aleatória
        tentativas_restantes = 6  # Número de tentativas permitidas
        conn.send(f"Bem-vindo ao definitelyNotWordle! Tente adivinhar a palavra de {len(palavra_secreta)} letras.".encode('utf-8'))

        while tentativas_restantes > 0:
            try:
                tentativa = conn.recv(1024).decode('utf-8').strip().lower()  # Recebe a tentativa do cliente

                if tentativa == palavra_secreta:
                    conn.send("Parabéns! Você acertou a palavra! Deseja jogar novamente? (s/n)".encode('utf-8'))
                    break
                else:
                    tentativas_restantes -= 1
                    feedback = verificar_palavra(palavra_secreta, tentativa)  # Verifica a tentativa
                    mensagem = f"Tentativa: {feedback} | Tentativas restantes: {tentativas_restantes}"
                    conn.send(mensagem.encode('utf-8'))  # Envia o feedback para o cliente

            except ConnectionError:
                print(f"Conexão perdida com {addr}")
                conn.close()
                return

        if tentativas_restantes == 0:
            conn.send(f"Game over! A palavra era '{palavra_secreta}'. Deseja jogar novamente? (s/n)".encode('utf-8'))

        try:
            resposta = conn.recv(1024).decode('utf-8').strip().lower()  # Recebe a resposta do cliente
            if resposta != 's':
                conn.send("Obrigado por jogar! Até a próxima.".encode('utf-8'))
                break
        except ConnectionError:
            print(f"Conexão encerrada inesperadamente com {addr}")
            break

    conn.close()  # Fecha a conexão com o cliente

def iniciar_servidor():
    """
    Inicia o servidor e aguarda conexões de clientes.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    server.bind((HOST, PORT))  # Associa o socket ao endereço e porta
    server.listen(5)  # Habilita o servidor a aceitar conexões

    ip_local = obter_ipv4_local()  # Obtém o IP local da máquina
    print(f"Servidor iniciado em {ip_local}:{PORT}. Aguardando conexões...")

    try:
        while True:
            conn, addr = server.accept()  # Aceita uma nova conexão
            threading.Thread(target=gerenciar_cliente, args=(conn, addr)).start()  # Cria uma nova thread para gerenciar o cliente
    except KeyboardInterrupt:
        print("Servidor encerrado.")

iniciar_servidor()  # Inicia o servidor

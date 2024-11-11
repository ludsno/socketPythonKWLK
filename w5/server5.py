import socket
import threading
import random

# Configurações do servidor
HOST = ''  # Permite que o servidor aceite conexões de qualquer IP na rede local
PORT = 12345

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectando-se a um servidor externo para descobrir o IP local
        s.connect(("8.8.8.8", 80))  # Usando o Google DNS para uma conexão de rede
        ip_local = s.getsockname()[0]  # Obtém o IP da máquina
    finally:
        s.close()
    return ip_local

def verificar_palavra(palavra_secreta, tentativa):
    feedback = ""
    for i in range(len(palavra_secreta)):
        if tentativa[i] == palavra_secreta[i]:
            feedback += tentativa[i].upper()
        elif tentativa[i] in palavra_secreta:
            feedback += tentativa[i].lower()
        else:
            feedback += "*"
    return feedback

def gerenciar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")

    while True:
        palavra_secreta = random.choice(palavras)
        tentativas_restantes = 6
        conn.send(f"Bem-vindo ao definitelyNotWordle! Tente adivinhar a palavra de {len(palavra_secreta)} letras.".encode('utf-8'))

        while tentativas_restantes > 0:
            try:
                tentativa = conn.recv(1024).decode('utf-8').strip().lower()

                if tentativa == palavra_secreta:
                    conn.send("Parabéns! Você acertou a palavra! Deseja jogar novamente? (s/n)".encode('utf-8'))
                    break
                else:
                    tentativas_restantes -= 1
                    feedback = verificar_palavra(palavra_secreta, tentativa)
                    mensagem = f"Tentativa: {feedback} | Tentativas restantes: {tentativas_restantes}"
                    conn.send(mensagem.encode('utf-8'))

            except ConnectionError:
                print(f"Conexão perdida com {addr}")
                conn.close()
                return

        if tentativas_restantes == 0:
            conn.send(f"Game over! A palavra era '{palavra_secreta}'. Deseja jogar novamente? (s/n)".encode('utf-8'))

        try:
            resposta = conn.recv(1024).decode('utf-8').strip().lower()
            if resposta != 's':
                conn.send("Obrigado por jogar! Até a próxima.".encode('utf-8'))
                break
        except ConnectionError:
            print(f"Conexão encerrada inesperadamente com {addr}")
            break

    conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    ip_local = obter_ipv4_local()  # Obtém o IP local da máquina
    print(f"Servidor iniciado em {ip_local}:{PORT}. Aguardando conexões...")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=gerenciar_cliente, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Servidor encerrado.")

iniciar_servidor()

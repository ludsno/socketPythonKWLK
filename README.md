
# definitelyNotWordle - README

## Sobre o Jogo

`definitelyNotWordle` é um joginho de palavras onde os jogadores tentam adivinhar uma palavra secreta de 5 letras. 
O servidor escolhe uma palavra aleatória e fornece feedback sobre as letras e suas posições a cada tentativa 
do cliente. O jogo é implementado em Python e utiliza sockets para comunicação entre cliente e servidor em 
rede local.

## Estrutura do Código

O projeto é composto por dois arquivos principais:
- **Servidor**: Controla a lógica do jogo, escolhe uma palavra secreta, envia feedback ao cliente e gerencia conexões.
- **Cliente**: Envia tentativas de palavras ao servidor e exibe o feedback recebido.

## Pré-requisitos

- Python 3.x
- Ambas as máquinas (servidor e cliente) devem estar conectadas na mesma rede local para permitir a comunicação direta por IP.

## Como Iniciar o Jogo

### Passo 1: Iniciar o Servidor
1. No terminal, execute o script do servidor:
   ```bash
   python servidor.py
   ```
2. O servidor exibe o IP local e a porta em que está escutando. Exemplo:
   ```
   Servidor iniciado em 192.168.x.x:12345. Aguardando conexões...
   ```

### Passo 2: Conectar o Cliente ao Servidor
1. Em uma outra máquina na mesma rede (ou na mesma máquina usando `127.0.0.1`), execute o script do cliente:
   ```bash
   python cliente.py
   ```
2. Insira o IP do servidor exibido no passo 1 (ou `127.0.0.1` se estiver executando o cliente e o servidor na mesma máquina).
3. O cliente se conecta ao servidor e inicia o jogo.

### Exemplo de Jogo
1. O cliente insere uma tentativa de palavra de 5 letras.
2. O servidor responde com feedback indicando quais letras estão corretas e em suas posições exatas, corretas mas em posições erradas, ou incorretas.
3. Se o jogador acertar a palavra ou esgotar as tentativas, o jogo termina.

## Detalhes Técnicos

### Configuração do Servidor (`servidor.py`)
- O servidor usa o protocolo TCP/IP para comunicação e escuta conexões na porta 12345.
- As palavras secretas são escolhidas aleatoriamente de uma lista.
- Cada cliente recebe feedback detalhado sobre suas tentativas, com letras corretas em maiúsculas, letras corretas em posições erradas em minúsculas e caracteres `*` para letras incorretas.

### Configuração do Cliente (`cliente.py`)
- O cliente solicita o IP do servidor e conecta-se à porta 12345.
- Envia tentativas de palavras e exibe feedback recebido do servidor até acertar a palavra ou esgotar as tentativas.

## Exemplo de Sessão de Jogo

1. **Servidor** inicia e exibe o IP local.
   ```bash
   Servidor iniciado em 192.168.0.10:12345. Aguardando conexões...
   ```

2. **Cliente** se conecta, insere tentativas e recebe feedback:
   ```plaintext
   Bem-vindo ao jogo definitelyNotWordle!
   Digite sua tentativa (5 letras): moral
   Tentativa: MOR** | Tentativas restantes: 5
   ```

3. O cliente continua tentando até acertar ou acabar as tentativas. Ao final, o servidor oferece a opção de jogar novamente.

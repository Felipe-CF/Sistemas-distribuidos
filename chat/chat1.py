import socket, time

# MEU_IP = '127.0.0.1'
PORTA = 8000

MEU_IP = input('digite o IP do servidor: ')

# Criar o socket TCP
conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

udp_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Conectar ao servidor TCP
try: 
    DESTINO = (MEU_IP, PORTA)

    conexao.connect(DESTINO)

    porta_udp = conexao.recv(1024) # espera a resposta

    porta_udp = int(porta_udp.decode('utf-8'))

    udp_servidor.bind(('127.0.0.1', porta_udp)) 

    print(f"Conectado ao servidor")

    while True:

        mensagem = input('Digite sua mensagem: ')

        conexao.sendall(mensagem.encode('utf-8'))

        if mensagem == 'sair':
            print('chat encerrado')

            conexao.close()

            break

        dados, origem = udp_servidor.recvfrom(1024) 

        if not dados or dados.decode('utf-8') != 'sair':
            print(dados.decode('utf-8'))
            
        else:
            print('chat encerrado')
            conexao.close()
            break
        
except socket.error as e:

    print(f"Erro ao conectar ao servidor: {e}")

    exit()




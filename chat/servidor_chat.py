import socket, time


# MEU_IP = '127.0.0.1'
PORTA1 = 8000
PORTA2 = 8002

MEU_IP = input('digite seu IP: ')

tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

DESTINO1 = (MEU_IP, PORTA1)

DESTINO2 = (MEU_IP, PORTA2)

tcp1.bind(DESTINO1)  

tcp2.bind(DESTINO2)  

tcp1.listen(1)   

tcp2.listen(1)   

try:
    print('esperando conexao1')
    conexao1, add_chat1 = tcp1.accept() 

    conexao1.sendall(str(add_chat1[1]+1).encode('utf-8'))

    print('esperando conexao2')
    conexao2, add_chat2 = tcp2.accept() 

    conexao2.sendall(str(add_chat2[1]+2).encode('utf-8'))

    while True:

        mensagem1 = conexao1.recv(1024)

        print('mensagem: conexão 1')

        udp.sendto(mensagem1, (add_chat2[0], add_chat2[1] + 2))

        if not mensagem1 or mensagem1.decode('utf-8') == 'sair':
            print('conexão 1 encerrada')
            break

        mensagem2 = conexao2.recv(1024) 

        print('mensagem: conexão 2')

        udp.sendto(mensagem2, (add_chat1[0], add_chat1[1] + 1))

        if not mensagem2 or mensagem2.decode('utf-8') == 'sair':
            print('conexão 2 encerrada')
            break

except socket.error as e:

    print(f"Erro ao conectar ao servidor: {e}")

    exit()


finally:

    conexao1.close()

    conexao2.close()


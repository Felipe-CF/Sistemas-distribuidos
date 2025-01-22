import grpc
import teste_pb2 as pb2
import teste_pb2_grpc as pb2_grpc

def run():
    canal = grpc.insecure_channel("localhost:8000")

    stub = pb2_grpc.DandoOiStub(canal)

    requisicao = pb2.OiRequest(name="oi")

    resposta = stub.Falando(requisicao)

    print(f"Mensagem do servidor: {resposta.mensagem}")

if __name__ == "__main__":
    run()
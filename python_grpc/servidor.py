import grpc
import teste_pb2_grpc as pb2_grpc
import teste_pb2 as pb2
from concurrent import futures

class DandoOiService(pb2_grpc.DandoOiServicer):
    def Falando(self, request, context):
        # Acessa o campo 'name' da requisição e envia uma resposta
        return pb2.OiResposta(mensagem=f"Olá, {request.name}!")

def serve():
    # Criando o servidor gRPC com um pool de threads
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registrando o serviço no servidor
    pb2_grpc.add_DandoOiServicer_to_server(DandoOiService(), servidor)
    
    # Iniciando o servidor na porta 8000
    servidor.add_insecure_port('[::]:8000')
    servidor.start()
    print("Servidor gRPC iniciado na porta 8000.")
    servidor.wait_for_termination()

if __name__ == "__main__":
    serve()

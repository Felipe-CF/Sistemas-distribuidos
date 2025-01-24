import grpc
import ProtoBUffer_pb2_grpc as pb2_grpc
import ProtoBUffer_pb2 as pb2
import os
from concurrent import futures


class UploadServicoServicer(pb2_grpc.UploadServicoServicer):  
    def ServicoUploadArquivo(self, request, context):

        caminho_arquivo = os.path.join("recebidos", request.nome)

        # Verifica se o arquivo já existe para evitar sobrescrita
        if os.path.exists(caminho_arquivo):
            return pb2.UploadResposta(mensagem=f"Erro: O arquivo {request.nome} já existe!")

        # Abre o arquivo em modo de escrita binária e grava os bytes
        with open(caminho_arquivo, "wb") as f:
            f.write(request.conteudo)

        # Confirma o recebimento do arquivo e envia uma resposta de sucesso
        print(f"Arquivo {request.nome} salvo com sucesso em {caminho_arquivo}")
        
        return pb2.UploadResposta(mensagem=f"Arquivo {request.nome} recebido e salvo com sucesso!")

def serve():
    # Criando o servidor gRPC com um pool de threads
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registrando o serviço de upload no servidor
    pb2_grpc.add_UploadServicoServicer_to_server(UploadServicoServicer(), servidor)  
    
    # Iniciando o servidor na porta 8000
    servidor.add_insecure_port('[::]:8000')
    servidor.start()
    print("Servidor gRPC iniciado na porta 8000.")
    servidor.wait_for_termination()

if __name__ == "__main__":
    serve()

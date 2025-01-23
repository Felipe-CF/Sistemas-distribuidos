using Grpc.Net.Client;
using ProjetoGrpc; // O namespace gerado pelo seu arquivo .proto
using Google.Protobuf;
using System;
using System.IO;
using System.Threading.Tasks;

namespace ProjetoGrpc;

class Program
{
    static async Task Main(string[] args)
    {
        // Cria o canal de comunicação com o servidor Python na porta 50051
        var canal = GrpcChannel.ForAddress("http://localhost:8000"); // Use GrpcChannel

        // Cria o cliente gRPC para o serviço UploadServico
        var cliente = new UploadServico.UploadServicoClient(canal);  // Ajustado para o nome do serviço no .proto

        // Caminho do arquivo que você quer enviar
        string filePath = "C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\python_grpc\\teste.mp4";  // Substitua pelo caminho real do arquivo

        // Lê o arquivo como um array de bytes
        byte[] fileBytes = File.ReadAllBytes(filePath);

        // Cria a requisição com o nome e conteúdo do arquivo
        var requisicao = new DadosArquivo
        {
            Nome = Path.GetFileName(filePath),
            Conteudo = Google.Protobuf.ByteString.CopyFrom(fileBytes)  // Converte o conteúdo para ByteString
        };

        // Envia o arquivo para o servidor Python
        var resposta = await cliente.ServicoUploadArquivoAsync(requisicao);  // Método do serviço no .proto

        // Exibe a resposta do servidor
        Console.WriteLine($"Resposta do servidor: {resposta.Mensagem}");

        // O canal é encerrado automaticamente ao sair do escopo
    }
}
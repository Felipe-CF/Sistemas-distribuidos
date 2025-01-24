using Grpc.Net.Client;
using System;
using System.IO;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // O endereço do servidor gRPC
        var canal = GrpcChannel.ForAddress("http://localhost:8000");

        // Cria o cliente de serviço usando a classe gerada
        var cliente = new ProjetoGrpc.UploadServico.UploadServicoClient(canal); 

        // Lê o arquivo que você quer enviar
        // string caminho_arquivo = @"C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\python_grpc\\enviar\\teste.mp4";
        // string caminho_arquivo = @"C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\python_grpc\\enviar\\teste.txt";
        string caminho_arquivo = @"C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\python_grpc\\enviar\\KASINAO.mp4";
        // string caminho_arquivo = @"C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\python_grpc\\enviar\\leao.jpg";

        byte[] fileBytes = File.ReadAllBytes(caminho_arquivo);

        // Cria a requisição para o servidor
        var request = new ProjetoGrpc.DadosArquivo
        {
            Nome = Path.GetFileName(caminho_arquivo),
            Conteudo = Google.Protobuf.ByteString.CopyFrom(fileBytes)
        };

        // Chama o método ServicoUploadArquivo no servidor gRPC
        var response = await cliente.ServicoUploadArquivoAsync(request); 

        // Mostra a resposta do servidor
        Console.WriteLine("Resposta Servidor: " + response.Mensagem);

        // Fechar o canal de comunicação
        await canal.ShutdownAsync();
    }
}

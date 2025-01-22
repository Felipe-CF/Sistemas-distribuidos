using Grpc.Core;
using MeuProjetoGrpc.Services;
using Microsoft.AspNetCore.Builder; // Para WebApplication
using Microsoft.Extensions.DependencyInjection; // Para AddGrpc


namespace MeuProjetoGrpc; // Corrija o nome do namespace para corresponder ao nome do projeto

public class Program
{
    public static void Main(string[] args) // Adicione o parâmetro args
    {
        var builder = WebApplication.CreateBuilder(args);
        
        // Adiciona o serviço gRPC ao contêiner de serviços
        builder.Services.AddGrpc();

        var app = builder.Build();

        // Mapeia o serviço gRPC para o pipeline de requisições
        app.MapGrpcService<BlogPostsService>();

        // Configura um endpoint HTTP para verificar se o servidor está funcionando
        app.MapGet("/", () => "Servidor gRPC em execução. Acesse /grpc para interagir com os serviços.");

        // Inicia o servidor
        app.Run();
    }
}
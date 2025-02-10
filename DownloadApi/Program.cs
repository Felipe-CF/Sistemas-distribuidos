using System.Text;
using System.Xml.Serialization;
using ApiUpload;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers().AddXmlSerializerFormatters();

var api = builder.Build();

api.UseHttpsRedirection();

// Endpoint para baixar o arquivo via XML
api.MapGet("/download", async (HttpContext context) =>
{
    try
    {
        Console.WriteLine("1. Iniciando processamento da requisição");
        
        using var reader_request = new StreamReader(context.Request.Body, Encoding.UTF8);
        var xmlContent = await reader_request.ReadToEndAsync();
        
        Console.WriteLine("2. XML recebido:");

        var serializer = new XmlSerializer(typeof(DeleteRequest));
        
        Console.WriteLine("3. Iniciando desserialização");
        using var stringReader = new StringReader(xmlContent);
        
        Console.WriteLine("4. Desserializando XML");
        var request = (DownloadRequest?)serializer.Deserialize(stringReader);
        
        Console.WriteLine("5. Desserialização concluída");

        if (request == null)
        {
            Console.WriteLine("6. Requisição é nula");
            return Results.BadRequest("Formato XML inválido");
        }

        Console.WriteLine($"7. FileName: {request.FileName}");

        string filePath = Path.Combine(@"C:\Users\FelipeCF\Desktop\Codigos\Sistemas-distribuidos\ApiUpload\uploads", request.FileName);


        if(!File.Exists(filePath)){
            Console.WriteLine("8. Arquivo não encontrado");
            return Results.NotFound($"Arquivo '{request.FileName}' não encontrado");
        }

        // Lê o arquivo do dir uploads
        byte[] fileBytes = await File.ReadAllBytesAsync(filePath);
        
        Console.WriteLine("9. Arquivo carregado com sucesso");

        // retorna o arquivo com resposta
        return Results.File(fileBytes, "application/octet-stream", request.FileName);
    }
    catch(Exception ex)
    {
        Console.WriteLine($"Erro: {ex.Message}");
        Console.WriteLine($"StackTrace: {ex.StackTrace}");
        return Results.Problem($"Erro ao processar a requisição: {ex.Message}");
    }
});

// Endpoint para deletar o arquivo via XML
api.MapPost("/delete", async (HttpContext context) =>
{
    try
    {
        using var reader_request = new StreamReader(context.Request.Body, Encoding.UTF8);
        var xmlContent = await reader_request.ReadToEndAsync();

        var serializer = new XmlSerializer(typeof(DeleteRequest));
        using var stringReader = new StringReader(xmlContent);
        var request = (DeleteRequest?)serializer.Deserialize(stringReader);

        if (request == null)
            return Results.BadRequest("Formato XML inválido");

        string filePath = Path.Combine(@"C:\Users\FelipeCF\Desktop\Codigos\Sistemas-distribuidos\ApiUpload\uploads", request.FileName);

        if (!File.Exists(filePath))
            return Results.NotFound($"Arquivo '{request.FileName}' não encontrado");

        File.Delete(filePath);

        return Results.Ok($"Arquivo '{request.FileName}' deletado com sucesso");
    }
    catch (Exception ex)
    {
        return Results.Problem($"Erro ao processar a requisição: {ex.Message}");
    }
});


api.Run();

using System.Text;
using System.Xml.Linq;
using System.Xml.Serialization;
using ApiUpload;

// criação da API
var builder = WebApplication.CreateBuilder(args);

// Adiciona o suporte ao XML para o controlador serializar e desserializar XML
builder.Services.AddControllers().AddXmlSerializerFormatters();

var api = builder.Build();

api.UseHttpsRedirection();



// Endpoint para salvar o arquivo via XML
api.MapPost("/upload", async (HttpContext context) =>
{
    try
    {
        Console.WriteLine("1. Iniciando processamento da requisição");
        
        using var reader_request = new StreamReader(context.Request.Body, Encoding.UTF8);
        var xmlContent = await reader_request.ReadToEndAsync();
        
        Console.WriteLine("2. XML recebido:");

        var serializer = new XmlSerializer(typeof(FileUploadRequest));
        
        Console.WriteLine("3. Iniciando desserialização");
        using var stringReader = new StringReader(xmlContent);
        
        Console.WriteLine("4. Desserializando XML");
        var request = (FileUploadRequest?)serializer.Deserialize(stringReader);
        
        Console.WriteLine("5. Desserialização concluída");

        if (request == null)
        {
            Console.WriteLine("6. Requisição é nula");
            return Results.BadRequest("Formato XML inválido");
        }

        Console.WriteLine($"7. FileName: {request.FileName}");
        Console.WriteLine($"8. FileContent length: {request.FileContent?.Length ?? 0}");

        byte[] fileBytes = Convert.FromBase64String(request.FileContent);
        
        Console.WriteLine("9. Base64 convertido para bytes");

        string filePath = Path.Combine("uploads", request.FileName);
        Directory.CreateDirectory("uploads");
        
        Console.WriteLine($"10. Salvando arquivo em: {filePath}");
        File.WriteAllBytes(filePath, fileBytes);
        
        Console.WriteLine("11. Arquivo salvo com sucesso");

        return Results.Content(
            new XElement("Response", 
            new XElement("Message", $"Arquivo '{request.FileName}' salvo com sucesso")).ToString(),
            "application/xml"
        );
    }
    catch(Exception ex)
    {
        Console.WriteLine($"Erro: {ex.Message}");
        Console.WriteLine($"StackTrace: {ex.StackTrace}");
        return Results.Problem($"Erro ao salvar o arquivo: {ex.Message}");
    }
});

api.Run();

using CoreWCF; // criar serviços SOAP
using CoreWCF.Configuration; // configurar serviços WCF
using CoreWCF.Description; // classes para descrever e expor metadados do serviço (como o WSDL)

// permite configurar a aplicação antes de rodá-la 
var builder = WebApplication.CreateBuilder(args); 

builder.Services.AddServiceModelServices(); // registra os serviços do CoreWCF

builder.Services.AddServiceModelMetadata(); // habilita WSDL, Sem isso, a URL `?wsdl` não funcionaria

// cria a aplicação com base nas configurações feitas acima
var app = builder.Build(); 


app.UseServiceModel(serviceBuilder =>
{
    // adiciona a implementação dos serviços SOAP 
    serviceBuilder.AddService<UploadServico>(); 

    serviceBuilder.AddService<DeleteServico>(); 

    serviceBuilder.AddService<DownloadServico>();

    serviceBuilder.AddService<TesteServico>(); 

    var binding = new BasicHttpBinding
    {
    MaxReceivedMessageSize = 50 * 1024 * 1024,  // 50 MB
    MaxBufferSize = 50 * 1024 * 1024,           // 50 MB
    ReaderQuotas = System.Xml.XmlDictionaryReaderQuotas.Max  // Aumenta os limites de leitura
};
    // endpoints para os serviços SOAP, BasicHttpBinding() indica que usuará o protocolo SOAP
    serviceBuilder.AddServiceEndpoint<UploadServico, IUploadServico>(binding, "/UploadServico");

    serviceBuilder.AddServiceEndpoint<DownloadServico, IDownloadServico>(new BasicHttpBinding(), "/DownloadServico");

    serviceBuilder.AddServiceEndpoint<DeleteServico, IDeleteServico>(new BasicHttpBinding(), "/DeleteServico");

    serviceBuilder.AddServiceEndpoint<TesteServico, ITesteServico>(new BasicHttpBinding(), "/TesteServico");

    // Habilita metadados WSDL para o acesso do cliente
    var serviceMetadataBehavior = app.Services.GetRequiredService<ServiceMetadataBehavior>();

    serviceMetadataBehavior.HttpGetEnabled = true; // Permite acesso ao metadado do WSDL
});





app.Run(); // a api começa a rodar

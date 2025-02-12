using CoreWCF;

[ServiceContract(Namespace = "http://tempuri.org/")]
public interface IUploadServico
{
    [OperationContract]
    string UploadArquivo(string nomeArquivo, byte[] conteudoArquivo);
}


[ServiceContract(Namespace = "http://tempuri.org/")]
public interface IDownloadServico
{
    [OperationContract]
    byte[] DownloadArquivo(string nomeArquivo);
}

[ServiceContract(Namespace = "http://tempuri.org/")]
public interface IDeleteServico
{
    [OperationContract]
    string DeleteArquivo(string nomeArquivo);
}

[ServiceContract(Namespace = "http://tempuri.org/")]
public interface ITesteServico
{
    [OperationContract]
    string TesteArquivo();
}




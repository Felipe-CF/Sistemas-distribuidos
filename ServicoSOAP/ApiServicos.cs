
public class UploadServico : IUploadServico
{
    private readonly string uploadPath = Path.Combine(Directory.GetCurrentDirectory(), "uploads");

    public string UploadArquivo(string nomeArquivo, byte[] conteudoArquivo)
    {
        try
        {
            if (!Directory.Exists(uploadPath))
            {
                Directory.CreateDirectory(uploadPath);
            }

            string filePath = Path.Combine(uploadPath, nomeArquivo);

            File.WriteAllBytes(filePath, conteudoArquivo);

            return $"Arquivo '{nomeArquivo}' salvo com sucesso em {filePath}";
        }
        catch (Exception ex)
        {
            return $"Erro ao salvar o arquivo: {ex.Message}";
        }
    }
}

public class DownloadServico : IDownloadServico
{
    private readonly string uploadPath = Path.Combine(Directory.GetCurrentDirectory(), "uploads");

    public byte[] DownloadArquivo(string nomeArquivo)
    {
        try
        {
            if (!Directory.Exists(uploadPath))
                throw new Exception("Diretorio 'uploads' não existe");

            string filePath = Path.Combine(uploadPath, nomeArquivo);

            if(!File.Exists(filePath))
                throw new Exception("o arquivo não existe");

            return File.ReadAllBytes(filePath);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Erro ao baixar o arquivo: {ex.Message}");
            return (new byte[0]);
        }
    }
}

public class DeleteServico : IDeleteServico
{
    private readonly string uploadPath = Path.Combine(Directory.GetCurrentDirectory(), "uploads");

    public string DeleteArquivo(string nomeArquivo)
    {
        try
        {
            if (!Directory.Exists(uploadPath))
                throw new Exception("Diretorio 'uploads' não existe");

            string filePath = Path.Combine(uploadPath, nomeArquivo);

            if(!File.Exists(filePath))
                throw new Exception("o arquivo não existe");

            File.Delete(filePath);

            if(!File.Exists(filePath))
                return "Arquivo foi deletado com sucesso!";

            else
                throw new Exception("o arquivo não foi deletado");

        }
        catch (Exception ex)
        {
            return $"Erro ao deletar o arquivo: {ex.Message}";
        }
    }
}

public class TesteServico : ITesteServico
{

    public string TesteArquivo()
    {
            return "sucesso!";
    }
}


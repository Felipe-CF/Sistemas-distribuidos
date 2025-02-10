using System.Xml.Serialization;

namespace ApiUpload;

// será usada para desserializar os dados do XML recebidos na requisição.
[XmlRoot("FileUploadRequest")]
public class FileUploadRequest
{
    public FileUploadRequest() { }  // Construtor necessário para XmlSerializer

    // Atributo XmlElement define como os elementos do XML serão mapeados para as propriedades da classe.
    [XmlElement("FileName")] 
    public string FileName { get; set; } = string.Empty;

    [XmlElement("FileContent")]
    public string FileContent { get; set; } = string.Empty;
}
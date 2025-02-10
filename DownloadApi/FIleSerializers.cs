using System.Xml.Serialization;

namespace ApiUpload;

// será usada para desserializar os dados do XML recebidos na requisição.

[XmlRoot("DownloadRequest")]
public class DownloadRequest
{
    [XmlElement("FileName")] 
    public string FileName { get; set; }
}

[XmlRoot("DeleteRequest")]
public class DeleteRequest
{
    [XmlElement("FileName")] 
    public string FileName { get; set; }
}

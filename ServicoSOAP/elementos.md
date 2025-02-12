Identificar os elementos principais do WSDL

1️⃣ O endpoint (URL para a requisição)

```
<soap:address location="http://localhost:8000/UploadServico"/>
```

2️⃣ O método que precisamos chamar

```
<wsdl:operation name="UploadArquivo">
    <soap:operation soapAction="http://tempuri.org/IUploadServico/UploadArquivo" style="document"/>

```
✅ Isso significa que a operação/método é:
👉 "UploadArquivo"

✅ O SOAPAction que precisa ser enviado no cabeçalho da requisição:
👉 "http://tempuri.org/IUploadServico/UploadArquivo"


3️⃣ O formato da mensagem esperada

```
<wsdl:message name="IUploadServico_UploadArquivo_InputMessage">
    <wsdl:part name="parameters" element="tns:UploadArquivo"/>
</wsdl:message>
```

✅ Isso indica que a requisição precisa conter um nó chamado UploadArquivo no namespace http://tempuri.org/.

Exemplo de requisição SOAP (XML)

```
<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tem="http://tempuri.org/">
    
    <soapenv:Header/>
    
    <soapenv:Body>
        <tem:UploadArquivo>
            <tem:fileName>meuarquivo.txt</tem:fileName>
            <tem:fileContent>BASE64_DO_ARQUIVO</tem:fileContent>
        </tem:UploadArquivo>
    </soapenv:Body>
</soapenv:Envelope>
```





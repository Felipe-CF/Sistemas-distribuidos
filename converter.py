import base64

# Caminho do arquivo a ser convertido
arquivo_origem = "morango.jpeg"  # Substitua pelo nome do seu arquivo
arquivo_destino = "arquivo_base64.txt"

# Lendo o arquivo e convertendo para Base64
with open(arquivo_origem, "rb") as f:
    conteudo_base64 = base64.b64encode(f.read()).decode("utf-8")

# Salvando o resultado em um arquivo .txt
with open(arquivo_destino, "w") as f:
    f.write(conteudo_base64)

print(f"Arquivo convertido e salvo em {arquivo_destino}")

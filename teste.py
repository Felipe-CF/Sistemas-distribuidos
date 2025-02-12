import base64

with open("C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\morango.jpeg", "rb") as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

print(file_content)

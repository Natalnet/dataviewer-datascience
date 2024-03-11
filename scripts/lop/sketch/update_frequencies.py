"""
Este script realiza uma autênticação em um API através do metodo POST e recebe um token de autenticação. 

Os dados de fruência dos estudantes são obtidos através de uma rota da API que recebe o token de autenticação 
e o código da turma. Esta consulta é realizada através do método GET. 

Por fim, os dados são tratados e inseridos no banco de dados do sistema dataviewer. 
"""

import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

print( config['USER_EMAIL'] )


"""
Esta função realiza a autenticação na API e retorna um token de autenticação.

Returns:
  str: Token de autenticação
"""
def get_token():
    # URL da API
    url = "http://apibot.orivaldo.net:8000/api/v1/users/login"

    # Dados de autenticação
    auth_data = {
        "email": config['USER_EMAIL'],
        "password": config['USER_PASSWORD']
    }

    # Faz a solicitação POST
    response = requests.post(url, json=auth_data)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Converte a resposta para JSON
        data = response.json()
        
        print(data['message']) 
        # Retorna o token
        return data['token']['access_token'] 
    else:
        print(f"Erro ao obter o token: {response.status_code}")
        return None
    

"""
Esta função obtém os dados de frequência de uma turma.

Args:
  class_code (str): Código da turma
  token (str): Token de autenticação

Returns:  
  dict: Dados da turma
"""
def get_class_data(class_code, token):
    # URL da API
    url = f"http://apibot.orivaldo.net:8000/api/v1/presenca/pegar_frequencias/{class_code}"

    # Cabeçalho de autenticação
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Faz a solicitação GET
    response = requests.get(url, headers=headers)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Converte a resposta para JSON
        data = response.json()

        # Retorna os dados
        return data
    else:
        print(f"Erro ao obter os dados da turma: {response.status_code}")
        return None

api_token = get_token()

# Exemplo de uso
class_data = get_class_data("LOP-A",api_token)
 

# Percorre os dados de frequência da turma
# Os dados estão organizados em um dicionário 
# Este for percorre o dicionário e mostra a presença de cada estudante. 
# O estudante é identificado por seu número de matrícula e este código lista 
# as datas em que o estudante esteve presente.
for key, value in class_data.items():
  if isinstance(value, dict):  # Verifica se o valor é um dicionário
    for sub_key, sub_value in value.items():
      #print(f"Chave: {sub_key}, Valor: {sub_value}")
      print(sub_value['matricula']) 
      #print(sub_value['frequencia'])
      for sub_sub_key, freq in sub_value['frequencia'].items():
        if freq == 'P':
          print(f"Chave: {sub_sub_key}")

 
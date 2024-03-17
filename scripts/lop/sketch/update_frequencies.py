"""
Este script realiza uma autênticação em um API através do metodo POST e recebe um token de autenticação. 

Os dados de fruência dos estudantes são obtidos através de uma rota da API que recebe o token de autenticação 
e o código da turma. Esta consulta é realizada através do método GET. 

Por fim, os dados são tratados e inseridos no banco de dados do sistema dataviewer. 
"""

import requests
import json
from dotenv import dotenv_values
import pymongo
from pymongo.server_api import ServerApi

config = dotenv_values(".env")

print( config['USER_EMAIL'] )


"""
Esta função realiza a autenticação na API e retorna um token de autenticação.

Returns:
  str: Token de autenticação
"""
def get_token():
    # URL da API
    url = f"{config['API_BOT']}/api/v1/users/login"

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
    url = f"{config['API_BOT']}/api/v1/presenca/pegar_frequencias/{class_code}"

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


def replaceOneStudentFrequency(collection, studentDataFreq, classCode):
  """
  Esta função recebe um dicionário com os dados de frequência de um estudante e os insere no banco de dados.
  Caso já exista o estudante com a frequência cadastrada, esta será atualizada. Os campos mais importantes da 
  tabela resultante são o código da turma, o número de matrícula do estudante e a lista de frequências.

  Args:  
  data (dict): Dicionário com os dados da turma
  nameCollection (str): Nome da coleção onde os dados serão inseridos
  classCode (str): Código da turma

  Returns:
  None
  """
  studentDataFreq['classCode'] = classCode 
  try: 
    print('\nGravando os dados do estudante ', studentDataFreq['regNum']) 
    result = collection.replace_one( {'regNum': studentDataFreq['regNum'], 'classCode': classCode }, studentDataFreq, True)
    
    if result.modified_count == 0:
      print('Inserido!') 
    else: 
      print('Atualizado!') 
  except:
    print("Erro ao inserir no banco de dados!")

api_token = get_token()

# Exemplo de uso
class_data = get_class_data("LOP-D",api_token)

# Conecta ao banco de dados
client = pymongo.MongoClient(config['ATLAS_URI'], server_api=ServerApi('1'))
dbDataviewer = client['dataviewert1'] 
# Acessa a coleção de frequências de estudantes
collections = dbDataviewer['studentfrequencies']

# Percorre os dados de frequência da turma
# Os dados estão organizados em um dicionário 
# Este for percorre o dicionário e mostra a presença de cada estudante. 
# O estudante é identificado por seu número de matrícula e este código lista 
# as datas em que o estudante esteve presente.
# Formato do dicionário para cada estudante depois de tratado:
# {"regNum": "234243234", "classCode": "lop2024_1t02", "classFreqs": [ "2021-10-10", "2021-10-11", "2021-10-12" ] }
for key, value in class_data.items():
  if isinstance(value, dict):  # Verifica se o valor é um dicionário
    for sub_key, sub_value in value.items():
      tempStudent = {}
      freqs = []
      #print(f"Chave: {sub_key}, Valor: {sub_value}")
      #print(sub_value['matricula']) 
      tempStudent['regNum'] =  str( int( sub_value['matricula'] ))
      #print(sub_value['frequencia'])
      for sub_sub_key, freq in sub_value['frequencia'].items():
        if freq == 'P':
          #print(f"Dia: {sub_sub_key}")
          freqs.append(sub_sub_key) 
      tempStudent['classFreqs'] = freqs
      print(tempStudent)
      #replaceOneStudentFrequency(collections, tempStudent, "lop2024_1t02")
 
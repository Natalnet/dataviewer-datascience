
"""
Classe para extrair dados da API do Bot e inserir no banco de dados do sistema dataviewer.

"""

import pandas as pd 
import requests
import json
from dotenv import dotenv_values
import pymongo
from pymongo.server_api import ServerApi

config = dotenv_values(".env")

print( config['USER_EMAIL'] )

def convertToUTCDate(date):
  s = date.split('/')
  return '{}-{}-{}'.format(s[2],s[1],s[0]) 

class BotDataManipulation:
  def __init__(self):
    self.token = self.get_token()
    #self.client = pymongo.MongoClient(config['MONGO_URL'], server_api=ServerApi('1'))
    #self.db = self.client[config['MONGO_DB']]
 
  """
  Este método realiza a autenticação na API e retorna um token de autenticação.

  Returns:
    str: Token de autenticação
  """
  def get_token(self):
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
  Este método obtém os dados de frequência de uma turma.

  Args:
    class_code (str): Código da turma
    token (str): Token de autenticação

  Returns:  
    dict: Dados da turma
  """
  def get_class_data(self, class_code, token):
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

  """
  Este método obtém os dados das atividades de participação de uma turma.

  Args:
    class_code (str): Código da turma
  """
  def get_participation_data(self, class_code):
      # URL da API
      url = f"{config['API_BOT']}/api/v1/miniteste/alunos/{class_code}"

      # Cabeçalho de autenticação
      headers = {
          "Authorization": f"Bearer {self.token}"
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
          print(f"Erro ao obter os dados de participação: {response.status_code}")
          return None
      

# Instancia a classe
bot = BotDataManipulation()

# Executa o método
data = bot.get_participation_data('LOP-A')
print(data) 
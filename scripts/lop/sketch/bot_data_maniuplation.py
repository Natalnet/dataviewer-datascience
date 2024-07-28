
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
    self.client = pymongo.MongoClient(config['ATLAS_URI'], server_api=ServerApi('1'))
    self.db = self.client['dataviewert1']
 
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
  def getParticipationData(self, classCode):
      # URL da API
      url = f"{config['API_BOT']}/api/v1/miniteste/alunos/{classCode}"

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
  """
  Este método insere os dados de participação de uma turma no banco de dados.    

  Args:
    class_code (str): Código da turma
  """
  def insertParticipationDataBot1(self, classCode, collectionName):
    collections = self.db[collectionName] 
    subClasses = ['LOP-A','LOP-B','LOP-C','LOP-D']
    # preenche a participação de cada sub-turma 
    for subClass in subClasses:
      participationMiniTests = self.getParticipationData(subClass)

      miniTestsForUnitOne = ['T1','T2','T3','T4','T5','T6']
      miniTestsForUnitTwo = ['T7','T8','T9','T10','T11','T12']
      miniTestsForUnitThree = ['T13','T14','T15','T16','T17']
      for participationCod in participationMiniTests:
        #print('---\n',participationMiniTests[participationCod]) 
        doc = {} 
        doc['matricula'] = str(participationMiniTests[participationCod]['matricula'])
        # Calcula a nota dos mini-testes da unidade 1. Soma 1 para cada mini teste realizado. 
        # Se o estudante não realizou o mini teste, o respectivo mini teste não está presente em participationMiniTests
        miniTestCount = 0 
        for miniTest in miniTestsForUnitOne:
          if miniTest in participationMiniTests[participationCod]['respostas']:
            miniTestCount += 1
        miniValue = str(miniTestCount/len(miniTestsForUnitOne))
        doc['pres1'] = miniValue
        # Temporariamente as notas da atividade 1 e da presença 1 são iguais e calculadas com os mini-testes 
        doc['ativs1'] = miniValue
        miniTestCount = 0 
        for miniTest in miniTestsForUnitTwo:
          if miniTest in participationMiniTests[participationCod]['respostas']:
            miniTestCount += 1
        if len(miniTestsForUnitTwo) == 0:
          miniValue = '0'
        else:
          miniValue = str(miniTestCount/len(miniTestsForUnitTwo))
        doc['pres2'] = miniValue
        doc['ativs2'] = miniValue
        miniTestCount = 0
        for miniTest in miniTestsForUnitThree:
          if miniTest in participationMiniTests[participationCod]['respostas']:
            miniTestCount += 1
        if len(miniTestsForUnitThree) == 0:
          miniValue = '0'
        else:
          miniValue = str(miniTestCount/len(miniTestsForUnitThree))
        doc['pres3'] = miniValue
        doc['ativs3'] =  miniValue 
        doc["codigoTurma"] = classCode 
        print('---\n',doc) 
        try: 
          collections.replace_one( {'matricula': doc['matricula'] }, doc, True)  
        except:
          print("Erro ao inserir no banco de dados!")   

# Instancia a classe
bot = BotDataManipulation()

# Obtendo participação da turma LOP-A
#data = bot.get_participation_data('LOP-A')
#print(data) 

# Inserindo dados de participação da turma lop2024_1t02 no banco de dados
bot.insertParticipationDataBot1('lop2024_1t02', 'studentparticipations')


from dotenv import dotenv_values
import pymongo
from pymongo.server_api import ServerApi

import argparse

# Recebe como parâmentro uma string durante a execução do código via linha de comando 
# Cria o parser
parser = argparse.ArgumentParser(description='Processa uma string.')
# Adiciona o argumento
parser.add_argument('input_string', type=str, help='A string a ser processada')
# Analisa os argumentos
args = parser.parse_args()
# Imprime a string recebida
print(f'String recebida: {args.input_string}')

classCode = args.input_string

config = dotenv_values(".env")

print(config['ATLAS_URI']) 

client = pymongo.MongoClient(config['ATLAS_URI'], server_api=ServerApi('1'))
db = client['dataviewert1'] 
#classesCollections = db['tclasses']

def replaceClassData(db, data, nameCollection,classCode):
  """
  Esta função recebe um dicionário com os dados de uma turma e os insere no banco de dados.
  Caso já exista uma turma cadastrada, esta será atualizada. Os campos mais importantes da 
  tabela resultante são o código da turma, nome, descriçao, ano e semestre. 

  Args:
  db (pymongo.database.Database): Banco de dados
  data (dict): Dicionário com os dados da turma
  nameCollection (str): Nome da coleção onde os dados serão inseridos
  classCode (str): Código da turma

  Returns:
  None
  """
  collections = db[nameCollection]
  #collections.update_one({"classCode": classCode}, {"$set": data}, upsert=True)
  try: 
    print('\nGravando os dados de ', classCode) 
    result = collections.replace_one( {'class_code': classCode }, data, True)   
    
    if result.modified_count == 0:
      print('Inserido!') 
    else: 
      print('Atualizado!') 
  except:
    print("Erro ao inserir no banco de dados!") 
  


import json 

with open('./dados/{}/turma.json'.format(classCode), mode='r',  encoding=" UTF-8") as classes_file:
  classesData = json.load(classes_file) 
  print(classesData)
  replaceClassData(db, classesData, 'tclasses', classCode)
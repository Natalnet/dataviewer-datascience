
import argparse

from dotenv import dotenv_values
import pymongo
from pymongo.server_api import ServerApi
import pandas as pd 
import numpy as np 

config = dotenv_values(".env")
client = pymongo.MongoClient(config['ATLAS_URI'], server_api=ServerApi('1'))
db = client['dataviewert1'] 


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

def replaceStudentsOfClass(db, data, nameCollection,classCode):
  """
  Esta função recebe um dataframe com os dados dos estudantes de uma turma e os insere no banco de dados.
  Caso já exista estudantes da turma cadastrados, estes serão atualizadas. Os campos mais importantes da 
  tabela resultante são o código da turma e a lista de estudantes (reg_num, name, sub_class)

  Args:
  db (pymongo.database.Database): Banco de dados
  data (pandas.core.frame.DataFrame): Dataframe com os dados dos estudantes
  nameCollection (str): Nome da coleção onde os dados serão inseridos
  classCode (str): Código da turma

  Returns:
  None
  """
  #linha = {"reg":0, "name":"xxxx", "sub_class":"ax"} 
  collections = db[nameCollection]

  l, c =  data.shape
  studentArray = np.array([]) 
  regArray = np.array([])
  tempLinha = {}
  for i in range(l): 
    tempStudent = {}  
    for campo in data.columns:
      if campo == 'Nome':
        tempStudent['name'] = str( data.iloc[i][campo] )  
      if campo == 'Matrícula':
        tempStudent['reg_num'] = str( int(data.iloc[i][campo]) ) 
        regArray = np.append(regArray, str( int(data.iloc[i][campo]) ) )
      if campo == 'sub_turma':
        tempStudent['sub_class'] = str( data.iloc[i][campo] ) 
    studentArray = np.append(studentArray, tempStudent)   
  #print(studentArray)  
  #print(regArray) 
  tempLinha['reg_students'] = list( regArray )
  tempLinha['students'] = list( studentArray )
  tempLinha['class_code'] = classCode
  print(tempLinha)
  try: 
    print('\nGravando os dados de ', classCode) 
    result = collections.replace_one( {'class_code': classCode }, tempLinha, True)   
    
    if result.modified_count == 0:
      print('Inserido!') 
    else: 
      print('Atualizado!') 
  except:
    print("Erro ao inserir no banco de dados!") 
   


#classCode = "lop2023_2t01" 



dataStudents =  pd.read_csv("./dados/{}/alunos.csv".format(classCode)) 

print( dataStudents.head() )
 
replaceStudentsOfClass(db,dataStudents, 'classstudents', classCode) 
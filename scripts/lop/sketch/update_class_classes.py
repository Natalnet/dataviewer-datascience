from dotenv import dotenv_values
import pymongo
from pymongo.server_api import ServerApi
import pandas as pd 


config = dotenv_values(".env")

client = pymongo.MongoClient(config['ATLAS_URI'], server_api=ServerApi('1'))
db = client['dataviewert1'] 


def convertToUTCDate(date):
  s = date.split('/')
  return '{}-{}-{}'.format(s[2],s[1],s[0]) 

# Insere as datas e assuntos das aulas no banco de dados 
# Formato inserido no banco de dados
# { "classCode": "lop2023_2t01", "classTitles": [ {"date": "2021-10-10", "classTitle": "Aula 1" }, {"date": "2021-10-11", "classTitle": "Aula 2" } ] } 
def replaceOneDateClassClasses(db, data, nameCollection,classCode):  
  collections = db[nameCollection]

  tempLine = {}
  tempLine['classCode'] = classCode

  l, c =  data.shape
  classes = []
  print(classCode)
  for i in range(l):   
    tempClass = {}         
    #print(campo, ": ",dados.iloc[i][campo]) 
    tempClass['date'] = str( convertToUTCDate( data.iloc[i]['date'] ) )
    tempClass['classTitle'] = str( data.iloc[i]['classTitle'] )
    classes.append(tempClass)       
    print(tempClass)
  print(classCode)
  tempLine['classTitles'] = classes

  
  try: 
    #collections.insert_one(tempLinha)  
    collections.replace_one( {'classCode':  classCode }, tempLine, True)  
  except:
    print("Erro ao inserir no banco de dados!") 
  
# Será necessário melhorar a forma de receber o código da turma 
classCode = "lop2024_1t02" 

dataClassDate =  pd.read_csv("./dados/{}/datas_aulas.csv".format(classCode)) 
print( dataClassDate.head() ) 
replaceOneDateClassClasses(db,dataClassDate,'classclasses', classCode) 

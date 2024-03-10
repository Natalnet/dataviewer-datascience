# Recebe como parâmentro uma string durante a execução do código via linha de comando 
import argparse

# Cria o parser
parser = argparse.ArgumentParser(description='Processa uma string.')

# Adiciona o argumento
parser.add_argument('input_string', type=str, help='A string a ser processada')

# Analisa os argumentos
args = parser.parse_args()

# Imprime a string recebida
print(f'String recebida: {args.input_string}')
import argparse
import json

from jinja2 import Template

classes = {}

def le_arquivo(nome_arquivo):
    
    arquivo = open(nome_arquivo, "r")

    if not arquivo:
        print('file not found')
        exit()
    arquivo_json = json.load(arquivo)

    return arquivo_json

def existe_na_lista(classe, chave):
    global classes

    for lista in classes[classe]['list']:
        if (lista['valor'] == chave):
            return True

    return False

def monta_string(nome_classe, chave):
    if chave not in classes[nome_classe]['str']:
        classes[nome_classe]['str'].append(chave)

def monta_lista (nome_classe, chave, valor):
    if (len(valor) == 0):
        if not existe_na_lista(nome_classe, chave):
            classes[nome_classe]['list'].append({
                'tipo': chave,
                'variavel': chave.lower() + 's',
                'valor': chave
            })
        monta_classes(chave, valor)

    else:
        valor_copia = valor.copy().pop()
        if (isinstance(valor_copia, dict)):
            if not existe_na_lista(nome_classe, chave):
                classes[nome_classe]['list'].append({
                    'tipo': chave,
                    'variavel': chave.lower() + 's',
                    'valor': chave
                })
            monta_classes(chave, valor)
        else:
            if not existe_na_lista(nome_classe, chave):
                classes[nome_classe]['list'].append({
                    'tipo': 'String',
                    'variavel': chave.lower() + 's',
                    'valor': chave
            })

def monta_dicionario(nome_classe, chave, valor):
    if chave not in classes[nome_classe]['dict']:
        classes[nome_classe]['dict'].append(chave)
    monta_classes(chave, valor)

def monta_classes(nome_classe, instancias):
    if nome_classe not in classes:
        classes[nome_classe] = {
            'str': [],
            'list': [],
            'dict': []
        }

    if isinstance(instancias, dict):
        for chave, valor in instancias.items():
            if (isinstance(valor, str)):
                monta_string(nome_classe, chave)
                
            if (isinstance(valor, list)):
                monta_lista(nome_classe, chave, valor)
                
            if isinstance(valor, dict):
                monta_dicionario(nome_classe, chave, valor)
    elif isinstance(instancias, list):
        for instancia in instancias:
            for chave, valor in instancia.items():
                if (isinstance(valor, str)):
                    monta_string(nome_classe, chave)
                    
                if (isinstance(valor, list)):
                    monta_lista(nome_classe, chave, valor)
                    
                if isinstance(valor, dict):
                    monta_dicionario(nome_classe, chave, valor)

def generate_java_code(dict: classes):
    print(classes)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', action='store', type=str, help='Caminho para o arquivo', required=True)
    args = parser.parse_args()

    arquivo = le_arquivo(args.path)

    for chave, valor in arquivo.items():
        monta_classes(chave, valor)

    generate_java_code(classes)
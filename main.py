#!/bin/python3

import argparse
import json

from jinja2 import Environment, FileSystemLoader

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
        dicionario = {}
        dicionario["tipo"] = chave
        dicionario["variavel"] = chave.lower()
        classes[nome_classe]['dict'].append(dicionario)
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
    
    file_java = open("programa.java", "w+")
    
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    classe_template = env.get_template('classe.template')

    file_java.write("import java.util.ArrayList;\n\n")
    for classe in classes:
        atributos = classes.get(classe)
        output = classe_template.render(
            nome_classe=classe, 
            atributos_strings=atributos.get("str"), 
            atributos_objetos=atributos.get("dict"), 
            atributos_arrays=atributos.get("list")
        )
        file_java.write(output)
    main_template = env.get_template("main.template")
    output = main_template.render()

    file_java.write(output)
    file_java.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', action='store', type=str, help='Caminho para o arquivo', required=True)
    args = parser.parse_args()

    arquivo = le_arquivo(args.path)

    for chave, valor in arquivo.items():
        monta_classes(chave, valor)

    generate_java_code(classes)
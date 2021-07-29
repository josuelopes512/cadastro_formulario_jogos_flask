import os
import sqlite3
from app import app
from dao import UsuarioDao


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_padrao' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


def consulta_usuario(id):
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    user = usuario_dao.buscar_por_id(id)
    if user:
        return user.nome
    else:
        return ''

from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
import sqlite3, os, time

from helpers import deleta_arquivo, recupera_imagem

from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    session, 
    flash, 
    url_for, 
    send_from_directory
)

app = Flask(__name__)
app.config.from_pyfile('config.py')


# session['usuario_logado']
def consulta(id):
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    user = usuario_dao.buscar_por_id(id)
    if user:   
        return user.nome
    else:
        return ''



@app.route('/')
def index():
    jogo_dao = JogoDao(sqlite3.connect('bd.sqlite3'))
    lista = jogo_dao.listar()
    nome = consulta(session['usuario_logado'])
    # usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    # user = usuario_dao.buscar_por_id(session['usuario_logado'])
    # if user:   
    #     nome = user.nome
    # else:
    #     nome = ''
    
    return render_template('lista.html', titulo='Jogos', jogos=lista, usuario=nome )



@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    nome = consulta(session['usuario_logado'])
    
    return render_template('novo.html', titulo='Novo Jogo', usuario=nome)

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao = JogoDao(sqlite3.connect('bd.sqlite3'))
    jogo_dao.salvar(jogo)
    upload_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo_dao = JogoDao(sqlite3.connect('bd.sqlite3'))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem =  recupera_imagem(id)
    capa_jogo = f'capa{id}.jpg'
    nome = consulta(session['usuario_logado'])
    return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo=nome_imagem, usuario=nome)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao = JogoDao(sqlite3.connect('bd.sqlite3'))
    jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao = JogoDao(sqlite3.connect('bd.sqlite3'))
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    usuario = usuario_dao.buscar_por_nome(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario ou Senha Incorreta - Tente de Novo !!!!')
            return redirect(url_for('login'))
    else:
        flash('Usuario ou Senha Incorreta - Tente de Novo !!!!')
        return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo='Cadastrar Login') 


@app.route('/cadastrar', methods=['POST',])
def cadastrar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    user = Usuario(usuario, senha)
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    usuario_dao.salvar(user)
    return redirect(url_for('login'))
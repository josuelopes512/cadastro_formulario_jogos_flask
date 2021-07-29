from models import Jogo, Usuario

SQL_DELETA_USUARIO = 'DELETE FROM usuario WHERE id = ?'
SQL_USUARIO_POR_NOME = 'SELECT id, nome, senha from usuario where nome = ?'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = ?'

# SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET nome= ?, senha= ? where id = ?'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET senha= ? where id = ?'
SQL_CRIA_USUARIO = 'INSERT INTO usuario(nome, senha) VALUES (?,?)'
SQL_BUSCA_USUARIO = 'SELECT id, nome, senha from usuario'
SQL_CRIA_TABELA_USUARIO = """
        create table if not exists usuario(
        id integer primary key autoincrement,
        nome text UNIQUE not null,
        senha text not null
    )"""

SQL_DELETA_JOGO = 'delete from jogo where id = ?'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = ?'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome= ?, categoria= ?, console= ? where id = ?'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_CRIA_JOGO = 'INSERT INTO jogo(nome, categoria, console) VALUES (?,?,?)'
SQL_CRIA_TABELA_JOGO = """
    create table if not exists jogo(
    id integer primary key autoincrement,
    nome text not null,
    categoria text not null,
    console text not null
    )"""


class JogoDao:
    def __init__(self, db):
        self.__db = db
        cursor = self.__db.cursor()
        cursor.execute(SQL_CRIA_TABELA_JOGO)

    def salvar(self, jogo):
        cursor = self.__db.cursor()
        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome,
                           jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome,
                           jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__db.commit()
        return jogo

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETA_JOGO, (id, ))
        self.__db.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db
        cursor = self.__db.cursor()
        cursor.execute(SQL_CRIA_TABELA_USUARIO)

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_USUARIO)
        jogos = traduz_user(cursor.fetchall())
        return jogos

    def buscar_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id, ))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def buscar_por_nome(self, nome):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_NOME, (nome, ))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def salvar(self, user):
        cursor = self.__db.cursor()
        user_exist = self.buscar_por_nome(user.nome)
        if user_exist:
            cursor.execute(SQL_ATUALIZA_USUARIO,
                           (user_exist.senha, user_exist.id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (user.nome, user.senha))
            user.id = cursor.lastrowid
        self.__db.commit()
        return user

    def deletar(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETA_USUARIO, (id, ))
        self.__db.commit()


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_user(user):
    def cria_user_com_tupla(tupla):
        return Usuario(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_user_com_tupla, user))


def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[0])


from sqlalchemy import Connection, Engine, create_engine, TextClause, text
from sqlalchemy.exc import DisconnectionError, StatementError, OperationalError
from urllib.parse import quote_plus

USER = 'pedreiraumvx'
SENHA = 'Admin@#2022!@#'
SENHA = quote_plus(SENHA)
SERVIDOR = '192.168.12.6'
PORTA = '3306'

# string_conexao = f"mariadb+mariadbconnector://pedreiraumvx:{senha}@192.168.12.6:3306/glpi"
string_conexao = f"mariadb+mariadbconnector://{USER}:{SENHA}@{SERVIDOR}:{PORTA}/glpi"

engine: Engine = create_engine(
    string_conexao, 
    echo=False, 
    future=True,
    pool_size=5,  # Number of connections to maintain in the pool
    max_overflow=10,  # Additional connections beyond pool_size
    pool_timeout=30,  # Timeout for getting connection from pool
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Validate connections before use
    connect_args={
        "connect_timeout": 10,  # Connection timeout
        "read_timeout": 30,     # Read timeout
        "write_timeout": 30     # Write timeout
    }
)


conn = engine.connect()
if not conn:
    raise ConnectionError("Failed to establish a connection to the MariaDB database.")




















import pandas
import time
from urllib.parse import quote_plus # para o @ da senha
import sqlalchemy
from sqlalchemy import create_engine, text # para criar a conexão
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert, update # para insert e update
from sqlalchemy.exc import SQLAlchemyError # para pegar o erro no try

from sqlalchemy.orm import Session # para update
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import update


class ConectarBd():
    def __init__(self, database = ''):
        # self.BotVar=BotVar
        # self.BotLog=BotLog
        
        self.cont_recursão = 0
        self.max_recursão = 10
        self.tempo_espera = 60
        self.erro = False # para controlar se deu erro na conexão ou consultas e para controlar os avisos, avisar somente uma vez
        if database:
            self.database = database
        else:
            self.database = 'rpa'

        self.engine = self.createEngine()

    def createEngine(self):
        # print('Iniciando createEngine')
        user = USER
        password = SENHA
        password = quote_plus(password)
        host = SERVIDOR
        port = 3306
        database = self.database

        while True:
            try:
                engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
                # print('Conexão estabelecida com sucesso!')
                if self.erro:
                    msg_erro = 'Resolvido:' + 'CELIM' + " ConectarBd.createEngine."
                    print(msg_erro)
                    # self.BotLog.telegram_send_message(self.BotVar.dfparametros.query('NOME=="id_telegram_alertas"')['VALOR'].iloc[0], '✅ ' + msg_erro)
                    self.erro = False
                return engine
            except Exception as e:
                msg_erro = 'CELIM' + " ConectarBd.createEngine, erro ao criar a conexão: " + str(e)
                print(msg_erro)

                if not self.erro:
                    # self.BotLog.telegram_send_message(self.BotVar.dfparametros.query('NOME=="id_telegram_alertas"')['VALOR'].iloc[0], '❌' +  msg_erro)
                    self.erro = True
                print('Aguardando para tentar conectar de novo no banco')
                time.sleep(120)


    def getSql(self,sql):
        # print('Iniciando getSql')
        while True:
            try:
                df = pandas.read_sql(sql, con=self.engine)
                # df = pandas.read_sql(sql, con=self.createEngine())
                if self.erro:
                    msg_erro = 'Resolvido:' + 'CELIM' + " ConectarBd.getSql."
                    print(msg_erro)
                    # self.BotLog.telegram_send_message(self.BotVar.dfparametros.query('NOME=="id_telegram_alertas"')['VALOR'].iloc[0], '✅ ' +  msg_erro)
                    self.erro = False
                return df
            except Exception as e:
                msg_erro = 'CELIM' + " ConectarBd.getSql, erro ao criar o df: "+str(e)
                print(msg_erro)
                if not self.erro: 
                    # self.BotLog.telegram_send_message(self.BotVar.dfparametros.query('NOME=="id_telegram_alertas"')['VALOR'].iloc[0],'❌' + msg_erro)
                    self.erro = True
                print('Aguardando para tentar gerar o df de novo')
                time.sleep(self.tempo_espera)

        # print('Finalizando getSql')


BotConectarBd_glpi = ConectarBd('glpi')


df2 = BotConectarBd_glpi.getSql('select * from glpi_tickets')
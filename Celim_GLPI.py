import datetime
import cryptocode # para criptografia
import MySQLdb
import pandas as pd
import time
import telebot
import sys # para importação relativa
import pyautogui


with open("Config\Diretorios\RaizProjeto.txt", "r",) as arquivo:
    RaizProjeto=arquivo.read()
RaizProjeto=str(RaizProjeto)
with open("Config\Diretorios\CaminhoProjeto.txt", "r",) as arquivo:
    CaminhoProjeto=arquivo.read()
CaminhoProjeto=str(CaminhoProjeto)
CaminhoLib = RaizProjeto+"\\01_lib"
CaminhoProjeto = RaizProjeto+CaminhoProjeto
with open(CaminhoProjeto+"\\Config\\Senhas\\Chave.txt", "r",) as arquivo:
    chave=arquivo.read()
chave=str(chave)

sys.path.insert(1, CaminhoLib)
# sys.path.append('...lib')
from GerarChave import GerarChave
from GerarVar import GerarVar
from GerarLog import Gerarlog
# from GerenciadorTarefas import GerenciadorTarefas
# from FinalizarExecucao import FinalizarExecucao


BotChave = GerarChave()
BotVar = GerarVar(BotChave) 
BotVar.chaveBD = BotChave.gerarChave(chave)
BotVar.getParametros(15)# 1 para falar o id do rpa para pegar os parametros
# BotAreaTransferencia = AreaTransferencia()
BotLog = Gerarlog(BotVar)
# BotTarefas = GerenciadorTarefas(BotVar,BotLog)
# BotFinalizar = FinalizarExecucao(BotVar,BotLog,BotTarefas)



class GLPI:
    def __init__(self):
        if BotVar.dfparametros.query('NOME=="ativar_contatos_producao_glpi"')['VALOR'].iloc[0] == '0': ## verifica se esta no modo produção ou teste para não mandar mensagem de teste para os contatos
            BotVar.dfpessoas['CONTATO']=BotVar.dfpessoas.query('NOME=="Contato Teste"')['CONTATO'].iloc[0]
            BotVar.dfpessoas['EMAIL']=BotVar.dfpessoas.query('NOME=="Contato Teste"')['EMAIL'].iloc[0]

            BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_iniciofim","VALOR"] = '452405307'
            BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_logs","VALOR"] = '452405307'
            BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"] = '452405307'
            BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_glpi","VALOR"] = '452405307'
            self.co = 'raisson.charles@pedreiraumvalemix.com.br'
        
        # BotVar.BotTelegram.send_message(BotVar.dfparametros.query('NOME=="id_telegram_iniciofim"')['VALOR'].iloc[0], "Celin "+str(BotVar.dfparametros.query('NOME=="nome_rpa"')['VALOR'].iloc[0])+" Iniciado")

        self.id_telegram = BotVar.dfparametros.query('NOME=="id_telegram_glpi"')['VALOR'].iloc[0]
        # self.id_telegram = '-940535548'

        with open("Config\horatermino.txt", "r",) as arquivo:
            self.horariotermino=arquivo.read()
        self.horariotermino=str(self.horariotermino)
        self.horariotermino = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y'+"-"+'%m'+'-'+'%d'+" "+self.horariotermino), "%Y-%m-%d %H:%M")
    def relogio_timer(self,tempo):
        for i in range(tempo, 0, -1):
            # if i < cont_ver_prioridade:
            #     cont_ver_prioridade = cont_ver_prioridade - 60
            #     bot.log("Verificando prioridade")
            #     bot.VerificaPrioridade()
            time.sleep(1)
            if i > 3599:
                hora = i / 3600
                if hora < 10:
                    hora = "0"+str(hora)
                    hora = hora[0:2]
                else:
                    hora = str(hora)
                    hora = hora[0:2]
                minutoint = i % 3600
                segundoint = minutoint % 60
                minutoint = minutoint / 60
                if minutoint < 10:
                    minuto = "0"+str(minutoint)
                    minuto = minuto[0:2]
                else:
                    minuto = str(minutoint)
                    minuto = minuto[0:2]
                if segundoint < 10:
                    segundo = "0"+str(segundoint)
                else:
                    segundo = str(segundoint)
            else:
                hora = "00"
            if i > 60 and i < 3600 :
                minutoint = i / 60
                segundoint = i % 60
                if minutoint < 10:
                    minuto = "0"+str(minutoint)
                    minuto = minuto[0:2]
                else:
                    minuto = str(minutoint)
                    minuto = minuto[0:2]
                if segundoint < 10:
                    segundo = "0"+str(segundoint)
                else:
                    segundo = str(segundoint)
            if i < 60 and i > 9:
                segundo = i
                segundo = str(segundo)
                minuto = "00"
            if i == 60:
                minuto = "01"
                segundo = "00"
            if i < 10:
                segundo = i
                segundo = "0"+str(i)
                minuto = "00"
            # print("\n" * os.get_terminal_size().lines) # para limpar a tela e deixar o retorno na ultima linha
            # print("\x1b[2J\x1b[1;1H")  # para limpar a tela e deixar o retorno na primeira linha
            BotLog.imprimirLog(hora+":"+minuto+":"+segundo)
    def limparDescricao(self,descricao):
        x = descricao.find('&#60;')
        if x == -1:
            return descricao
        parte1 = descricao[:x]
        parte2 = descricao[x:]
        descricao = parte1+' '+parte2
        x+=1
        if x > 0:
            y = descricao.find('&#62;')+5
            parte1 = descricao[:y]
            parte2 = descricao[y:]
            descricao = parte1+' '+parte2
            y+=1
            if y>x:
                descricao_limpa = descricao[:x]+descricao[y:]
                descricao_limpa = bot.limparDescricao(descricao_limpa)
                return descricao_limpa
    def novoChamado(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO NOVO CHAMADO ###########################################################")
        
        sql_ultimo = 'SELECT max(id_chamado) ULTIMO_CHAMADO FROM tb015_glpi'
        conMySQLRPA = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db=BotVar.bancomysql) #Criando a conexão
        dfultimochamado= pd.read_sql_query(sql_ultimo,conMySQLRPA)
        id = dfultimochamado['ULTIMO_CHAMADO'].iloc[0]
        
        BotLog.gerarExcel(dfultimochamado,'dfultimochamado'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S"))
        
        sql_glpi = f"""
                SELECT t.id Numero, u.name Solicitante, e.name Entidade, c.name Categoria, t.name Titulo, SUBSTRING(t.content,12,LOCATE('&#60;/p&#62;',SUBSTRING(t.content,12,1000))-1) Descricao
                ,t.date_creation Data_Abertura,sa.name TA, t.time_to_own Data_TA , ss.name TS, t.time_to_resolve Data_TS
                ,t.status
                -- , t.users_id_recipient id_solicitante,t.slas_id_tto,t.slas_id_ttr, t.date,t.itilcategories_id id_categoria,t.*
                FROM glpi_tickets t
                INNER JOIN glpi_entities e ON e.id = t.entities_id
                INNER JOIN glpi_users u ON u.id = t.users_id_recipient
                INNER JOIN glpi_itilcategories c ON c.id = t.itilcategories_id
                INNER JOIN glpi_slas sa ON sa.id = t.slas_id_tto
                INNER JOIN glpi_slas ss ON ss.id = t.slas_id_ttr
                WHERE t.status = 1 and t.id > {id} ORDER BY t.id"""
        sql_glpi = ''
        sql_glpi = f"""
                SELECT t.id Numero, u1.name Solicitante, e.name Entidade, c.name Categoria, t.name Titulo, t.content Descricao
                ,t.date_creation Data_Abertura,sa.name TA, t.time_to_own Data_TA , ss.name TS, t.time_to_resolve Data_TS
                ,t.status
                FROM glpi_tickets t
                LEFT JOIN glpi_entities e ON e.id = t.entities_id
                left JOIN glpi_tickets_users tu1 ON tu1.tickets_id=t.id AND tu1.type = 1 -- para usuário atribuido
                left JOIN glpi_users u1 ON u1.id=tu1.users_id                            -- para usuário atribuido
                LEFT JOIN glpi_itilcategories c ON c.id = t.itilcategories_id
                LEFT JOIN glpi_slas sa ON sa.id = t.slas_id_tto
                LEFT JOIN glpi_slas ss ON ss.id = t.slas_id_ttr
                WHERE t.status = 1 and t.id > {id} ORDER BY t.id
                    """
        # self.id_telegram = '452405307'
                
        conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamados= pd.read_sql_query(sql_glpi,conMySQLGLPI)
        BotLog.gerarExcel(dfchamados,'dfchamados'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S"))

        for x in range(len(dfchamados.index)):
            numero = dfchamados['Numero'].iloc[x]
            solicitante = dfchamados['Solicitante'].iloc[x]
            entidade = dfchamados['Entidade'].iloc[x]
            categoria = dfchamados['Categoria'].iloc[x]
            categoria = categoria.replace('&#62;','>')
            titulo = dfchamados['Titulo'].iloc[x]
            descricao = dfchamados['Descricao'].iloc[x]
            descricao_limpa = bot.limparDescricao(descricao)
            descricao_limpa = descricao_limpa.replace('&#60;/p&#62;',' ')
            descricao_limpa = descricao_limpa.replace('&#60;p&#62;',' ')
            descricao_limpa = descricao_limpa.replace('&#60;br&#62;',' ')
            data_abertura = dfchamados['Data_Abertura'].iloc[x].strftime('%d-%m-%Y %H:%M:%S')
            ta = dfchamados['TA'].iloc[x]
            ta = ta.replace("TA","Tempo para atendimento")
            data_ta = dfchamados['Data_TA'].iloc[x].strftime('%d-%m-%Y %H:%M:%S')
            ts = dfchamados['TS'].iloc[x]
            ts = ts.replace("TS","Tempo para solução")
            data_ts = dfchamados['Data_TS'].iloc[x].strftime('%d-%m-%Y %H:%M:%S')
            link = r'http://192.168.11.50:8080/glpi/front/ticket.form.php?id='
            mensagem = f""" ⚠️ Novo Chamado!⚠️
            🎟 {numero}
            👤 {solicitante}
            🏢 {entidade}
            🏷 {categoria}
            ✏️ {titulo}
            🗒 {descricao_limpa}
            📅 {data_abertura}
            ⏱ {ta}
            ⏱ {data_ta}
            ⏰ {ts}
            ⏰ {data_ts}
            🔗 {link}{numero}
            """.replace("    ","")
            try:
                BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
            except Exception as e:
                msg_erro = "Erro no envio da mensagem pelo telegram, mensagem de erro: "+str(e)
                BotLog.imprimirLog(msg_erro)

            cur = conMySQLRPA.cursor()
            # sql = "INSERT INTO tb015_glpi (ID_CHAMADO)VALUES (%s)"
            numero = str(numero)
            # val = (numero)
            sql = f"INSERT INTO tb015_glpi (ID_CHAMADO)VALUES ({numero})"
            try:
                # cur.execute(sql, val)
                cur.execute(sql)
            except Exception as e:
                msg_erro = "Erro no insert do servidor MySQL, mensagem de erro: "+str(e)
                BotLog.imprimirLog(msg_erro)
                BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
            try:
                conMySQLRPA.commit()
            except Exception as e:
                msg_erro = "Erro no commit ou close no servidor MySQL, mensagem de erro: "+str(e)
                BotLog.imprimirLog(msg_erro)
                BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
        try:
            conMySQLRPA.close()    
        except Exception as e:
            msg_erro = "Erro na hora de fechar a conexão do servidor MySQL, mensagem de erro: "+str(e)
            BotLog.imprimirLog(msg_erro)
            BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
            
        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO NOVO CHAMADO ###########################################################")
    def chamadosVencendo(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO CHAMADOS VENCENDO ###########################################################")
        sql_glpi = f"""
        SELECT t.id Numero, u.name Solicitante, e.name Entidade, c.name Categoria, t.name Titulo, SUBSTRING(t.content,12,LOCATE('&#60;/p&#62;',SUBSTRING(t.content,12,1000))-1) Descricao
        ,t.date_creation Data_Abertura,sa.name TA, t.time_to_own Data_TA , ss.name TS, t.time_to_resolve Data_TS
        ,t.status
        -- , t.users_id_recipient id_solicitante,t.slas_id_tto,t.slas_id_ttr, t.date,t.itilcategories_id id_categoria,t.*
        FROM glpi_tickets t
        INNER JOIN glpi_entities e ON e.id = t.entities_id
        INNER JOIN glpi_users u ON u.id = t.users_id_recipient
        INNER JOIN glpi_itilcategories c ON c.id = t.itilcategories_id
        INNER JOIN glpi_slas sa ON sa.id = t.slas_id_tto
        INNER JOIN glpi_slas ss ON ss.id = t.slas_id_ttr
        WHERE t.status = 1 ORDER BY t.id"""
        
        # conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamados= pd.read_sql_query(sql_glpi,self.conMySQLGLPI)
        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO CHAMADOS VENCENDO ###########################################################")

bot = GLPI()



while bot.horariotermino>=datetime.datetime.now():
    bot.novoChamado()
    # bot.relogio_timer(5)
    bot.relogio_timer(300)


# BotFinalizar.finalizarExecucao("Finalizando execução com sucesso na ultima linha")

















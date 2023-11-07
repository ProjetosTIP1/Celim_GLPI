import datetime
from datetime import timedelta
import cryptocode # para criptografia
import MySQLdb
import pandas as pd
import time
import telebot
import sys # para importação absoluta
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import subprocess # executar exe, abrir programas e finalizar tarefas com o call




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
from GerenciadorTarefas import GerenciadorTarefas
from FinalizarExecucao import FinalizarExecucao
from GerenciadorJanelas import GerenciadorJanelas


BotChave = GerarChave()
BotVar = GerarVar(BotChave) 
BotVar.chaveBD = BotChave.gerarChave(chave)
BotVar.getParametros(15)# 1 para falar o id do rpa para pegar os parametros
# BotAreaTransferencia = AreaTransferencia()
BotLog = Gerarlog(BotVar)

# BotVar.dfparametros.loc[BotVar.dfparametros['NOME'] == "id_telegram_iniciofim", 'VALOR'] = 452405307
# BotLog.InicioFim("InicioExecucao")

BotTarefas = GerenciadorTarefas(BotVar,BotLog)
BotFinalizar = FinalizarExecucao(BotVar,BotLog,BotTarefas)
BotGerenciadorJanelas = GerenciadorJanelas(BotVar=BotVar,BotLog=BotLog)



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


        with open("Config\caminho_excel.txt", "r",) as arquivo:
            self.caminho_excel=arquivo.read()
        self.caminho_excel=str(self.caminho_excel)

        with open("Config\sistema.txt", "r",) as arquivo:
            self.sistema=arquivo.read()
        self.sistema=str(self.sistema)

        self.chamadosvencendoavisado = [] # lista com chamados vencendo que ja foi avisado
        self.limiteaguardarelemento = 0 # contador limitar as tentativas de procurar um elemento html
        self.tempo = 300 # tempo em segundos entre cada verificação
        self.limiteaguardartitulo = 0
        self.limiteaguardartitulomaximo = 60
        self.conterro = 0 # contador para mandar mensagem somente se o erro acontecer mais de duas vezes seguida
        self.enviar_pendentes = True
    def relogio_timer(self,tempo):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO RELOGIO_TIMER ###########################################################")
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
        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO RELOGIO_TIMER ###########################################################")
    def esperarTitulo(self,titulo):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO ESPERAR TITULO ###########################################################")
        BotLog.imprimirLog("Esperando a janela com titulo: "+titulo)
        if titulo in pyautogui.getActiveWindow().title:
            BotLog.imprimirLog("Encontrou o titulo, titulo atual: "+str(pyautogui.getActiveWindow().title))
            self.limiteaguardartitulo=0
            BotLog.imprimirLog("########################################################### FINALIZANDO MODULO ESPERAR TITULO ###########################################################")
            return True
        if self.limiteaguardartitulo>self.limiteaguardartitulomaximo:
            raise Exception("Execeu o limite de tentativas de encontrar o titulo "+titulo)
        time.sleep(1)
        self.limiteaguardartitulo+=1
        if bot.esperarTitulo(titulo):
            return True
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
    def tempoComercial(self,data_inicio_str,data_fim_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
        # BotLog.imprimirLog("########################################################### INICIANDO MODULO TEMPO COMERCIAL ###########################################################")
        # Lendo a tabela de feriados
        sql_holidays = f"""
            SELECT id, name, begin_date, end_date, is_perpetual
            FROM glpi_holidays
            ORDER BY id
            """
        conMySQLholidays = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfholidays= pd.read_sql_query(sql_holidays,conMySQLholidays)
        BotLog.gerarExcel(dfholidays,'dfholidays'+datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S"))
        # Criando uma lista com os feriado
        self.feriados = []
        # self.chamadosvencendoavisado.append(str(numerodf))
        for x_holiday in range(len(dfholidays.index)):
            id = dfholidays['id'].iloc[x_holiday]
            name = dfholidays['name'].iloc[x_holiday]
            begin_data = dfholidays['begin_date'].iloc[x_holiday]
            end_date = dfholidays['end_date'].iloc[x_holiday]
            is_perpetual = dfholidays['is_perpetual'].iloc[x_holiday]
            if is_perpetual == 1: # condição para feriados perpetuos
                if begin_data.year != end_date.year:
                    msg = f"""Erro no Celim GLPI Chamados pendentes.
                      Intervalo de datas na tabela de feriado com anos diferentes, favor corrigir.
                      Data inicio: {begin_data.strftime("%d-%m-%Y")}
                      Data Fim: {end_date.strftime("%d-%m-%Y")}
                      Nome do feriado: {name}
                      """
                    msg = msg.replace("  ","")
                    print(msg)
                    BotVar.BotTelegram.send_message(int(self.id_telegram),msg)
                if begin_data.year != datetime.datetime.now().date().year:
                    # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                    begin_data = begin_data.replace(year=datetime.datetime.now().date().year)                        
                if end_date.year != datetime.datetime.now().date().year:
                    # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                    end_date = end_date.replace(year=datetime.datetime.now().date().year)
            if begin_data == end_date:
                # print("Datas de inicio e fim de feriado iguais")
                self.feriados.append(begin_data)
            elif begin_data > end_date: # Inicio do feriado não pode ser maior que o fim
                msg = "A data de id "+str(id)+' e nome '+str(name)+' na tabela de calendario esta com uma data de inicio maior que a data de fim.'
                print(msg)
                BotVar.BotTelegram.send_message(int(self.id_telegram),msg)
            elif begin_data < end_date: #Adiciona o intervalo de datas do feriado
                # print("Datas diferentes, percorrendo as datas")
                difer_dias = end_date - begin_data
                difer_dias = difer_dias.days
                while begin_data <= end_date:
                    self.feriados.append(begin_data)
                    begin_data = begin_data + datetime.timedelta(days=1)

    
        data_inicio_dt = datetime.datetime.strptime(data_inicio_str,"%d-%m-%Y %H:%M:%S")
        data_fim_dt = datetime.datetime.strptime(data_fim_str,"%d-%m-%Y %H:%M:%S")
        date = data_inicio_dt.date()
        hour = data_inicio_dt.time()
        tempo_segundos = 0

        # hoje = datetime.datetime.now()
        # dia_semana = hoje
        # for x in range(10):
        #     dia_semana = hoje.weekday()
        #     hoje = hoje + datetime.timedelta(days=1)
        horas = data_inicio_dt.hour


        hoje_data = datetime.datetime.now().date()
        while data_inicio_dt.date() <= data_fim_dt.date():
            dia_semana = data_inicio_dt.weekday() 
            if data_inicio_dt.weekday() == 5 or data_inicio_dt.weekday() == 6: # pular um dia se for final de semana
                # print("Final de semana")
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
                continue
            if data_inicio_dt.date() in self.feriados: # pular um dia se for feriado
                # print("E um feriado")
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
                continue
            if (data_inicio_dt.weekday() == 4 and data_inicio_dt.hour>16) or (data_inicio_dt.weekday() == 4 and data_inicio_dt.hour==17 and data_inicio_dt.minute>0): # ir para o proximo dia se for mais de 16 horas e sexta
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
                continue
            if (data_inicio_dt.weekday() in (0,1,2,3) and data_inicio_dt.hour>17) or (data_inicio_dt.weekday() in (0,1,2,3) and data_inicio_dt.hour==17 and data_inicio_dt.minute>0): # ir para o proximo dia se for mais de 17 horas
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
                continue
            if data_inicio_dt.hour<7: # se o chamado for aberto antes das 7
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
            if data_inicio_dt.day == data_fim_dt.day: # para quando a data de inicio e fim for no mesmo dia, caucula a diferença de horas so no dia
                diferenca = data_fim_dt - data_inicio_dt
                tempo_segundos+=diferenca.seconds
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                continue
            if (data_inicio_dt.hour != 7 or data_inicio_dt.minute != 0) and (data_inicio_dt.hour>=7) and (data_inicio_dt.hour<17): # caucula diferença para o primeiro dia
                fim_do_dia = data_inicio_dt
                fim_do_dia = fim_do_dia.replace(hour=17,minute=0,second=0)
                diferenca = fim_do_dia - data_inicio_dt
                # tempo_segundos+=(diferenca.hour * 3600)
                # tempo_segundos+=(diferenca.minute * 60)
                tempo_segundos+=diferenca.seconds
                if data_inicio_dt.weekday() == 4: # tirar uma hora se for a sexta
                    tempo_segundos-=3600
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0)
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                continue
            if data_inicio_dt.date() == data_fim_dt.date(): # diferença de hora do ultimo dia
                # hora_atual = datetime.datetime.now()
                if (data_fim_dt.weekday() == 4 and data_fim_dt.hour > 16) or (data_fim_dt.weekday() == 4 and data_fim_dt.hour == 16 and data_fim_dt.minute > 0):
                    data_fim_dt = data_fim_dt.replace(hour=16,minute=0)
                if (data_fim_dt.weekday() in (0,1,2,3) and data_fim_dt.hour > 17) or (data_fim_dt.weekday() in (0,1,2,3) and data_fim_dt.hour == 17 and data_fim_dt.hour > 0):
                    data_fim_dt = data_fim_dt.replace(hour=17,minute=0)
                diferenca = data_fim_dt - data_inicio_dt
                # tempo_segundos+=(diferenca.hour * 3600)
                # tempo_segundos+=(diferenca.minute * 60)
                tempo_segundos+=diferenca.seconds
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                continue
            if data_inicio_dt.weekday() == 4: # se for sexta soma 9 horas
                tempo_segundos+=32400
            else: # se não for sexta soma dez horas
                tempo_segundos+=36000
            data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)

        # BotLog.imprimirLog("########################################################### FINALIZANDO MODULO TEMPO COMERCIAL ###########################################################")
        return tempo_segundos
    def segundos_para_horas_minutos(self,segundos):
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos = segundos % 60
        if segundos < 9:
            segundos = "0"+str(segundos)
        if minutos < 9:
            minutos = "0"+str(minutos)
        if horas < 9:
            horas = "0"+str(horas)
        return str(horas)+":"+str(minutos)+":"+str(segundos)
    def novoChamado(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO NOVO CHAMADO ###########################################################")
        
        sql_ultimo = 'SELECT max(id_chamado) ULTIMO_CHAMADO FROM tb015_glpi WHERE TIPO_AVISO = "NOVO"'
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
        
                
        conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamados= pd.read_sql_query(sql_glpi,conMySQLGLPI)
        BotLog.gerarExcel(dfchamados,'dfchamadosnovos'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S"))

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
            # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
            link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
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
    def chamadosVencendoWeb(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO CHAMADOS VENCENDO ###########################################################")

        sql_glpi = f"""
            SELECT  t.id Numero, 
                    u1.name Solicitante, 
                    e.name Entidade, 
                    c.name Categoria, 
                    t.name Titulo, 
                    t.content Descricao,
                    t.date_creation Data_Abertura,
                    sa.name TA, 
                    t.time_to_own Data_TA , 
                    ss.name TS, 
                    t.time_to_resolve Data_TS
                    ,t.status
            FROM glpi_tickets t
            LEFT JOIN glpi_entities e ON e.id = t.entities_id
            left JOIN glpi_tickets_users tu1 ON tu1.tickets_id=t.id AND tu1.type = 1 -- para usuário atribuido
            left JOIN glpi_users u1 ON u1.id=tu1.users_id                            -- para usuário atribuido
            LEFT JOIN glpi_itilcategories c ON c.id = t.itilcategories_id
            LEFT JOIN glpi_slas sa ON sa.id = t.slas_id_tto
            LEFT JOIN glpi_slas ss ON ss.id = t.slas_id_ttr
            -- WHERE t.status in (1,2)
            ORDER BY t.id
                """
        conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamados= pd.read_sql_query(sql_glpi,conMySQLGLPI)
        BotLog.gerarExcel(dfchamados,'dfchamados_ematendimento_novos'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S"))
    
        def esperarElemento(elemento):
            while self.limiteaguardarelemento < 60:
                time.sleep(1)
                BotLog.imprimirLog("Aguardando o elemento "+str(elemento))
                try:
                    self.driver.find_element("xpath",elemento)
                except Exception as e:
                    BotLog.imprimirLog(str(e))
                    self.limiteaguardarelemento+=1
                    continue
                self.limiteaguardarelemento = 0
                return True
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt')
        options.add_argument("--headless=new")    # para abrir no navegador no back end
        options.add_argument("--disable-notifications")  # Desabilitar notificações do navegador
        service = Service(executable_path=r"chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)
        BotLog.imprimirLog("Iniciando o Navegador")
        # self.driver = webdriver.Chrome(r"C:\Users\raisson.charles\Desktop\Python\RPA\02_essencial\chromedriver.exe", options=options)
        # self.driver = webdriver.Chrome(options=options,r"chromedriver.exe")
        url = 'http://chamado.pedreiraumvalemix.com.br/' 
        # url = 'http://localhost/glpi/' 
        self.driver.get(url)   
        # self.driver.maximize_window()
        # self.driver.minimize_window()
        BotLog.imprimirLog("Abrindo o GLPI")

        elemento = '//*[@id="login_name"]' # //*[@id="login_name"]
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        self.driver.find_element("xpath",elemento).send_keys(BotVar.dfparametros.query('NOME=="Usuario_Rede"')['VALOR'].iloc[0])
        # self.driver.find_element("xpath",elemento).click() 

        elemento = '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[3]/input' # 
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        self.driver.find_element("xpath",elemento).send_keys(BotVar.dfparametros.query('NOME=="Senha_Rede"')['VALOR'].iloc[0])
        # self.driver.find_element("xpath",elemento).click() 

        elemento = '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button' # botão logar /html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        # self.driver.find_element("xpath",elemento).send_keys("")
        elemt = self.driver.find_element("xpath",elemento)
        self.driver.execute_script("arguments[0].click();",elemt)
        BotLog.imprimirLog("Logando no GLPI")


        elemento = '/html/body/div[2]/aside/div/div[2]/ul/li[2]/a/span' # menu assitencia
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        # self.driver.find_element("xpath",elemento).send_keys("")
        self.driver.find_element("xpath",elemento).click() 


        elemento = '/html/body/div[2]/aside/div/div[2]/ul/li[2]/div/div/div[1]/a[2]/span' # menu chamados
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        # self.driver.find_element("xpath",elemento).send_keys("")
        elemt = self.driver.find_element("xpath",elemento)
        self.driver.execute_script("arguments[0].click();",elemt)
        BotLog.imprimirLog("Abrindo a tela de chamados")

        elemento = '/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[3]/div/span[1]/select' # selecionar o maximo de chamados para exibir
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        select_element = self.driver.find_element("xpath",elemento)
        # Criar um objeto Select para o elemento select
        select = Select(select_element)
        # Selecionar para exibir 10000 chamados
        select.select_by_value("10000")
        BotLog.imprimirLog("Exibindo o maximo de chamados")

        # forma antiga de mudar o select
        # self.driver.find_element("xpath",elemento).send_keys("")
        # self.driver.find_element("xpath",elemento).click() 
        # self.driver.find_element("xpath",elemento).send_keys("10000")
        # self.driver.find_element("xpath",elemento).send_keys(Keys.ENTER)

        elemento = '/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[2]/a[2]/i' # clicar para limpar o filtro
        esperarElemento(elemento)
        self.driver.find_element("xpath",elemento).click()
        BotLog.imprimirLog("Limpando os filtros")

        # /html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[6]/td[2]
        # /html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[7]/td[2]
        # /html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[1]/td[2]/span
        elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[3]/div/p[1]' # Verificando se possui chamados na tela
        try:
            total_chamados = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
            x = total_chamados.find('de')
            y = total_chamados.find('linhas')
            quant_chamados = int(total_chamados[x+3:y-1])
        except:
            BotLog.imprimirLog("Não possui chamados abertos ou em atendimentos")
            time.sleep(30)
            self.driver.quit()
            return
        elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[1]/td[5]/span/i' # 
        esperarElemento(elemento)
        coluna = 1
        numero_coluna_ta = 0
        numero_coluna_ts = 0
        BotLog.imprimirLog("Procurando a coluna de TA e TS")
        while True:
            elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/thead/tr/th[{coluna}]'
            try:
                nome_coluna = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
            except:
                BotLog.imprimirLog("Não conseguiu encontrar as colunas de TA e TS")
                time.sleep(30)
                self.driver.quit()
                return
            if 'Tempo para atendimento + Progresso' in nome_coluna:
                numero_coluna_ta = coluna
            if 'Tempo para solução + Progresso' in nome_coluna:
                numero_coluna_ts = coluna
            coluna+=1
            if numero_coluna_ta > 0 and numero_coluna_ts > 0:
                break
        BotLog.imprimirLog("Coluna TA: "+str(numero_coluna_ta)+" Coluna TS: "+str(numero_coluna_ts))
        linha = 1
        dfchamadosvencidos = pd.DataFrame(columns=['Numero','Status','Vencido','Data_Abertura','Tempo para atendimento','Tempo para solução','Solicitante','Entidade','Categoria','Titulo','Descricao'])
        BotLog.imprimirLog("Começando a verificação dos chamados, sao "+str(quant_chamados)+" Chamados")
        while linha <= quant_chamados:
            elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{linha}]/td[2]/span' # 
            try:
                numero = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
                if str(numero) in self.chamadosvencendoavisado:
                    BotLog.imprimirLog("O chamado "+str(numero)+' ja foi avisado hoje, pulando ele')
                    BotLog.imprimirLog("Imprimindo a lista de chamados vencendo ja avisado hoje")
                    BotLog.imprimirLog(str(self.chamadosvencendoavisado))
                    linha+=1
                    continue
                # if numero == 115 or numero == '115':
                #     print("")
            except:
                BotLog.imprimirLog("Não conseguiu pegar o TA do chamado "+str(numero))
                time.sleep(30)
                linha+=1
                continue
            BotLog.imprimirLog("Verificando chamado "+str(numero))
            progresso_sla_ta = 0
            progresso_sla_ts = 0
            elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{linha}]/td[5]/span/i' # 
            if not esperarElemento(elemento):
                break
            # status = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
            status = self.driver.find_element("xpath",elemento).get_attribute('data-bs-original-title')
            if status == 'Pendente':
                linha+=1
                BotLog.imprimirLog("Chamado "+str(numero)+" Pendente, pulando a linha")
                continue
            if status == 'Novo':
                elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{linha}]/td[{numero_coluna_ta}]/div/div'
                try:
                    progresso_sla_ta = self.driver.find_element("xpath",elemento).get_attribute('aria-valuenow')
                except:
                    BotLog.imprimirLog("Não conseguiu pegar o TA do chamado "+str(numero))
                    # time.sleep(30)
                    # linha+=1
                    # continue

            elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{linha}]/td[{numero_coluna_ts}]/div/div'
            try:
                progresso_sla_ts = self.driver.find_element("xpath",elemento).get_attribute('aria-valuenow')
            except:
                BotLog.imprimirLog("Não conseguiu pegar o TS do chamado "+str(numero))
                # time.sleep(30)
                # linha+=1
                # continue
            BotLog.imprimirLog("Chamado: "+str(numero)+" Status: "+str(status)+" TA: "+str(progresso_sla_ta)+" TS: "+str(progresso_sla_ts))
            if int(progresso_sla_ta) < 80 and int(progresso_sla_ts) < 80 :
                linha+=1
                continue

            if int(progresso_sla_ta) > 80 and int(progresso_sla_ts) > 80:
                BotLog.imprimirLog("Chamado "+str(numero)+" com TA "+str(progresso_sla_ta)+"%")

                dfchamados_linha = dfchamados[dfchamados['Numero']==int(numero)]
                if len(dfchamados_linha.index)==1:
                    numerodf = dfchamados_linha['Numero'].iloc[0]
                    solicitante = dfchamados_linha['Solicitante'].iloc[0]
                    entidade = dfchamados_linha['Entidade'].iloc[0]
                    categoria = dfchamados_linha['Categoria'].iloc[0]
                    categoria = categoria.replace('&#62;','>')
                    titulo = dfchamados_linha['Titulo'].iloc[0]
                    descricao = dfchamados_linha['Descricao'].iloc[0]
                    descricao_limpa = bot.limparDescricao(descricao)
                    descricao_limpa = descricao_limpa.replace('&#60;/p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;br&#62;',' ')
                    data_abertura = dfchamados_linha['Data_Abertura'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ta = dfchamados_linha['TA'].iloc[0]
                    ta = ta.replace("TA","Tempo para atendimento")
                    data_ta = dfchamados_linha['Data_TA'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ts = dfchamados_linha['TS'].iloc[0]
                    ts = ts.replace("TS","Tempo para solução")
                    data_ts = dfchamados_linha['Data_TS'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
                    link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TA '+str(progresso_sla_ta)+'%'+' TS '+str(progresso_sla_ts)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao_limpa}
                    dfchamadosvencidos = pd.concat([dfchamadosvencidos,pd.DataFrame([dic])], axis=0)
                    linha+=1
                    continue


                else:
                    BotLog.imprimirLog("O filtro pelo numero do chamado retornou mais de uma linha")

            if int(progresso_sla_ta) > 80:
                BotLog.imprimirLog("Chamado "+str(numero)+" com TA "+str(progresso_sla_ta)+"%")

                dfchamados_linha = dfchamados[dfchamados['Numero']==int(numero)]
                if len(dfchamados_linha.index)==1:
                    numerodf = dfchamados_linha['Numero'].iloc[0]
                    solicitante = dfchamados_linha['Solicitante'].iloc[0]
                    entidade = dfchamados_linha['Entidade'].iloc[0]
                    categoria = dfchamados_linha['Categoria'].iloc[0]
                    categoria = categoria.replace('&#62;','>')
                    titulo = dfchamados_linha['Titulo'].iloc[0]
                    descricao = dfchamados_linha['Descricao'].iloc[0]
                    descricao_limpa = bot.limparDescricao(descricao)
                    descricao_limpa = descricao_limpa.replace('&#60;/p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;br&#62;',' ')
                    data_abertura = dfchamados_linha['Data_Abertura'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ta = dfchamados_linha['TA'].iloc[0]
                    ta = ta.replace("TA","Tempo para atendimento")
                    data_ta = dfchamados_linha['Data_TA'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ts = dfchamados_linha['TS'].iloc[0]
                    ts = ts.replace("TS","Tempo para solução")
                    data_ts = dfchamados_linha['Data_TS'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
                    link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TA '+str(progresso_sla_ta)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao_limpa}
                    dfchamadosvencidos = pd.concat([dfchamadosvencidos,pd.DataFrame([dic])], axis=0)
                else:
                    BotLog.imprimirLog("O filtro pelo numero do chamado retornou mais de uma linha")

            if int(progresso_sla_ts) > 80:
                BotLog.imprimirLog("Chamado "+str(numero)+" com TS "+str(progresso_sla_ts)+"%")

                dfchamados_linha = dfchamados[dfchamados['Numero']==int(numero)]
                if len(dfchamados_linha.index)==1:
                    numerodf = dfchamados_linha['Numero'].iloc[0]
                    solicitante = dfchamados_linha['Solicitante'].iloc[0]
                    entidade = dfchamados_linha['Entidade'].iloc[0]
                    categoria = dfchamados_linha['Categoria'].iloc[0]
                    categoria = categoria.replace('&#62;','>')
                    titulo = dfchamados_linha['Titulo'].iloc[0]
                    descricao = dfchamados_linha['Descricao'].iloc[0]
                    descricao_limpa = bot.limparDescricao(descricao)
                    descricao_limpa = descricao_limpa.replace('&#60;/p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;p&#62;',' ')
                    descricao_limpa = descricao_limpa.replace('&#60;br&#62;',' ')
                    data_abertura = dfchamados_linha['Data_Abertura'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ta = dfchamados_linha['TA'].iloc[0]
                    ta = ta.replace("TA","Tempo para atendimento")
                    data_ta = dfchamados_linha['Data_TA'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    ts = dfchamados_linha['TS'].iloc[0]
                    ts = ts.replace("TS","Tempo para solução")
                    data_ts = dfchamados_linha['Data_TS'].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
                    # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
                    link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TS '+str(progresso_sla_ts)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao_limpa}
                    dfchamadosvencidos = pd.concat([dfchamadosvencidos,pd.DataFrame([dic])], axis=0)
                else:
                    BotLog.imprimirLog("O filtro pelo numero do chamado retornou mais de uma linha")

            

            # print(dado_html)
            # print("")
            # self.driver.find_element("xpath",elemento).send_keys("")
            # self.driver.find_element("xpath",elemento).click() 
            linha+=1
        
        for x in range(len(dfchamadosvencidos.index)):
            # ‼️⚠️👩‍🦰🆕📪📫📬📮📭✉️📩📨📥📤❗️🧨
            numerodf = dfchamadosvencidos['Numero'].iloc[x]
            status = dfchamadosvencidos['Status'].iloc[x]
            solicitante = dfchamadosvencidos['Solicitante'].iloc[x]
            entidade = dfchamadosvencidos['Entidade'].iloc[x]
            categoria = dfchamadosvencidos['Categoria'].iloc[x]
            titulo = dfchamadosvencidos['Titulo'].iloc[x]
            descricao = dfchamadosvencidos['Descricao'].iloc[x]
            data_abertura = dfchamadosvencidos['Data_Abertura'].iloc[x]

            data_ta = dfchamadosvencidos['Tempo para atendimento'].iloc[x] #.strftime('%d-%m-%Y %H:%M:%S')
            data_ts = dfchamadosvencidos['Tempo para solução'].iloc[x] #.strftime('%d-%m-%Y %H:%M:%S')
            vencido = dfchamadosvencidos['Vencido'].iloc[x]
            # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
            link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
            if status == 'Novo':
                status = '📫 '+status 
            else:
                status = '📬 '+status 
            mensagem = f""" 🔴 Chamado Vencendo!🔴
            🎟 {numerodf}
            {status}
            📅 {data_abertura}
            ⏱ {data_ta}
            ⏰ {data_ts}
            🧨 {vencido}
            👤 {solicitante}
            🏢 {entidade}
            🏷 {categoria}
            ✏️ {titulo}
            🗒 {descricao}
            🔗 {link}{numerodf}
            """.replace("    ","")
            try:
                BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
                BotLog.imprimirLog("Adicionando o chamado "+str(numerodf)+" a lista de numeros de chamados que ja foram avisados hoje")
                self.chamadosvencendoavisado.append(str(numerodf))
                BotLog.imprimirLog("Imprimindo a lista de chamados vencendo ja avisado hoje")
                BotLog.imprimirLog(str(self.chamadosvencendoavisado))
            except Exception as e:
                msg_erro = "Erro no envio da mensagem pelo telegram de ta vencendo, mensagem de erro: "+str(e)
                BotLog.imprimirLog(msg_erro)


        self.driver.quit()
        self.conterro = 0
        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO CHAMADOS VENCENDO ###########################################################")
    def chamadosVencendo(self):
        sql_glpi = f"""
                    SELECT  t.id Numero,
                            u1.name Solicitante, 
                            e.name Entidade, 
                            i.name Categoria,   
                            t.name Titulo, 
                            t.content Descricao,
                            DATE_FORMAT(t.date_creation, '%d-%m-%Y') Data_Abertura
                            ,t.status Status
                            ,IFNULL(u2.name,"") Tecnico
                            ,DATE_FORMAT(t.date, '%d-%m-%Y %T') Data_Hora_Abertura, 
                            IFNULL(DATE_FORMAT(t.takeintoaccountdate, '%d-%m-%Y %T'),"") Data_Hora_Atendimento
                            ,ta.name TA,
                            ts.name TS,
                            DATE_FORMAT(t.time_to_own, '%d-%m-%Y %T') 'Tempo para atendimento',
                            DATE_FORMAT(t.time_to_resolve, '%d-%m-%Y %T') 'Tempo para solução',
                            t.sla_waiting_duration Tempo_Espera_Segundos
                    FROM glpi_tickets t
                    left JOIN glpi_entities e ON e.id=t.entities_id
                    left JOIN glpi_tickets_users tu2 ON tu2.tickets_id=t.id AND tu2.type = 2 -- para tecnico
                    left JOIN glpi_users u2 ON u2.id=tu2.users_id -- para tecnico
                    left JOIN glpi_tickets_users tu1 ON tu1.tickets_id=t.id AND tu1.type = 1 -- para usuário atribuido
                    left JOIN glpi_users u1 ON u1.id=tu1.users_id -- para usuário
                    left JOIN glpi_itilcategories i ON i.id=t.itilcategories_id
                    left JOIN glpi_slas ta ON ta.id=t.slas_id_tto -- tempo para atendimento
                    left JOIN glpi_slas ts ON ts.id=t.slas_id_ttr -- tempo para solução
                    WHERE t.is_deleted = 0  AND t.status IN (1,2)
                    GROUP BY t.id -- Agrupando pelo numero porque tem um chamado de numero 173 duplicado poque foi atribuido a dois tecnicos
                    ORDER BY t.id
        """
        conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamadosvencendo= pd.read_sql_query(sql_glpi,conMySQLGLPI)
        dfchamadosvencendo["TA_S"] = 0 # Iniciando a coluna para armazenar o TA do chamado em segundos 
        dfchamadosvencendo["TS_S"] = 0 # Iniciando a coluna para armazenar o TS do chamado em segundos 
        dfchamadosvencendo["TA_S_A"] = 0 # Iniciando a coluna para armazenar o TA percorrido do chamado
        dfchamadosvencendo["TS_S_A"] = 0 # Iniciando a coluna para armazenar o TS percorrido do chamado
        dfchamadosvencendo["TA_P"] = 0 # Iniciando a coluna para armazenar o percentual do TA
        dfchamadosvencendo["TS_P"] = 0 # Iniciando a coluna para armazenar o percentual do TS

        for linha, valor in enumerate(dfchamadosvencendo['Data_Hora_Abertura']):
            print(dfchamadosvencendo['Numero'].iloc[linha])
            if not dfchamadosvencendo['Tecnico'].iloc[linha] and dfchamadosvencendo['Data_Hora_Atendimento'].iloc[linha]: #Verifica se o chamado foi respondido se ser atribuido
                # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
                link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
                id_chamado = str(dfchamadosvencendo['id'].iloc[linha])
                msg = f"""❗️ Atenção, Chamado {id_chamado} foi iniciado antendiemnto mas esta sem tecnico definido ❗️
                        🔗 {link}{id_chamado}
                        """.replace("    ","")
                BotLog.imprimirLog(msg)
                BotVar.BotTelegram.send_message(int(self.id_telegram),msg)
            if not dfchamadosvencendo['Data_Hora_Atendimento'].iloc[linha]: #Caucula o tempo TA caso a coluna esteja em branco, não tenha iniciado atendimento
                print("Chamado "+str(dfchamadosvencendo['Numero'].iloc[linha])+" ainda não foi iniciado antendiemnto, verificando TA")
                dfchamadosvencendo["TA_S"].iloc[linha] = self.tempoComercial(dfchamadosvencendo['Data_Hora_Abertura'].iloc[linha],dfchamadosvencendo['Tempo para atendimento'].iloc[linha]) #Cauculando TA em segundos
                dfchamadosvencendo["TA_S_A"].iloc[linha] = self.tempoComercial(dfchamadosvencendo['Data_Hora_Abertura'].iloc[linha]) #Cauculando o tempo TA percorrido ate a hora atual em segundos
                dfchamadosvencendo["TA_P"].iloc[linha] = round(((dfchamadosvencendo["TA_S_A"].iloc[linha] / dfchamadosvencendo["TA_S"].iloc[linha])*100),2) # Cauculando o percentual do TA percorrido
                # ta_percentual = round(ta_percentual,2)
            
            dfchamadosvencendo["TS_S"].iloc[linha] = self.tempoComercial(dfchamadosvencendo['Data_Hora_Abertura'].iloc[linha],dfchamadosvencendo['Tempo para solução'].iloc[linha]) #Cauculando TS em segundos
            dfchamadosvencendo["TS_S_A"].iloc[linha] = self.tempoComercial(dfchamadosvencendo['Data_Hora_Abertura'].iloc[linha]) #Cauculando o tempo TS percorrido ate a hora atual em segundos
            dfchamadosvencendo["TS_P"].iloc[linha] = round(((dfchamadosvencendo["TS_S_A"].iloc[linha] / dfchamadosvencendo["TS_S"].iloc[linha])*100),2) # Cauculando o percentual do TS percorrido

        # dfchamadosvencendo["TA_P"].iloc[0] = 92
        dfchamadosvencidos = dfchamadosvencendo.query('TA_P > 80 | TS_P > 80')
        print("")

        for x in range(len(dfchamadosvencidos.index)):
            # ‼️⚠️👩‍🦰🆕📪📫📬📮📭✉️📩📨📥📤❗️🧨
            numerodf = dfchamadosvencidos['Numero'].iloc[x]
            status = dfchamadosvencidos['Status'].iloc[x]
            solicitante = dfchamadosvencidos['Solicitante'].iloc[x]
            entidade = dfchamadosvencidos['Entidade'].iloc[x]
            categoria = dfchamadosvencidos['Categoria'].iloc[x]
            titulo = dfchamadosvencidos['Titulo'].iloc[x]
            descricao = dfchamadosvencidos['Descricao'].iloc[x]
            data_abertura = dfchamadosvencidos['Data_Abertura'].iloc[x]

            data_ta = dfchamadosvencidos['Tempo para atendimento'].iloc[x] #.strftime('%d-%m-%Y %H:%M:%S')
            data_ts = dfchamadosvencidos['Tempo para solução'].iloc[x] #.strftime('%d-%m-%Y %H:%M:%S')
            vencido = dfchamadosvencidos['Vencido'].iloc[x]
            # link = r'http://sistemas:8080/glpi/front/ticket.form.php?id='
            link = BotVar.dfparametros.query('NOME=="link_glpi"')['VALOR'].iloc[0]
            if status == 'Novo':
                status = '📫 '+status 
            else:
                status = '📬 '+status 
            mensagem = f""" 🔴 Chamado Vencendo!🔴
            🎟 {numerodf}
            {status}
            📅 {data_abertura}
            ⏱ {data_ta}
            ⏰ {data_ts}
            🧨 {vencido}
            👤 {solicitante}
            🏢 {entidade}
            🏷 {categoria}
            ✏️ {titulo}
            🗒 {descricao}
            🔗 {link}{numerodf}
            """.replace("    ","")
            try:
                BotVar.BotTelegram.send_message(int(self.id_telegram),mensagem)
                BotLog.imprimirLog("Adicionando o chamado "+str(numerodf)+" a lista de numeros de chamados que ja foram avisados hoje")
                self.chamadosvencendoavisado.append(str(numerodf))
                BotLog.imprimirLog("Imprimindo a lista de chamados vencendo ja avisado hoje")
                BotLog.imprimirLog(str(self.chamadosvencendoavisado))
            except Exception as e:
                msg_erro = "Erro no envio da mensagem pelo telegram de ta vencendo, mensagem de erro: "+str(e)
                BotLog.imprimirLog(msg_erro)

        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO CHAMADOS VENCENDO ###########################################################")
    def chamadosPendente(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO CHAMADOS PENDENTES ###########################################################")
        sql = """
                SELECT 
                    t.id  Numero
                    , DATE_FORMAT(t.date, '%d-%m-%Y %T') Data_Abertura
                    , IFNULL(DATE_FORMAT(t.begin_waiting_date, '%d-%m-%Y %T'),"") Inicio_Espera
                    ,t.waiting_duration Tempo_Pendente_Segundos
                   -- ,concat(HOUR(SEC_TO_TIME(t.waiting_duration)),":",LPAD(MINUTE(SEC_TO_TIME(t.waiting_duration)),2,0)) Tempo_Pendente_Horas
                    , IFNULL(u2.name,"") Tecnico
                    , i.name Categoria
                FROM glpi_tickets t
                left JOIN glpi_tickets_users tu2 ON tu2.tickets_id=t.id AND tu2.type = 2 -- para tecnico
                left JOIN glpi_users u2 ON u2.id=tu2.users_id -- para tecnico
                left JOIN glpi_itilcategories i ON i.id=t.itilcategories_id
                WHERE t.is_deleted = 0  AND t.status = 4 
                GROUP BY t.id -- Agrupando pelo numero porque tem um chamado de numero 173 duplicado poque foi atribuido a dois tecnicos
                ORDER BY t.begin_waiting_date
            """
        conMySQLGLPI = MySQLdb.connect(host=BotVar.serverMySQL,user=BotVar.usermysql,passwd=BotVar.senhamysql,db='glpi') #Criando a conexão
        dfchamadospendente= pd.read_sql_query(sql,conMySQLGLPI)

        dfchamadospendente['Tempo_Pendente_Segundos_Atual'] = 0
        dfchamadospendente['Tempo_Pendente_Segundos_Total'] = 0
        dfchamadospendente['Horas_Pendente'] = 0
        total_chamados_pendentes = len(dfchamadospendente.index)
        for x, data in enumerate(dfchamadospendente['Inicio_Espera']):
            # data = dfchamadospendente['Inicio_Espera'].iloc[0]
            tempo_segundos =  bot.tempoComercial(data)
            dfchamadospendente['Tempo_Pendente_Segundos_Atual'].iloc[x] = tempo_segundos
            tempo_pendente_total_Segundos = tempo_segundos + dfchamadospendente['Tempo_Pendente_Segundos'].iloc[x]
            dfchamadospendente['Tempo_Pendente_Segundos_Total'].iloc[x] = tempo_pendente_total_Segundos
            horas_pendentes = bot.segundos_para_horas_minutos(tempo_pendente_total_Segundos)
            dfchamadospendente['Horas_Pendente'].iloc[x] = horas_pendentes
        
        nome_arquivo = 'dfchamados_pendentes_historico'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        BotLog.gerarExcel(dfchamadospendente,nome_arquivo)

        dfchamadospendente = dfchamadospendente.sort_values(['Tempo_Pendente_Segundos_Total'],ascending = False)
        
        ultima_linha = {'Numero':'Total de Chamados','Data_Abertura':total_chamados_pendentes}
        dfchamadospendente.loc[total_chamados_pendentes+1]=ultima_linha
        # dfchamadospendente = dfchamadospendente.append(ultima_linha)
        dfchamadospendente = dfchamadospendente.drop(columns=['Tempo_Pendente_Segundos_Total'])
        dfchamadospendente = dfchamadospendente.drop(columns=['Tempo_Pendente_Segundos_Atual'])
        dfchamadospendente = dfchamadospendente.drop(columns=['Tempo_Pendente_Segundos'])

        nome_arquivo = 'dfchamados_pendentes_'+datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        BotLog.gerarExcel(dfchamadospendente,nome_arquivo)
        caminho_arquivo = r"log\\log"+BotLog.nomedir+"\\dataframe\\"+nome_arquivo+'_'+str(BotLog.contexcel)+".xlsx"

        BotLog.imprimirLog("Mudando o status para executando")
        BotTarefas.MudarStatus("Executando")
        BotLog.imprimirLog("Verificando prioridade")
        BotTarefas.VerificaPrioridade()

        # Comando para abrir o arquivo Excel com o aplicativo Excel
        comando_excel = [self.caminho_excel, caminho_arquivo]

        # Subprocesso para executar o comando
        subprocess.Popen(comando_excel)
        
        if not BotGerenciadorJanelas.esperarTitulo(0,30,'dfchamados_pendentes',2):
            raise Exception("Erro ao abrir a planilha com os chamados pendentes")
        BotGerenciadorJanelas.ativarTela('dfchamados_pendentes',2)

        time.sleep(10)
        pyautogui.hotkey("ctrl","t")
        time.sleep(10)
        pyautogui.hotkey('alt','c','o','t')
        time.sleep(10)
        pyautogui.hotkey("ctrl","c")
        time.sleep(10)

        paint = ['mspaint']
        subprocess.Popen(paint)

        if not BotGerenciadorJanelas.esperarTitulo(0,30,'Paint',2):
            raise Exception("Erro na hora de abrir o paint")

        time.sleep(4)
        pyautogui.hotkey("ctrl","v")
        time.sleep(4)

        pyautogui.press('f12')
        time.sleep(4)

        self.limiteaguardartitulo = 0
        self.limiteaguardartitulomaximo = 60
        if self.sistema == '10':
            BotGerenciadorJanelas.esperarTitulo(0,30,'Salvar como',2)
        elif self.sistema == '11':
            BotGerenciadorJanelas.esperarTitulo(0,30,'Save As',2)

        time.sleep(4)
        nome_print = CaminhoProjeto+r"\log\log"+BotLog.nomedir+r"\print\print"+str(BotLog.contprint)+'.jpg'
        BotLog.contprint+=1
        pyautogui.write(nome_print)

        time.sleep(4)
        pyautogui.hotkey("alt","l")
        time.sleep(4)
        subprocess.call(["taskkill", "/S", 'localhost',  "/FI", "IMAGENAME eq Excel*"])
        subprocess.call(["taskkill", "/S", 'localhost',  "/FI", "IMAGENAME eq mspaint*"])
        BotVar.BotTelegram.send_photo(int(bot.id_telegram),open(nome_print,'rb'))
        self.enviar_pendentes = False
        BotLog.imprimirLog("########################################################### FINALIZANDO MODULO CHAMADOS PENDENTES ###########################################################")
       
bot = GLPI()






# BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"] = '452405307'
# BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_iniciofim","VALOR"] = '452405307'
# bot.id_telegram = '452405307'
# bot.tempo = 5
# bot.chamadosVencendo()



BotLog.InicioFim("InicioExecucao")
teste = datetime.datetime.now()
bot.horariotermino = bot.horariotermino + timedelta(days=1)
while bot.horariotermino>=datetime.datetime.now():
    if bot.enviar_pendentes:
        try: # chamados Pendentes
            bot.chamadosPendente()
            BotLog.imprimirLog("Mudando o status para Parado")
            BotTarefas.MudarStatus("Parado")
        except Exception as e:
            BotLog.imprimirLog("Mudando o status para Parado")
            BotTarefas.MudarStatus("Parado")
            msg = f"Erro no modulo chamadosPendentes: {e}"
            BotLog.imprimirLog(msg)
            BotVar.BotTelegram.send_message(int(BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"]),msg)   
    try:
        bot.novoChamado()
    except Exception as e:
        msg_erro = "Erro no modulo que verifica novos chamados, mensagem de erro: "+str(e)
        BotLog.imprimirLog(msg_erro)
        BotVar.BotTelegram.send_message(int(BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"]),msg_erro)    
    try:
        bot.chamadosVencendoWeb()
    except Exception as e:
        bot.conterro+=1
        msg_erro = "Erro no modulo que verifica os chamados que estão vencendo, mensagem de erro: "+str(e)
        BotLog.imprimirLog(msg_erro)
        if bot.conterro > 2:
            BotVar.BotTelegram.send_message(int(BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"]),msg_erro)
    bot.relogio_timer(bot.tempo)
    BotLog.imprimirLog("Data e hora configurardo para finalizar o Celim: "+bot.horariotermino.strftime('%d-%m-%Y %H:%M'))
    BotLog.imprimirLog('Data e hora atual: '+datetime.datetime.now().strftime('%d-%m-%Y %H:%M'))
    
BotFinalizar.finalizarExecucao("Finalizando na ultima linha")
# bot.InicioFim("FimExecucao")
# BotFinalizar.finalizarExecucao("Finalizando execução com sucesso na ultima linha")

















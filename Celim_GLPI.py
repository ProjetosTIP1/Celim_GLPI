import datetime
from datetime import timedelta
import cryptocode # para criptografia
import MySQLdb
import pandas as pd
import time
import telebot
import sys # para importação relativa
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select



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

        self.chamadosvencendoavisado = [] # lista com chamados vencendo que ja foi avisado
        self.limiteaguardarelemento = 0


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
    def chamadosVencendoWeb(self):
        BotLog.imprimirLog("########################################################### INICIANDO MODULO CHAMADOS VENCENDO ###########################################################")

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
        # self.driver = webdriver.Chrome(r"C:\Users\raisson.charles\Desktop\Python\RPA\02_essencial\chromedriver.exe", options=options)
        # self.driver = webdriver.Chrome(options=options,r"chromedriver.exe")
        url = 'http://192.168.11.50:8080/glpi/' # site depois do qr code
        # url = 'http://localhost/glpi/' # site depois do qr code
        # url = 'https://www.bancointer.com.br/' # site depois do qr code
        self.driver.get(url)   
        # self.driver.maximize_window()
        # self.driver.minimize_window()

        elemento = '//*[@id="login_name"]' # //*[@id="login_name"]
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        self.driver.find_element("xpath",elemento).send_keys("celim")
        # self.driver.find_element("xpath",elemento).click() 

        elemento = '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[3]/input' # 
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        self.driver.find_element("xpath",elemento).send_keys("Rpa@celim")
        # self.driver.find_element("xpath",elemento).click() 

        elemento = '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button' # botão logar /html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        # self.driver.find_element("xpath",elemento).send_keys("")
        elemt = self.driver.find_element("xpath",elemento)
        self.driver.execute_script("arguments[0].click();",elemt)


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

        elemento = '/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[3]/div/span[1]/select' # selecionar o maximo de chamados para exibir
        esperarElemento(elemento)
        # dado_html = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
        select_element = self.driver.find_element("xpath",elemento)
        # Criar um objeto Select para o elemento select
        select = Select(select_element)
        # Selecionar para exibir 10000 chamados
        select.select_by_value("10000")

        # forma antiga de mudar o select
        # self.driver.find_element("xpath",elemento).send_keys("")
        # self.driver.find_element("xpath",elemento).click() 
        # self.driver.find_element("xpath",elemento).send_keys("10000")
        # self.driver.find_element("xpath",elemento).send_keys(Keys.ENTER)

        elemento = '/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[2]/a[2]/i' # clicar para limpar o filtro
        esperarElemento(elemento)
        self.driver.find_element("xpath",elemento).click()

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
        linha = 1
        dfchamadosvencidos = pd.DataFrame(columns=['Numero','Status','Vencido','Data_Abertura','Tempo para atendimento','Tempo para solução','Solicitante','Entidade','Categoria','Titulo','Descricao'])
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
            progresso_sla_ta = 0
            progresso_sla_ts = 0
            elemento = f'/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{linha}]/td[5]/span/i' # 
            if not esperarElemento(elemento):
                break
            # status = self.driver.find_element("xpath",elemento).get_attribute('innerHTML')
            status = self.driver.find_element("xpath",elemento).get_attribute('data-bs-original-title')
            if status == 'Pendente':
                linha+=1
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
                    link = r'http://192.168.11.50:8080/glpi/front/ticket.form.php?id='
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TA '+str(progresso_sla_ta)+'%'+' TS '+str(progresso_sla_ts)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao}
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
                    link = r'http://192.168.11.50:8080/glpi/front/ticket.form.php?id='
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TA '+str(progresso_sla_ta)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao}
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
                    link = r'http://192.168.11.50:8080/glpi/front/ticket.form.php?id='
                    dic = {'Numero':numerodf,'Status':status,'Vencido':'TS '+str(progresso_sla_ts)+'%','Data_Abertura':data_abertura,
                           'Tempo para atendimento':data_ta,'Tempo para solução':data_ts,'Solicitante':solicitante,'Entidade':entidade,
                           'Categoria':categoria,'Titulo':titulo,'Descricao':descricao}
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
            link = r'http://192.168.11.50:8080/glpi/front/ticket.form.php?id='
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
            🗒 {descricao_limpa}
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
    def chamadosvencendo(Self):
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

# bot.id_telegram = '452405307'

teste = datetime.datetime.now()
bot.horariotermino = bot.horariotermino + timedelta(days=1)
while bot.horariotermino>=datetime.datetime.now():
    try:
        bot.novoChamado()
    except Exception as e:
        msg_erro = "Erro no modulo que verifica novos chamados, mensagem de erro: "+str(e)
        BotLog.imprimirLog(msg_erro)
        BotVar.BotTelegram.send_message(int(BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"]),msg_erro)    
    try:
        bot.chamadosVencendoWeb()
    except Exception as e:
        msg_erro = "Erro no modulo que verifica os chamados que estão vencendo, mensagem de erro: "+str(e)
        BotLog.imprimirLog(msg_erro)
        BotVar.BotTelegram.send_message(int(BotVar.dfparametros.loc[BotVar.dfparametros['NOME']=="id_telegram_alertas","VALOR"]),msg_erro)
    # bot.relogio_timer(5)
    bot.relogio_timer(300)
    


# BotFinalizar.finalizarExecucao("Finalizando execução com sucesso na ultima linha")

















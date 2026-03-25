
import MySQLdb
import pandas as pd
import matplotlib

sql_glpi = f"""
           SELECT * FROM glpi_tickets
                """
conMySQLGLPI = MySQLdb.connect(host='DC-P1-SISTEMA',user='pedreiraumvx',passwd='Admin@#2022!@#',db='glpi') #Criando a conexão
dfchamados= pd.read_sql_query(sql_glpi,conMySQLGLPI)



# import pandas as pd
# import os
# import MySQLdb
# import matplotlib
import datetime
# from datetime import timedelta


teste = datetime.datetime.now()
testestr = teste.strftime('%d/%m/%Y %H:%M:%S')
testedt = datetime.datetime.strptime(testestr,'%d/%m/%Y %H:%M:%S')

# data_abertura = datetime.datetime.strptime(dataset.loc[x, 'Data_Hora_Abertura'], '%Y-%d-%m %H:%M:%S')
# data_abertura = data_abertura.strftime("%d-%m-%Y %H:%M:%S")


def tempoComercial(data_inicio_str,data_fim_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
    conMySQLGLPI = MySQLdb.connect(host='DC-P1-SISTEMA',user='pedreiraumvx',passwd='Admin@#2022!@#',db='glpi') #Criando a conexão
    sql_holidays = f"""
        SELECT id, name, begin_date, end_date, is_perpetual
        FROM glpi_holidays
        ORDER BY id
        """
    dfholidays= pd.read_sql_query(sql_holidays,conMySQLGLPI)
    # Criando uma lista com os feriado
    feriados = []
    total_feriados = len(dfholidays.index)
    for x_holiday in range(total_feriados):
        # id = dfholidays['id'].iloc[x_holiday]
        id = dfholidays.loc[x,'id']
        # name = dfholidays['name'].iloc[x_holiday]
        name = dfholidays.loc[x,'name']
        # begin_data = dfholidays['begin_date'].iloc[x_holiday]
        begin_data = dfholidays.loc[x,'begin_date']
        # end_date = dfholidays['end_date'].iloc[x_holiday]
        end_date = dfholidays.loc[x,'end_date']
        # is_perpetual = dfholidays['is_perpetual'].iloc[x_holiday]
        is_perpetual = dfholidays.loc[x,'is_perpetual']
        if is_perpetual == 1: # condição para feriados perpetuos
            if begin_data.year != end_date.year:
                msg = f"""Erro 
                    Intervalo de datas na tabela de feriado com anos diferentes, favor corrigir.
                    Data inicio: {begin_data.strftime("%d-%m-%Y")}
                    Data Fim: {end_date.strftime("%d-%m-%Y")}
                    Nome do feriado: {name}
                    """
                msg = msg.replace("  ","")
                print(msg)
            if begin_data.year != datetime.datetime.now().date().year:
                # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                begin_data = begin_data.replace(year=datetime.datetime.now().date().year)                        
            if end_date.year != datetime.datetime.now().date().year:
                # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                end_date = end_date.replace(year=datetime.datetime.now().date().year)
        if begin_data == end_date:
            # print("Datas de inicio e fim de feriado iguais")
            feriados.append(begin_data)
        elif begin_data > end_date: # Inicio do feriado não pode ser maior que o fim
            msg = "A data de id "+str(id)+' e nome '+str(name)+' na tabela de calendario esta com uma data de inicio maior que a data de fim.'
            print(msg)
        elif begin_data < end_date: #Adiciona o intervalo de datas do feriado
            # print("Datas diferentes, percorrendo as datas")
            difer_dias = end_date - begin_data
            difer_dias = difer_dias.days
            while begin_data <= end_date:
                feriados.append(begin_data)
                begin_data = begin_data + datetime.timedelta(days=1)


    data_inicio_dt = datetime.datetime.strptime(data_inicio_str,"%d-%m-%Y %H:%M:%S")
    data_fim_dt = datetime.datetime.strptime(data_fim_str,"%d-%m-%Y %H:%M:%S")
    date = data_inicio_dt.date()
    hour = data_inicio_dt.time()
    tempo_segundos = 0

    while data_inicio_dt.date() <= data_fim_dt.date():
        dia_semana = data_inicio_dt.weekday() 
        if data_inicio_dt.weekday() == 5 or data_inicio_dt.weekday() == 6: # pular um dia se for final de semana
            # print("Final de semana")
            data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
            data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
            continue
        if data_inicio_dt.date() in feriados: # pular um dia se for feriado
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
    return tempo_segundos

sql_glpi = f"""
            SELECT 
                    t.id,
                    e.name AS Entidade,
                    DATE_FORMAT(t.date, '%d-%m-%Y') DATA, 
                    i.name Categoria, 
                    u1.name Usuario, 
                    IFNULL(u2.name,"") Tecnico,
                    DATE_FORMAT(t.date, '%d-%m-%Y %T') Data_Hora_Abertura, 
                    IFNULL(DATE_FORMAT(t.takeintoaccountdate, '%d-%m-%Y %T'),"") Data_Hora_Atendimento,
                    IFNULL(DATE_FORMAT(t.begin_waiting_date, '%d-%m-%Y %T'),"") Data_Hora_Inicio_Espera,
                    IFNULL(DATE_FORMAT(t.closedate, '%d-%m-%Y %T'),"") Data_Hora_Fechamento,
                    CASE
                            WHEN t.status = 6 THEN "FECHADO"
                            WHEN t.status = 4 THEN "PENDENTE"
                            WHEN t.status = 5 THEN "SOLUCIONADO"	
                            WHEN t.status = 2 THEN "EM ATENDIMENTO"		
                            WHEN t.status = 1 THEN "NOVO"	
                            ELSE t.status
                    END STATUS,
                    ta.name TA,
                    ts.name TS,
                    DATE_FORMAT(t.time_to_own, '%d-%m-%Y %T') Tempo_Atendimento,
                    DATE_FORMAT(t.time_to_resolve, '%d-%m-%Y %T') Tempo_Solução,
                    t.takeintoaccount_delay_stat Tempo_Atendimento_Segundos,
                    concat(HOUR(SEC_TO_TIME(t.takeintoaccount_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.takeintoaccount_delay_stat)),2,0)) Tempo_Atendimento_Horas,
                    t.solve_delay_stat Tempo_Solução_Segundos,
                    concat(HOUR(SEC_TO_TIME(t.solve_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.solve_delay_stat)),2,0)) Tempo_Solução_Horas,
                    t.close_delay_stat Tempo_Fechamento_Segundos,
                    concat(HOUR(SEC_TO_TIME(t.close_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.close_delay_stat)),2,0)) Tempo_Fechamento_Horas,
                    t.waiting_duration Tempo_Pendente_Segundos,
                    concat(HOUR(SEC_TO_TIME(t.waiting_duration)),":",LPAD(MINUTE(SEC_TO_TIME(t.waiting_duration)),2,0)) Tempo_Pendente_Horas
            FROM glpi_tickets t
            left JOIN glpi_entities e ON e.id=t.entities_id
            left JOIN glpi_locations l ON l.id=t.locations_id
            left JOIN glpi_tickets_users tu2 ON tu2.tickets_id=t.id AND tu2.type = 2 -- para tecnico
            left JOIN glpi_users u2 ON u2.id=tu2.users_id -- para tecnico
            left JOIN glpi_tickets_users tu1 ON tu1.tickets_id=t.id AND tu1.type = 1 -- para usuário atribuido
            left JOIN glpi_users u1 ON u1.id=tu1.users_id -- para usuário
            left JOIN glpi_itilcategories i ON i.id=t.itilcategories_id
            left JOIN glpi_slas ta ON ta.id=t.slas_id_tto -- tempo para atendimento
            left JOIN glpi_slas ts ON ts.id=t.slas_id_ttr -- tempo para solução
            WHERE t.is_deleted = 0  -- AND t.date_creation > '2023-06-01'  AND t.date_creation < '2023-07-01'   -- AND t.id = 42
            GROUP BY t.id 
                """
conMySQLGLPI = MySQLdb.connect(host='DC-P1-SISTEMA',user='pedreiraumvx',passwd='Admin@#2022!@#',db='glpi') #Criando a conexão
dfchamados= pd.read_sql_query(sql_glpi,conMySQLGLPI)

dfchamados['Tempo_Previsto_SLA_TS_Segundos'] = 0
# dfchamados.to_excel("teste.xlsx",index = False)
for x in range(len(dfchamados.index)):
    abertura, solucao = dfchamados['Data_Hora_Abertura'].iloc[x],dfchamados['Tempo_Solução'].iloc[x]
    dfchamados['Tempo_Previsto_SLA_TS_Segundos'].iloc[x] = tempoComercial(abertura, solucao)
    # dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial(dataset.loc[x,'Data_Hora_Abertura'],dataset.loc[x,'Tempo_Solução'])




if 1==2:
    # 'dataset' tem os dados de entrada para este script

    import pandas as pd
    import os
    import MySQLdb
    import matplotlib
    import datetime
    from datetime import timedelta

    def tempoComercial(data_inicio_str,data_fim_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
        conMySQLGLPI = MySQLdb.connect(host='DC-P1-SISTEMA',user='pedreiraumvx',passwd='Admin@#2022!@#',db='glpi') #Criando a conexão
        sql_holidays = f"""
            SELECT id, name, begin_date, end_date, is_perpetual
            FROM glpi_holidays
            ORDER BY id
            """
        dfholidays= pd.read_sql_query(sql_holidays,conMySQLGLPI)
        # Criando uma lista com os feriado
        feriados = []
        total_feriados = len(dfholidays.index)
        for x_holiday in range(total_feriados):
            # id = dfholidays['id'].iloc[x_holiday]
            id = dfholidays.loc[x,'id']
            # name = dfholidays['name'].iloc[x_holiday]
            name = dfholidays.loc[x,'name']
            # begin_data = dfholidays['begin_date'].iloc[x_holiday]
            begin_data = dfholidays.loc[x,'begin_date']
            # end_date = dfholidays['end_date'].iloc[x_holiday]
            end_date = dfholidays.loc[x,'end_date']
            # is_perpetual = dfholidays['is_perpetual'].iloc[x_holiday]
            is_perpetual = dfholidays.loc[x,'is_perpetual']
            if is_perpetual == 1: # condição para feriados perpetuos
                if begin_data.year != end_date.year:
                    msg = f"""Erro 
                        Intervalo de datas na tabela de feriado com anos diferentes, favor corrigir.
                        Data inicio: {begin_data.strftime("%d-%m-%Y")}
                        Data Fim: {end_date.strftime("%d-%m-%Y")}
                        Nome do feriado: {name}
                        """
                    msg = msg.replace("  ","")
                    print(msg)
                if begin_data.year != datetime.datetime.now().date().year:
                    # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                    begin_data = begin_data.replace(year=datetime.datetime.now().date().year)                        
                if end_date.year != datetime.datetime.now().date().year:
                    # print("Ano de inicio do feriado diferente do ano atual, ajustando para o ano atual")
                    end_date = end_date.replace(year=datetime.datetime.now().date().year)
            if begin_data == end_date:
                # print("Datas de inicio e fim de feriado iguais")
                feriados.append(begin_data)
            elif begin_data > end_date: # Inicio do feriado não pode ser maior que o fim
                msg = "A data de id "+str(id)+' e nome '+str(name)+' na tabela de calendario esta com uma data de inicio maior que a data de fim.'
                print(msg)
            elif begin_data < end_date: #Adiciona o intervalo de datas do feriado
                # print("Datas diferentes, percorrendo as datas")
                difer_dias = end_date - begin_data
                difer_dias = difer_dias.days
                while begin_data <= end_date:
                    feriados.append(begin_data)
                    begin_data = begin_data + datetime.timedelta(days=1)


        data_inicio_dt = datetime.datetime.strptime(data_inicio_str,"%d-%m-%Y %H:%M:%S")
        data_fim_dt = datetime.datetime.strptime(data_fim_str,"%d-%m-%Y %H:%M:%S")
        date = data_inicio_dt.date()
        hour = data_inicio_dt.time()
        tempo_segundos = 0

        while data_inicio_dt.date() <= data_fim_dt.date():
            dia_semana = data_inicio_dt.weekday() 
            if data_inicio_dt.weekday() == 5 or data_inicio_dt.weekday() == 6: # pular um dia se for final de semana
                # print("Final de semana")
                data_inicio_dt = data_inicio_dt + datetime.timedelta(days=1)
                data_inicio_dt = data_inicio_dt.replace(hour=7,minute=0,second=0)
                continue
            if data_inicio_dt.date() in feriados: # pular um dia se for feriado
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
        return tempo_segundos

    dataset['Tempo_Previsto_SLA_TS_Segundos'] = 0
    for x in range(len(dataset.index)):
        dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial(dataset.loc[x,'Data_Hora_Abertura'],dataset.loc[x,'Tempo_Solução'])



teste = """


SELECT 
		t.id,
		e.name AS Entidade,
		t.date DATA, 
		i.name Categoria, 
		u1.name Usuario, 
		IFNULL(u2.name,"") Tecnico,
		t.date Data_Hora_Abertura, 
		IFNULL(t.takeintoaccountdate,"") Data_Hora_Atendimento,
		IFNULL(t.begin_waiting_date,"") Data_Hora_Inicio_Espera,
		IFNULL(t.closedate,"") Data_Hora_Fechamento,
		CASE
				WHEN t.status = 6 THEN "FECHADO"
				WHEN t.status = 4 THEN "PENDENTE"
				WHEN t.status = 5 THEN "SOLUCIONADO"	
				WHEN t.status = 2 THEN "EM ATENDIMENTO"		
				WHEN t.status = 1 THEN "NOVO"	
				ELSE t.status
		END STATUS,
		ta.name TA,
		ts.name TS,
		t.time_to_own Tempo_Atendimento,
		t.time_to_resolve Tempo_Solução,
		t.takeintoaccount_delay_stat Tempo_Atendimento_Segundos,
		concat(HOUR(SEC_TO_TIME(t.takeintoaccount_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.takeintoaccount_delay_stat)),2,0)) Tempo_Atendimento_Horas,
		t.solve_delay_stat Tempo_Solução_Segundos,
		concat(HOUR(SEC_TO_TIME(t.solve_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.solve_delay_stat)),2,0)) Tempo_Solução_Horas,
		t.close_delay_stat Tempo_Fechamento_Segundos,
		concat(HOUR(SEC_TO_TIME(t.close_delay_stat)),":",LPAD(MINUTE(SEC_TO_TIME(t.close_delay_stat)),2,0)) Tempo_Fechamento_Horas,
		t.waiting_duration Tempo_Pendente_Segundos,
		concat(HOUR(SEC_TO_TIME(t.waiting_duration)),":",LPAD(MINUTE(SEC_TO_TIME(t.waiting_duration)),2,0)) Tempo_Pendente_Horas
FROM glpi_tickets t
left JOIN glpi_entities e ON e.id=t.entities_id
left JOIN glpi_locations l ON l.id=t.locations_id
left JOIN glpi_tickets_users tu2 ON tu2.tickets_id=t.id AND tu2.type = 2 -- para tecnico
left JOIN glpi_users u2 ON u2.id=tu2.users_id -- para tecnico
left JOIN glpi_tickets_users tu1 ON tu1.tickets_id=t.id AND tu1.type = 1 -- para usuário atribuido
left JOIN glpi_users u1 ON u1.id=tu1.users_id -- para usuário
left JOIN glpi_itilcategories i ON i.id=t.itilcategories_id
left JOIN glpi_slas ta ON ta.id=t.slas_id_tto -- tempo para atendimento
left JOIN glpi_slas ts ON ts.id=t.slas_id_ttr -- tempo para solução
WHERE t.is_deleted = 0  -- AND t.date_creation > '2023-06-01'  AND t.date_creation < '2023-07-01'   -- AND t.id = 42
GROUP BY t.id 



"""


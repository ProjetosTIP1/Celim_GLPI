# 'dataset' tem os dados de entrada para este script

import pandas as pd
import os
import MySQLdb
import matplotlib
import datetime
from datetime import timedelta

def pegarFeriados():
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
    for x in range(total_feriados):
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
    return feriados

# def tempoComercial(data_inicio_str,data_fim_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
def tempoComercial(data_inicio_str,data_fim_str,feriados):

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

feriados = pegarFeriados()
x = 0
dataset['Tempo_Previsto_SLA_TS_Segundos'] = '0'
total = len(dataset.index)
for x in range(total):
    # # data_abertura = dataset.loc[x,'Data_Hora_Abertura']
# data_abertura = datetime.datetime.strptime(dataset.loc[x, 'Data_Hora_Abertura'], '%Y-%m-%d %H:%M:%S')
    data_abertura = dataset.loc[x, 'Data_Hora_Abertura']
    data_abertura = datetime.datetime.strptime(data_abertura,'%d/%m/%Y %H:%M:%S')
    data_abertura = data_abertura.strftime('%d-%m-%Y %H:%M:%S')

    data_solucao = dataset.loc[x, 'Tempo_Solução']
    data_solucao = datetime.datetime.strptime(data_solucao,'%d/%m/%Y %H:%M:%S')
    data_solucao = data_solucao.strftime('%d-%m-%Y %H:%M:%S')

    tempo_previsto = tempoComercial(data_abertura,data_solucao,feriados)
    dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempo_previsto

    # dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = data_abertura
# .strftime("%d/%m/%Y %H:%M:%S")
    # # data_solucao = dataset.loc[x,'Tempo_Solução']
    # data_solucao = datetime.datetime.strptime(dataset.loc[x, 'Tempo_Solução'], '%Y-%m-%d %H:%M:%S')
    # data_solucao = data_abertura.strftime("%d-%m-%Y %H:%M:%S")
    # tempo_previsto = tempoComercial(data_abertura,data_solucao)
    # dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempo_previsto





# import datetime

# total = len(dataset.index)
# for x in range(total):
#     data_abertura = datetime.datetime.strptime(dataset.loc[x, 'Data_Hora_Abertura'], '%d-%m-%Y %H:%M:%S')
#     data_solucao = datetime.datetime.strptime(dataset.loc[x, 'Tempo_Solução'], '%d-%m-%Y %H:%M:%S')
#     tempo_previsto = tempoComercial(data_abertura, data_solucao)
#     dataset.loc[x, 'Tempo_Previsto_SLA_TS_Segundos'] = tempo_previsto


#     dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial(dataset.loc[x,'Data_Hora_Abertura'],dataset.loc[x,'Tempo_Solução'])

    # dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial('12-10-2023 07:00:00','13-10-2023 08:00:00')
    # dataset.loc[x,'Tempo_Previsto_SLA_TS_Segundos'] = 10
# dataset.loc[2,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial('01-10-2023 07:00:00')

# dataset.loc[3,'Tempo_Previsto_SLA_TS_Segundos'] = tempoComercial(dataset.loc[3,'Data_Hora_Abertura'],dataset.loc[3,'Tempo_Solução'])








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
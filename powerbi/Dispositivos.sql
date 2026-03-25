
SELECT 
		c.ID,
		e.name ENTIDADE, 
		l.name LOCALIZACAO,
		u.name USUARIO,
		c.name NOME,  
		ct.name AS DISPOSITIVO,
		CASE WHEN c.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA,
		cm.name MODELO, 
		os.name SISTEMA,
		c.serial SERIAL, 
		c.otherserial INVENTARIO,
		DATE_FORMAT(c.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		c.contact ACESSO, 
		c.comment OBSERVACAO
FROM glpi_computers c
LEFT JOIN glpi_entities e ON e.id = c.entities_id
LEFT JOIN glpi_users u ON u.id = c.users_id
LEFT JOIN glpi_locations l ON l.id = c.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = c.manufacturers_id
LEFT JOIN glpi_computertypes ct ON ct.id = c.computertypes_id
LEFT JOIN glpi_computermodels cm ON cm.id = c.computermodels_id
LEFT JOIN glpi_items_operatingsystems ios ON ios.items_id = c.id
LEFT JOIN glpi_operatingsystems os ON os.id = ios.operatingsystems_id
WHERE c.is_deleted = 0  

UNION ALL

SELECT 
		mo.ID, 
		e.name ENTIDADE, 
		l.name LOCALIZACAO, 
		u.name USUARIO, 
		mo.name NOME, 
		'Monitor' AS DISPOSITIVO,
		CASE WHEN mo.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA, 
		mm.name MODELO, 
		'' SISTEMA, 
		mo.serial SERIAL, 
		mo.otherserial INVENTARIO, 
		DATE_FORMAT(mo.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		mo.contact ACESSO, 
		mo.comment OBSERVACAO
FROM glpi_monitors mo
LEFT JOIN glpi_entities e ON e.id = mo.entities_id
LEFT JOIN glpi_users u ON u.id = mo.users_id
LEFT JOIN glpi_locations l ON l.id = mo.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = mo.manufacturers_id
LEFT JOIN glpi_monitormodels mm ON mm.id = mo.monitormodels_id
WHERE mo.is_deleted = 0  

UNION ALL

SELECT 
		p.ID, 
		e.name ENTIDADE, 
		l.name LOCALIZACAO, 
		u.name USUARIO, 
		p.name NOME, 
		'Impressora' AS DISPOSITIVO,
		CASE WHEN p.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA, 
		pm.name MODELO, 
		'' SISTEMA, 
		p.serial SERIAL, 
		p.otherserial INVENTARIO, 
		DATE_FORMAT(p.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		p.contact ACESSO, 
		p.comment OBSERVACAO
FROM glpi_printers p
LEFT JOIN glpi_entities e ON e.id = p.entities_id
LEFT JOIN glpi_users u ON u.id = p.users_id
LEFT JOIN glpi_locations l ON l.id = p.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = p.manufacturers_id
LEFT JOIN glpi_printermodels pm ON pm.id = p.printermodels_id
WHERE p.is_deleted = 0 

UNION ALL

SELECT 
		n.ID, 
		e.name ENTIDADE, 
		l.name LOCALIZACAO, 
		u.name USUARIO, 
		n.name NOME, 
		'Roteador' AS DISPOSITIVO,
		CASE WHEN n.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA, 
		nm.name MODELO, 
		'' SISTEMA, 
		n.serial SERIAL, 
		n.otherserial INVENTARIO, 
		DATE_FORMAT(n.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		n.contact ACESSO, 
		n.comment OBSERVACAO
FROM glpi_networkequipments n
LEFT JOIN glpi_entities e ON e.id = n.entities_id
LEFT JOIN glpi_users u ON u.id = n.users_id
LEFT JOIN glpi_locations l ON l.id = n.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = n.manufacturers_id
LEFT JOIN glpi_networkequipmentmodels nm ON nm.id = n.networkequipmentmodels_id
WHERE n.is_deleted = 0 

UNION ALL

SELECT 
		p.ID, 
		e.name ENTIDADE, 
		l.name LOCALIZACAO, 
		u.name USUARIO, 
		p.name NOME, 
		'Telefone' AS DISPOSITIVO,
		CASE WHEN p.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA, 
		pm.name MODELO, 
		'' SISTEMA, 
		p.serial SERIAL, 
		p.otherserial INVENTARIO, 
		DATE_FORMAT(p.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		p.contact ACESSO, 
		p.comment OBSERVACAO
FROM glpi_phones p
LEFT JOIN glpi_entities e ON e.id = p.entities_id
LEFT JOIN glpi_users u ON u.id = p.users_id
LEFT JOIN glpi_locations l ON l.id = p.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = p.manufacturers_id
LEFT JOIN glpi_phonemodels pm ON pm.id = p.phonemodels_id
WHERE p.is_deleted = 0 

UNION ALL

SELECT 
		p.ID, 
		e.name ENTIDADE, 
		l.name LOCALIZACAO, 
		u.name USUARIO, 
		p.name NOME, 
		'Dispositivos' AS DISPOSITIVO,
		CASE WHEN p.states_id = 1 THEN 'ATIVO' ELSE 'INATIVO' END STATUS_EQUIP,
		m.name MARCA, 
		pm.name MODELO, 
		'' SISTEMA, 
		p.serial SERIAL, 
		p.otherserial INVENTARIO, 
		DATE_FORMAT(p.date_mod, '%d/%m/%Y') AS ULTIMA_ATUALIZACAO,
		p.contact ACESSO, 
		p.comment OBSERVACAO
FROM glpi_peripherals p
LEFT JOIN glpi_entities e ON e.id = p.entities_id
LEFT JOIN glpi_users u ON u.id = p.users_id
LEFT JOIN glpi_locations l ON l.id = p.locations_id
LEFT JOIN glpi_manufacturers m ON m.id = p.manufacturers_id
LEFT JOIN glpi_peripheralmodels pm ON pm.id = p.peripheralmodels_id
WHERE p.is_deleted = 0 
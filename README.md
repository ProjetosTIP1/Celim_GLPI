# Celim_GLPI - Automação de Chamados (RPA)

Este projeto é um sistema de Automação de Processos Robóticos (RPA) desenvolvido para monitorar e gerenciar chamados no **GLPI** (Gestão de Ativos de TI e Service Desk). O robô automatiza o acompanhamento de tickets, calcula prazos de SLA e envia notificações em tempo real via Telegram.

## 🚀 Funcionalidades Principais

- **Monitoramento de Novos Chamados**: Identifica automaticamente tickets recém-abertos e notifica a equipe.
- **Alertas de Vencimento**: Monitora chamados próximos ao vencimento (SLA de atendimento ou solução) e envia alertas preventivos.
- **Cálculo de Tempo Comercial**: Possui lógica avançada para desconsiderar finais de semana, feriados e horários fora do expediente comercial no cálculo de prazos.
- **Integração com Telegram**: Notificações ricas com detalhes do chamado (Solicitante, Entidade, Categoria, Título e Link direto).
- **Persistência e Log**: Mantém o estado dos avisos em um banco de dados MariaDB/MySQL para evitar notificações redundantes.
- **Modo de Operação**: Suporta modo de teste (silencioso) e produção.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Automação Web**: Selenium (Headless Chrome)
- **Manipulação de Dados**: Pandas
- **Interface com Banco de Dados**: SQLAlchemy (com pool de conexões)
- **Notificações**: PyTelegramBotAPI (telebot)
- **Interface Desktop**: PyAutoGUI
- **Banco de Dados**: MariaDB / MySQL

## 📂 Estrutura do Projeto

```text
├── Celim_GLPI.py           # Script principal com a lógica do robô
├── database_adapter.py     # Adaptador moderno para conexão com banco de dados
├── settings.py             # Gerenciamento de configurações e variáveis de ambiente
├── Config/                 # Arquivos de configuração legados (.txt)
├── utils/                  # Utilitários diversos (ex: renderização de tabelas)
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
```

## ⚙️ Configuração

### 1. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
CHAVE=sua_chave_de_criptografia
HORA_TERMINO=17:00
CAMINHO_EXCEL=C:\Caminho\Para\Excel.exe
EXTERNAL_LIBS_PATH=./01_lib
```

### 2. Arquivos de Configuração (Pasta Config/)
O robô lê parâmetros de arquivos de texto simples para compatibilidade legada:
- `sistema.txt`: Identificador do sistema.
- `horatermino.txt`: Horário de encerramento diário.
- `caminho_excel.txt`: Caminho para o executável do Excel (utilizado em módulos específicos).

### 3. Banco de Dados
O sistema utiliza duas bases de dados principais configuradas via banco:
- **Base RPA**: Armazena parâmetros globais e o log de avisos (`tb015_glpi`).
- **Base GLPI**: Fonte dos dados dos chamados.

## 🚀 Execução

### Modo Desenvolvimento
Para rodar o robô diretamente:
```bash
python Celim_GLPI.py
```

### Gerar Executável (Produção)
O projeto utiliza o `PyInstaller` para compilação. Para gerar o executável:

```bash
pyinstaller --onefile --noconsole Celim_GLPI.py
```
*Nota: Certifique-se de que o `chromedriver.exe` e a pasta `Config/` estejam no mesmo diretório do executável gerado.*

## 📝 Notas de Manutenção

- **Log Operacional**: O robô gera logs detalhados na pasta `log/` e no banco de dados.
- **SLA**: A lógica de tempo comercial deve ser revisada se houver mudanças nos calendários de feriados na tabela `glpi_holidays`.
- **Headless**: Por padrão, o Selenium roda em modo `--headless`, o que significa que o navegador não será visível durante a operação.

---
*Este é um projeto que combina lógica legada com melhorias modernas de arquitetura.*

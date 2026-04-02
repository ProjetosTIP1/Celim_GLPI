# Celim_GLPI - Automação de Chamados (RPA)

Este projeto é um sistema de Automação de Processos Robóticos (RPA) desenvolvido para monitorar e gerenciar chamados no **GLPI**. O robô automatiza o acompanhamento de tickets, calcula prazos de SLA e envia notificações em tempo real via Telegram.

## 🚀 Funcionalidades Principais

- **Monitoramento de Novos Chamados**: Identifica tickets recém-abertos e notifica a equipe.
- **Alertas de Vencimento**: Monitora chamados próximos ao vencimento (SLA de atendimento ou solução) e envia alertas (80%+ de progresso).
- **Cálculo de Tempo Comercial**: Lógica para desconsiderar finais de semana e feriados no cálculo de prazos.
- **Integração com Telegram**: Notificações ricas com detalhes do chamado e links diretos.
- **Resolução Estável**: Configurado para rodar sempre em 1920x1080 (mesmo em modo Headless) para garantir a integridade dos seletores WEB.

## 🛠️ Tecnologias e Requisitos

- **Linguagem**: Python 3.11+
- **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv) (Recomendado para performance e estabilidade)
- **Automação Web**: Selenium (Chrome / Headless Support)
- **Banco de Dados**: MariaDB / MySQL (SQLAlchemy)

## 📂 Estrutura de Implantação (Deploy)

Para um funcionamento "limpo" em produção, o robô deve seguir a seguinte estrutura de diretórios no servidor/máquina de execução:

```text
C:\Projetos\RPA\             <-- Diretório Raiz de RPAs
├── 01_lib\                  <-- Biblioteca de funções compartilhadas (Legado)
└── Celim_GLPI\              <-- Pasta deste Projeto
    ├── Celim_GLPI.exe       <-- Executável gerado
    ├── .env                 <-- Configurações de ambiente
    ├── Config\              <-- Parâmetros (.txt)
    ├── log\                 <-- Logs operacionais
    └── chromedriver-win64\  <-- Driver do Chrome (Versão compatível)
```

## ⚙️ Configuração (.env)

Crie um arquivo `.env` na pasta do executável:

```env
CHAVE=sua_chave_de_criptografia
HORA_TERMINO=17:00
EXTERNAL_LIBS_PATH=../01_lib
```

## 📦 Como Gerar o Executável (.exe)

O projeto utiliza o `PyInstaller`. Recomenda-se gerar o executável em modo Console para facilitar o debug inicial em produção.

1.  **Instale as dependências**:
    ```bash
    uv sync
    ```
2.  **Gere o executável**:
    ```bash
    pyinstaller --onefile --icon=NONE Celim_GLPI.py
    ```

### Checklist para o Executável rodar "Clean":
1.  **Versão do Chrome**: Verifique se o `chromedriver.exe` dentro de `chromedriver-win64/` é compatível com a versão do Chrome instalada no Windows.
2.  **Pasta 01_lib**: Certifique-se de que a biblioteca compartilhada está na pasta **pai** (`../01_lib`).
3.  **Ambiente**: O arquivo `.env` deve estar presente para carregar a `CHAVE` e o `EXTERNAL_LIBS_PATH`.
4.  **SQL**: O RPA requer acesso às tabelas `tb015_glpi` e `glpi_tickets` nos bancos configurados.

---
*Manutenção: O bot detecta automaticamente se está rodando como script ou executável para ajustar os caminhos base.*

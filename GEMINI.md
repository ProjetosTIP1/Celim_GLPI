# Celim_GLPI - RPA Project

## Project Overview
`Celim_GLPI` is a Robotic Process Automation (RPA) system designed to automate interactions with GLPI (IT Asset Management and Service Desk). The automation monitors tickets, manages task execution, logs activities in a database, and provides real-time notifications via Telegram.

### Main Technologies
- **Python**: Core programming language.
- **Selenium**: Web automation for GLPI interactions.
- **Pandas**: Data manipulation and state management.
- **PyTelegramBotAPI (telebot)**: Integration for Telegram notifications.
- **PyAutoGUI**: Desktop GUI automation.
- **MariaDB/MySQL**: Database persistence for logs and task status.
- **PyInstaller**: Used for packaging the script into an executable.

## Architecture
The project follows a modular architecture, relying on a set of shared libraries for core functionalities:

- **Main Script (`Celim_GLPI.py`)**: Contains the `GLPI` class which encapsulates the main automation logic, including ticket monitoring, time management (`relogio_timer`), and error handling.
- **Shared Libraries (`01_lib`)**: The project imports several modules from a centralized directory (defined in `Config/Diretorios/RaizProjeto.txt`):
    - `ConectarBd`: Handles database connections.
    - `Gerarlog`: Manages process logging.
    - `GerenciadorTarefas`: Orchestrates the execution of different automation tasks.
    - `GerenciadorJanelas`: Manages browser windows and desktop focus.
    - `GerarVar` & `GerarChave`: Handles parameter loading and encryption/decryption of sensitive data.
- **Configuration (`Config/`)**: Environment-specific settings are stored in plain text files within the `Config` directory, allowing for easy adjustment of paths, timing, and database parameters without code changes.

## Building and Running

### Prerequisites
1.  **Python Environment**: Python 3.x installed.
2.  **Dependencies**: Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  **ChromeDriver**: Ensure a `chromedriver.exe` matching your Chrome version is present in the root directory (versions 116 and 119 are provided).
4.  **Database**: Access to the MariaDB/MySQL server specified in the parameters.

### Execution
To run the automation directly:
```bash
python Celim_GLPI.py
```

### Build (Executable)
The project includes `pyinstaller` in `requirements.txt`, suggesting it can be compiled for production environments:
```bash
pyinstaller --onefile Celim_GLPI.py
```
*(Note: Additional hooks or assets might be required for a successful build depending on the internal library structure.)*

## Development Conventions

- **Environment Paths**: Always check `Config/Diretorios/` if the project fails to load libraries or local data.
- **Logging**: Use the `BotLog` instance for all operational logging to ensure consistency across the RPA ecosystem.
- **Encryption**: Sensitive data (like database passwords) are typically encrypted and require a `Chave.txt` (referenced in the code) to be decrypted at runtime.
- **Persistence**: The bot checks `tb015_glpi` in the database to maintain state (e.g., which tickets have already been notified).

## Key Files
- `Celim_GLPI.py`: Main automation entry point and class definition.
- `requirements.txt`: List of Python dependencies.
- `Config/`: Configuration directory containing:
    - `sistema.txt`: System identifier.
    - `horatermino.txt`: Daily termination time for the bot.
    - `Diretorios/`: Local and library path definitions.
- `chromedriver*.exe`: Web drivers for Selenium.

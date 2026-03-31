import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .web_driver_manager import WebDriverFactory


class GLPIScraper:
    """
    Dedicated service for scraping GLPI ticket data from the web interface.
    """

    def __init__(self, bot_log, headless: bool = True):
        self.bot_log = bot_log
        self.driver: Optional[webdriver.Chrome] = None
        self.headless = headless
        self.limite_aguardar_elemento = 60

    def start(self):
        """Initializes the WebDriver instance."""
        self.driver = WebDriverFactory.create_chrome_driver(headless=self.headless)
        self.bot_log.imprimirLog("Navegador iniciado via GLPIScraper")

    def _esperar_elemento(self, xpath: str) -> bool:
        """Internal helper to wait for an element to appear."""
        if not self.driver:
            return False
        tentativas = 0
        while tentativas < self.limite_aguardar_elemento:
            try:
                self.driver.find_element(By.XPATH, xpath)
                return True
            except Exception:
                time.sleep(1)
                tentativas += 1
        return False

    def login(self, url: str, username: str, password: str):
        """Performs login on the GLPI portal."""
        if not self.driver:
            self.start()

        if not self.driver:
            return

        self.bot_log.imprimirLog(f"Abrindo GLPI: {url}")
        self.driver.get(url)

        # Username
        xpath_user = '//*[@id="login_name"]'
        if self._esperar_elemento(xpath_user):
            self.driver.find_element(By.XPATH, xpath_user).send_keys(username)

        # Password
        xpath_pass = "/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[3]/input"
        if self._esperar_elemento(xpath_pass):
            self.driver.find_element(By.XPATH, xpath_pass).send_keys(password)

        # Sign In
        xpath_btn = "/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button"
        if self._esperar_elemento(xpath_btn):
            btn = self.driver.find_element(By.XPATH, xpath_btn)
            self.driver.execute_script("arguments[0].click();", btn)
            self.bot_log.imprimirLog("Login submetido")
            time.sleep(2)

    def navigate_to_tickets(self):
        """Navigates to the ticket list and prepares the view."""
        if not self.driver:
            return

        # Assistência
        xpath_assist = "/html/body/div[2]/aside/div/div[2]/ul/li[2]/a/span"
        if self._esperar_elemento(xpath_assist):
            self.driver.find_element(By.XPATH, xpath_assist).click()

        # Chamados
        xpath_tickets = (
            "/html/body/div[2]/aside/div/div[2]/ul/li[2]/div/div/div[1]/a[2]/span"
        )
        if self._esperar_elemento(xpath_tickets):
            btn = self.driver.find_element(By.XPATH, xpath_tickets)
            self.driver.execute_script("arguments[0].click();", btn)
            self.bot_log.imprimirLog("Navegado para a tela de chamados")
            time.sleep(2)

        # Configure View: Show 10000 entries
        xpath_select = "/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[3]/div/span[1]/select"
        if self._esperar_elemento(xpath_select):
            select = Select(self.driver.find_element(By.XPATH, xpath_select))
            select.select_by_value("10000")
            self.bot_log.imprimirLog("Configurado para exibir 10000 chamados")
            time.sleep(2)

        # Clear filters
        xpath_clear = (
            "/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[2]/a[2]/i"
        )
        if self._esperar_elemento(xpath_clear):
            self.driver.find_element(By.XPATH, xpath_clear).click()
            self.bot_log.imprimirLog("Filtros limpos")
            time.sleep(2)

    def scrape_vencimentos(self):
        """Scrapes ticket progress data from the table."""
        if not self.driver:
            return []

        # Check if rows exist
        xpath_rows_info = (
            "/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[3]/div/p[1]"
        )
        try:
            total_text = self.driver.find_element(
                By.XPATH, xpath_rows_info
            ).get_attribute("innerHTML")
            if not total_text:
                return []
            x, y = total_text.find("de"), total_text.find("linhas")
            quant_chamados = int(total_text[x + 3 : y - 1])
        except Exception:
            self.bot_log.imprimirLog("Sem chamados visíveis")
            return []

        # Map TA and TS columns dynamically
        col_ta, col_ts = 0, 0
        for i in range(1, 20):
            try:
                header = self.driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/thead/tr/th[{i}]",
                ).get_attribute("innerHTML")
                if not header:
                    continue
                if "Tempo para atendimento" in header:
                    col_ta = i
                if "Tempo para solução" in header:
                    col_ts = i
            except Exception:
                break
            if col_ta and col_ts:
                break

        results = []
        for row in range(1, quant_chamados + 1):
            try:
                num = self.driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{row}]/td[2]/span",
                ).get_attribute("innerHTML")
                status_icon = self.driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{row}]/td[5]/span/i",
                )
                status = status_icon.get_attribute("data-bs-original-title")

                if status == "Pendente":
                    continue

                prog_ta = 0
                if status == "Novo" and col_ta:
                    prog_ta_val = self.driver.find_element(
                        By.XPATH,
                        f"/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{row}]/td[{col_ta}]/div/div",
                    ).get_attribute("aria-valuenow")
                    prog_ta = int(prog_ta_val) if prog_ta_val else 0

                prog_ts = 0
                if col_ts:
                    try:
                        prog_ts_val = self.driver.find_element(
                            By.XPATH,
                            f"/html/body/div[2]/div/div/main/div/div[2]/div[2]/form/div/div[2]/table/tbody/tr[{row}]/td[{col_ts}]/div/div",
                        ).get_attribute("aria-valuenow")
                        prog_ts = int(prog_ts_val) if prog_ts_val else 0
                    except Exception:
                        pass

                if prog_ta > 80 or prog_ts > 80:
                    results.append(
                        {
                            "Numero": int(num) if num else 0,
                            "Status": status,
                            "TA_P": prog_ta,
                            "TS_P": prog_ts,
                        }
                    )
            except Exception:
                continue

        return results

    def quit(self):
        """Closes the browser session."""
        if self.driver:
            self.driver.quit()
            self.bot_log.imprimirLog("Navegador encerrado")

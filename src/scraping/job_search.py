import os
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Exceptions
from selenium.common.exceptions import NoSuchElementException


# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.extract.job import JobDataExtractor


class JobSearchScraper:
    def __init__(self, session=".session", headless=False) -> None:
        self.session = session
        self.domain = "https://www.linkedin.com"

        self.options = Options()

        # Headless
        if headless:
            self.options.add_argument("--headless=new")
            self.options.add_argument("window-size=2160,3840")
        self.options.add_argument("window-size=1920,1080")
        # self.options.add_argument("window-size=3840,2160")

        # Session
        if not os.path.isdir(session):
            os.makedirs(session)

        self.options.add_argument(f"--user-data-dir={self.session}")
        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def autenticate(self, email=None, password=None):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.get(self.domain)

        # Verifica se já está logado
        try:
            driver.find_element(By.XPATH, "//a[contains(text(), 'Sign in')]")
        except NoSuchElementException:
            self.driver = driver
            sleep(5)
            return

        # Inserindo email
        session_key = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='session_key']"))
        )
        print("sending", session_key.get_attribute("name"))
        session_key.send_keys(email)

        # Inserindo senha
        session_password = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='session_password']")
            )
        )
        print("sending", session_password.get_attribute("name"))
        session_password.send_keys(password)
        sleep(2)

        # Aperta botão de sign in
        sign_in = driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]")
        sign_in.click()

        print("Sessão criada")
        self.driver = driver

    def search_job_ids(self, job_name: str = "Engenharia de dados", max_pages=3):
        dataset = []
        id_dataset = []

        if self.driver is None:
            print("You need to authenticate before doing search")
            return

        endpoint = self.domain + "/jobs"
        self.driver.get(endpoint)
        sleep(5)

        # Entrada dos termos de pesquisa
        search_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[starts-with(@id,'jobs-search-box-keyword-id')]")
            )
        )
        search_input.send_keys(job_name)
        sleep(1)
        search_input.send_keys(Keys.ENTER)

        # Navegação pelas páginas
        next_page = 2
        last_page = 0
        while next_page < max_pages:
            sleep(3)
            print(f"Página: {next_page - 1}")
            # Encontra os cards com as vagas
            job_cards = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "jobs-search-results__list-item")
                )
            )
            for card in job_cards:
                id_dataset.append(card.get_attribute("data-occludable-job-id"))
            # input("Continue?")

            # Iterando nos cards de jobs
            # print("cards", len(job_cards))
            # for card in job_cards:
            #     sleep(2)
            #     card.click()

            #     # =====================================
            #     # Início da captura dados sobre o job
            #     ## Url | Id
            #     sleep(2)  # Tempo para carregar a página
            #     job_url = self.driver.current_url
            #     data_extractor = JobDataExtractor(job_url)
            #     # print("ID: ", data_extractor.get_id())

            #     ## Skills

            pages_btn = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "artdeco-pagination__indicator--number")
                )
            )

            for i, page in enumerate(pages_btn):
                if page.text == str(next_page):
                    print(last_page, "-->", page.text)
                    last_page = page.text
                    page.click()
                    break

                if page.text == "…" and i > 2:
                    print("… --> mais páginas")
                    page.click()
                    next_page -= 1
                    sleep(2)
                    break
            next_page += 1

        return id_dataset

    def retrive_job_data(self, job_id):
        data_extractor = JobDataExtractor(job_id)
        if self.driver is None:
            print("You need to authenticate before retriving data")
            return

        endpoint = self.domain + "/jobs/view/" + job_id
        self.driver.get(endpoint)
        sleep(3)

        # Expandir sessão "Ver mais"
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "button[aria-label='Clicar para ver mais detalhes']",
                )
            )
        ).click()

        # ## Detalhes
        detalhes = data_extractor.details(self.driver.page_source)
        # print(detalhes)

        ## Skills
        try:
            ### Navegar | Abrir popup
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='#HYM']"))
            ).click()  # Link superior

            sleep(2)
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='#']"))
            ).click()  # Abre popup

            ### Skills
            sleep(2)  # Tempo para carregar a página
            job_skills = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "artdeco-modal-outlet"))
            )
            # job_skills = self.driver.find_element(By.ID, "artdeco-modal-outlet")
            job_skills_data = data_extractor.skills(
                job_skills.get_attribute("innerHTML")
            )

            detalhes["skills"] = job_skills_data
            # print(job_skills_data)

            ### Fecha popup
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Fechar']")
                )
            ).click()  # Fecha popup

        except Exception as e:
            print(e)
            job_data = data_extractor.save()
            print("-", job_data["id"])

        detalhes["id"] = job_id
        detalhes["url"] = endpoint

        # WebDriverWait(self.driver, 5).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.CLASS_NAME,
        #             "job-details-how-you-match__skills-item-subtitle",
        #         )
        #     )
        # ).click()

        return detalhes


if __name__ == "__main__":
    from dotenv import load_dotenv
    import pandas as pd
    from random import shuffle

    load_dotenv()

    bot = JobSearchScraper(headless=True)
    email = os.environ["LINKEDIN_EMAIL"]
    password = os.environ["LINKEDIN_PASSWORD"]
    bot.autenticate(email=email, password=password)
    # id_dataset = bot.search_job_ids(job_name="Engenharia de dados")

    id_dataset = [
        "3906678509",
        "3871159643",
        "3894277050",
        "3749314307",
        "3884248793",
        "3865842702",
        "3879398354",
        "3907132071",
        "3838683554",
        "3896037368",
    ]

    shuffle(id_dataset)
    dataset = []
    for _id in id_dataset:
        data = bot.retrive_job_data(_id)
        dataset.append(data)
        print(data["id"], data["url"])

    # print(dataset)
    df = pd.DataFrame(dataset)
    df.to_csv("jobs.csv")
    print("CSV salvo!")

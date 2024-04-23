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
        self.options.headLessess = headless
        # self.options.add_argument("--headless=new")
        # self.options.add_argument("window-size=430,2160")
        self.options.add_argument("window-size=1920,1080")

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

    def search_job(self, job_name: str = "Engenharia de dados"):
        dataset = []
        # self.options.add_argument("--headless=new")
        # self.options.add_argument(f"--user-data-dir={self.session}")
        # driver = webdriver.Chrome(service=self.service, options=self.options)

        if self.driver is None:
            print("You need to authenticate before doing search")
            return

        endpoint = self.domain + "/jobs"
        self.driver.get(endpoint)

        # Entrada dos termos de pesquisa
        search_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[starts-with(@id,'jobs-search-box-keyword-id')]")
            )
        )
        search_input.send_keys(job_name)
        sleep(1)
        search_input.send_keys(Keys.ENTER)
        sleep(4)

        # Navegação pelas páginas
        max_pages = 10
        next_page = 2
        while next_page < max_pages:
            job_cards = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "jobs-search-results__list-item")
                )
            )

            # Iterando nos cards de jobs
            # print("cards", len(job_cards))
            for card in job_cards[:1]:
                sleep(2)
                card.click()
                # print(f"card [{i}]...")

                # =====================================
                # Início da captura dados sobre o job
                ## Url | Id
                sleep(2)  # Tempo para carregar a página
                job_url = self.driver.current_url
                data_extractor = JobDataExtractor(job_url)
                # print("ID: ", data_extractor.get_id())

                ## Detalhes

                job_details = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jobs-search__job-details")
                    )
                )
                job_details_data = data_extractor.add_details(
                    job_details.get_attribute("innerHTML")
                )
                # print(job_details_data)

                ## Skills
                ### Navegar | Abrir popup
                sleep(2)
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='#HYM']"))
                ).click()  # Link superior

                # input("stop: ")
                sleep(2)
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='#']"))
                ).click()  # Abre popup

                # WebDriverWait(self.driver, 3).until(
                #     EC.presence_of_element_located(
                #         (
                #             By.XPATH,
                #             "//span[contains(text(), 'Exibir todas as competências')]",
                #         )
                #     )
                # ).parent.click()  # Abre popup

                ### Skills
                sleep(2)  # Tempo para carregar a página
                job_skills = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "artdeco-modal-outlet"))
                )
                # job_skills = self.driver.find_element(By.ID, "artdeco-modal-outlet")
                job_skills_data = data_extractor.add_skills(
                    job_skills.get_attribute("innerHTML")
                )
                # print(job_skills_data)

                ### Fecha popup
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@aria-label='Fechar']")
                    )
                ).click()  # Fecha popup

                dataset.append(data_extractor.save())

            pages_btn = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "artdeco-pagination__indicator--number")
                )
            )

            # print("pages len:", len(pages_btn))
            for page in pages_btn:
                if page.text == str(next_page) or page.text == "...":
                    page.click()
                    break
            next_page += 1

        return dataset


if __name__ == "__main__":
    from dotenv import load_dotenv
    import pandas as pd

    load_dotenv()

    bot = JobSearchScraper()
    email = os.environ["LINKEDIN_EMAIL"]
    password = os.environ["LINKEDIN_PASSWORD"]
    bot.autenticate(email=email, password=password)
    dataset = bot.search_job(job_name="Engenharia de dados")

    # print(dataset)
    df = pd.DataFrame(dataset)
    df.to_csv("jobs.csv")
    print("CSV salvo!")

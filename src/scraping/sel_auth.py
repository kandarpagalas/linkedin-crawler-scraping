from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Inicia o navegador Chrome driver
options = Options()

# Headless
options.headLessess = False
# options.add_argument("--headless=new")

# Modo anônimo
# options.add_argument("--incognito")

#Session
options.add_argument(r"--user-data-dir=.session")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

endpoint = "https://www.linkedin.com/"
driver.get(endpoint)

input("???")
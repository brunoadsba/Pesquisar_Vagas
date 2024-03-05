from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from openpyxl import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Imprimir mensagem de início
print("Vamos lá!")

# Definir a busca para "estágio"
search = "estágio"

# FUNÇÃO - BUSCAR CREDENCIAIS
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split(":")
            credentials[key] = value
        return credentials
    
# Caminho do arquivo de credenciais
file_path_credentials = "credentials.txt"
# Ler as credenciais do arquivo
credentials = read_credentials(file_path_credentials)

# Iniciar o navegador
browser = webdriver.Chrome()  # Use o navegador desejado (ex: Chrome, Firefox)
browser.maximize_window()
browser.get("https://www.linkedin.com/jobs")
sleep(2)

# Preencher e enviar informações de login
email = browser.find_element(By.XPATH, "//input[@id='session_key']")
password = browser.find_element(By.XPATH, "//input[@id='session_password']")
btn_enter = browser.find_element(By.XPATH, "//button[normalize-space(text())='Entrar']")
sleep(2)

email.send_keys(credentials['user'])
password.send_keys(credentials['password'])
btn_enter.click()
sleep(5)

# Pesquisar vagas
input_jobs_search = browser.find_element(By.XPATH,'//header//input')
sleep(3)
input_jobs_search.send_keys(search)
sleep(3)
input_jobs_search.send_keys(Keys.ENTER)
sleep(5)

# Rolagem para carregar mais resultados
for _ in range(25):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

# Capturar elementos da lista de resultados
wait = WebDriverWait(browser, 10)
ul_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "main div.jobs-search-results-list")))

# Capturar informações das vagas
jobs = ul_element.find_elements(By.CSS_SELECTOR, "ul>li")

# Criar uma planilha para armazenar os resultados
wb = Workbook()
ws = wb.active
ws.append(['Empresa', 'Cargo', 'Localização', 'Data de Publicação', 'Link da Vaga'])

# Escrever as informações das vagas na planilha
for job in jobs:
    try:
        # Verificar se o título da vaga existe antes de tentar acessá-lo
        job_title_element = job.find_element(By.CSS_SELECTOR, "h3")
        job_title = job_title_element.text
    except NoSuchElementException:
        job_title = "Título não encontrado"
    
    try:
        # Verificar se o link da vaga existe antes de tentar acessá-lo
        job_link_element = job.find_element(By.CSS_SELECTOR, "a")
        job_link = job_link_element.get_attribute('href')
    except NoSuchElementException:
        job_link = "Link não encontrado"
    
    try:
        # Capturar informações adicionais da vaga
        job_info_element = job.find_element(By.CSS_SELECTOR, "div.job-card-container__metadata-wrapper")
        job_info = job_info_element.text.split("\n")
        company = job_info[0]
        location = job_info[1]
        posted_date = job_info[2]
    except NoSuchElementException:
        company = "Informação não disponível"
        location = "Informação não disponível"
        posted_date = "Informação não disponível"

    ws.append([company, job_title, location, posted_date, job_link])

# Salvar a planilha no diretório especificado

from datetime import datetime

# Obter a data e hora atual para criar um nome de arquivo único
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Nome do arquivo com a data e hora atual
file_name = f"vagas_linkedin_{current_datetime}.xlsx"
# Caminho completo do arquivo
file_path = f"C:\\Users\\danyp\\Downloads\\Bruno\\{file_name}"

# Salvar a planilha com o nome de arquivo único

wb.save(file_path)
print("Planilha criada")
print("Encerrando a busca")
sleep(1)
browser.quit()

# WEB MINING & CRAWLER SCRAPING

#### Clonando e instalando requisitos
```bash
# Clone o repositório
git clone https://github.com/kandarpagalas/trabalho_final_web_mining_crawler_scraping.git

# Navegue até a pasta
cd trabalho_final_web_mining_crawler_scraping

# Inicie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate
```
#### Pacotes/bibliotecas utilizadas
##### requirements.txt
```text
jupyterlab
selenium
webdriver_manager
beautifulsoup4
sqlalchemy
python-dotenv
pandas
nltk
setuptools
wheel
spacy
scikit-learn
```
##### Instale as dependências
```
pip install -r requirements.txt
```


## Crawler | scraping

#### Executando
1. adicione suas credenciais em ```template.env``` e renomei para ```.env```
2. Execute o crawler passando como argumento a ```área de interesse``` para busca
```bash
python src/crawler.py "Engenharia de dados" [options]
```
##### Opções (não é necessário usar):
* ```--headless``` Modo headless.
* ```--max_pages=20``` Limite de páginas visitadas.
* ```--output="./data/jobs.csv"``` Arquivo de output.
* ```--session="./.session/"``` Pasta com arquivos da sessão.

##### Obs.: Corrigir Exception ```ModuleNotFoundError: No module named 'src'```
```bash
# Execute esse código na pasta raiz do projeto (com o venv ativado)
export PYTHONPATH="$PYTHONPATH:$PWD"
```

#### Output do crawler / Scraping
Arquivo ```data/jobs.csv``` contendo informações sobre as vagas coletadas


## Recuperação de informação
As análises podem ser verificadas no notebook ```recuperacao_de_informacao.ipynb```

#### Analise de similaridade 
Utilisa o algorítimo de Similaridade TF-IDF para a comparar o conteúdo da sessão SOBRE de um perfil do linkedin e as descrições das vagas em aberto. 
Retornando um DataFrame com as vagas ordenadas de forma decrescente pela similaridade.

#### Contador de palavras
Implementa um contador de palavras para ordenar, de acordo com a contagem, as skills que mais apareceram nas vagas em aberto.
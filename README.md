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

# Instale as dependências
pip install -r requirements
```

## Crawler | scraping

#### Executando
1. adicione suas credenciais em ```template.env``` e renomei para ```.env```
2. Execute o crawler passando como argumento a ```área de interesse``` para busca
```bash
python src/crawler.py "Engenharia de dados" [options]
```
Opções:
```--headless``` para rodar em modo headless
```--max_pages=20``` Limite de páginas visitadas durante a busca. Padrão ```20```
```--output="caminho/para/o/arquivo.csv"``` Para modificar onde o arquivo de output deve ser salvo. Padrão ```./data/jobs.csv```
```--session="caminho/para/a/pasta/"``` Para definir onde fica a pasta da sessão. Padrão ```./.session/```

#### Output do crawler / Scraping
- Arquivo ```data/jobs.csv``` contendo informações sobre as vagas coletadas


```bash
```


## Mecanismo de busca
```bash
```
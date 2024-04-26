import os
import argparse
from dotenv import load_dotenv
import pandas as pd

from src.scraping.job_search import JobSearchScraper


load_dotenv()


def find_jobs(
    subject,
    headless=True,
    max_pages=1,
    csv_output="data/jobs.csv",
    session_folder=".session",
):

    email = os.environ["LINKEDIN_EMAIL"]
    password = os.environ["LINKEDIN_PASSWORD"]

    bot = JobSearchScraper(session=session_folder, headless=headless)
    bot.autenticate(email=email, password=password)
    id_dataset = bot.search_job_ids(job_name=subject, max_pages=max_pages)

    print("Start retrieving jobs data")
    total = len(id_dataset)
    dataset = []

    for i, _id in enumerate(id_dataset):
        try:
            data = bot.retrive_job_data(_id)
            dataset.append(data)
            url = data["url"]
            log_str = f"{i}/{total} OK {url}"
            print(log_str)
        except Exception:
            log_str = f"{i}/{total} OK {_id}"
            print(log_str)

    df = pd.DataFrame(dataset)
    df.to_csv(csv_output)
    print(f"CSV disponível em: {csv_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Executar um crawler que coleta dados sobre vagas no linkedin"
    )
    parser.add_argument(
        "subject",
        # required=False,
        help="Termo que deve ser pesquisado",
    )
    # --headless
    parser.add_argument(
        "--headless",
        required=False,
        nargs="?",
        const=True,
        type=bool,
        default=False,
        help="Termo que deve ser pesquisado",
    )
    # --max_pages
    parser.add_argument(
        "--max_pages",
        required=False,
        nargs="?",
        type=int,
        default=20,
        help="Limite de páginas visitadas durante a busca",
    )
    # --output
    parser.add_argument(
        "--output",
        required=False,
        nargs="?",
        type=str,
        default="data/jobs.csv",
        help="Para definir onde o arquivo de output deve ser salvo",
    )
    # --session
    parser.add_argument(
        "--session",
        required=False,
        nargs="?",
        type=str,
        default=".session",
        help="Para definir onde fica a pasta da sessão",
    )

    args = parser.parse_args()

    # find_jobs(args.subject.strip())
    find_jobs(
        args.subject.strip(),
        headless=args.headless,
        max_pages=args.max_pages,
        csv_output=args.output,
        session_folder=args.session,
    )

    # python src/crawler.py "Engenharia de dados" --headless --output="data/eng_de_dados.csv"

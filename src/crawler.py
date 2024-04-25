import os
import argparse
from dotenv import load_dotenv
import pandas as pd

from src.scraping.job_search import JobSearchScraper


load_dotenv()


def find_jobs(
    subject,
    headless=True,
    max_pages=20,
    csv_output="data/jobs.csv",
    session_folder=".session",
):
    email = os.environ["LINKEDIN_EMAIL"]
    password = os.environ["LINKEDIN_PASSWORD"]

    bot = JobSearchScraper(session=session_folder, headless=headless)
    bot.autenticate(email=email, password=password)
    id_dataset = bot.search_job_ids(job_name=subject, max_pages=max_pages)

    # with open("adta/id_dataset.txt", "w", encoding="utf-8") as f:
    #     for _id in id_dataset:
    #         f.write(_id)

    dataset = []
    for _id in id_dataset:
        print(_id)
        try:
            data = bot.retrive_job_data(_id)
            dataset.append(data)
            print("--", data["url"])
        except Exception as e:
            print("--", e)

    df = pd.DataFrame(dataset)
    df.to_csv(csv_output)
    print("CSV salvo!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "subject",
        # required=False,
        help="Termo que deve ser pesquisado",
    )
    parser.add_argument(
        "--headless",
        required=False,
        nargs="?",
        const=True,
        type=bool,
        default=False,
        help="Termo que deve ser pesquisado",
    )
    parser.add_argument(
        "--max_pages",
        required=False,
        nargs="?",
        type=int,
        default=20,
        help="Limite de páginas visitadas durante a busca",
    )
    parser.add_argument(
        "--output",
        required=False,
        nargs="?",
        type=str,
        default="data/jobs.csv",
        help="Para definir onde o arquivo de output deve ser salvo",
    )
    parser.add_argument(
        "--session",
        required=False,
        nargs="?",
        type=str,
        default=".session",
        help="Para definir onde fica a pasta da sessão",
    )

    #     headless=True,
    # max_pages=40,
    # csv_output="data/jobs.csv",
    # session_folder=".session",

    args = parser.parse_args()
    print(args.subject)
    print(args.headless)
    print(args.max_pages)
    print(args.output)
    print(args.session)

    # find_jobs(args.subject.strip())
    find_jobs(
        args.subject.strip(),
        headless=args.headless,
        max_pages=args.max_pages,
        csv_output=args.output,
        session_folder=args.session,
    )

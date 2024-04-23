import os
import re
from bs4 import BeautifulSoup


class JobDataExtractor:
    def __init__(self, url) -> None:
        self.url = url
        self.id = url.split("currentJobId=")[-1].split("&")[0]
        self.folder = f"./data/{self.id}/"
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)

        self.skills = []

    def get_id(self):
        return self.id

    def add_details(self, el_content):
        soup = BeautifulSoup(el_content, "html.parser")

        # Título
        title = soup.find("h1")
        print("Título: ", title.text.strip())

        # Infos
        data = soup.find(
            "div",
            {
                "class": "job-details-jobs-unified-top-card__primary-description-without-tagline"
            },
        )
        # Empresa
        print("Empresa:", data.a.text.strip(), data.a["href"])

        for field in data.find_all("span", {"class": "tvm__text--neutral"}):
            field_text = field.text.strip()
            if re.search(r"há \d+", field_text):
                print("Tempo:", field_text)

            elif re.search(r"\d+ candidat", field_text):
                # print("Candidatos:", re.search(r"\d+", field_text)[0])
                print("Candidatos:", field_text)

            elif len(field_text) > 1:
                # re.findall(r"\d+ candidat", field_text)[0]
                # print(re.findall(r"\d+ candidat", field_text)[0])
                print(field_text)

        data = soup.find(
            "li",
            {"class": "job-details-jobs-unified-top-card__job-insight"},
        )
        tags_span = data.span.find_all("span")

        print("Local:", tags_span[0].text.strip())
        print("Período:", tags_span[1].text.strip())
        print("Senioridade:", tags_span[2].text.strip())

        # hirer-information
        hirer_information = soup.find("div", {"class": "hirer-card__hirer-information"})
        print("Anunciante:", hirer_information.a["href"])

        # jobs_description
        jobs_description = soup.find("div", {"id": "job-details"})
        print(jobs_description.text.strip())

        return "add_details..."

    def add_skills(self, el_content):
        soup = BeautifulSoup(el_content, "html.parser")

        look_for = re.compile(r"^job-details-skill-match-status-list__")
        lis_tag = soup.find_all("li", {"class": look_for})
        for div_tag in lis_tag:
            divs = div_tag.div.find_all("div")
            self.skills.append(divs[1].text.strip())

        return self.skills

    def save(self):
        return "saving..."


if __name__ == "__main__":
    _id = "3900029464"
    extractor = JobDataExtractor(_id)
    filename = extractor.folder + _id

    print("\n------------ detalhes -------------")
    with open(extractor.folder + "/details.html", "r", encoding="utf-8") as f:
        extractor.add_details(f.read())

    print("\n------------- skills --------------")
    with open(extractor.folder + "/skills.html", "r", encoding="utf-8") as f:
        skills = extractor.add_skills(f.read())
    print(skills)
    print()
    # print(el_source)

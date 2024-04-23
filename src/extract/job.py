import os
import re
from bs4 import BeautifulSoup


class JobDataExtractor:
    def __init__(self, url) -> None:
        self.data = {}

        self.url = url
        self.id = url.split("currentJobId=")[-1].split("&")[0]
        # self.folder = f"./data/{self.id}/"
        # if not os.path.isdir(self.folder):
        #     os.makedirs(self.folder)

        self.data["id"] = url.split("currentJobId=")[-1].split("&")[0]
        self.data["url"] = url

    def get_id(self):
        return self.id

    def add_details(self, el_content):
        soup = BeautifulSoup(el_content, "html.parser")

        # Título
        title = soup.find("h1")
        # print("Título: ", title.text.strip())
        self.data["titulo"] = title.text.strip()

        # Empresa
        data = soup.find(
            "div",
            {
                "class": "job-details-jobs-unified-top-card__primary-description-without-tagline"
            },
        )

        primary_description = data.text.strip().split("·")

        try:

            self.data["empresa_nome"] = primary_description[0].strip()
            self.data["localidade"] = primary_description[1].strip()
            self.data["tempo_em_aberto"] = primary_description[2].strip()
            self.data["qtd_candidatos"] = primary_description[3].strip()
        except Exception as e:
            print("\n----------- exception -----------")
            print(e)
            print(primary_description)
            print(self.data["url"])

        try:
            # self.data["empresa_nome"] = data.a.text.strip()
            self.data["empresa_link"] = data.a["href"]
        except:
            ...

        # # características
        # try:
        #     for field in data.find_all("span", {"class": "tvm__text--neutral"}):
        #         field_text = field.text.strip()
        #         if re.search(r"há \d+", field_text):
        #             # print("Tempo:", field_text)
        #             self.data["tempo_em_aberto"] = field_text

        #         elif re.search(r"\d+ candidat", field_text):
        #             # # print("Candidatos:", re.search(r"\d+", field_text)[0])
        #             # print("Candidatos:", field_text)
        #             self.data["qtd_candidatos"] = field_text

        #         elif len(field_text) > 1:
        #             # re.findall(r"\d+ candidat", field_text)[0]
        #             # # print(re.findall(r"\d+ candidat", field_text)[0])
        #             print("Outro:", field_text)
        # except:
        #     ...

        # workplace_type | senioridade
        try:
            data = soup.find(
                "li",
                {"class": "job-details-jobs-unified-top-card__job-insight"},
            )
            tags_span = data.span.find_all("span")

            # # print("Período:", tags_span[1].text.strip())
            # print("Senioridade:", tags_span[-1].text.strip())
            self.data["workplace_type"] = tags_span[0].text.strip()
            self.data["senioridade"] = tags_span[-1].text.strip()
        except:
            ...

        # hirer-information
        try:
            hirer_information = soup.find(
                "div", {"class": "hirer-card__hirer-information"}
            )
            # print("recrutador:", hirer_information.a["href"])
            self.data["recrutador"] = hirer_information.a["href"]
        except:
            print("recrutador: None")

        # jobs_description
        jobs_description = soup.find("div", {"id": "job-details"})
        self.data["jobs_description"] = jobs_description.text.strip()
        # # print(jobs_description.text.strip())

        return "add_details..."

    def add_skills(self, el_content):
        soup = BeautifulSoup(el_content, "html.parser")
        self.data["skills"] = []

        look_for = re.compile(r"^job-details-skill-match-status-list__")
        lis_tag = soup.find_all("li", {"class": look_for})
        for div_tag in lis_tag:
            divs = div_tag.div.find_all("div")
            self.data["skills"].append(divs[1].text.strip())
        # print(self.skills)
        # self.data["skills"] = self.skills
        return "add_details..."

    def save(self):
        # print("\n------------- saving ---------------\n")
        # print(self.data)
        # print("\n-------------- DONE ----------------\n")
        return self.data


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

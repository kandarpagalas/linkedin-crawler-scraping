import re
from bs4 import BeautifulSoup


class JobDataExtractor:
    def __init__(self, url) -> None:
        self.data = {}

        self.url = url
        self.id = url.split("currentJobId=")[-1].split("&")[0]

        self.data["id"] = url.split("currentJobId=")[-1].split("&")[0]
        self.data["url"] = url

    def get_id(self, url):
        return url.split("currentJobId=")[-1].split("&")[0]

    def details(self, page_source):
        details = {}
        soup = BeautifulSoup(page_source, "html.parser")
        # Título
        title = soup.find("h1")
        details["titulo"] = title.text.strip()

        # Empresa
        data1 = soup.find(
            "div",
            {
                "class": "job-details-jobs-unified-top-card__primary-description-without-tagline"
            },
        )
        primary_description = data1.text.strip().split("·")
        try:
            details["empresa_nome"] = primary_description[0].strip()
            details["localidade"] = primary_description[1].strip()
            details["tempo_em_aberto"] = primary_description[2].strip()
            details["qtd_candidatos"] = primary_description[3].strip()
        except Exception as e:
            ...

        try:
            details["empresa_link"] = data1.a["href"]
        except:
            ...

        # workplace_type | senioridade
        try:
            data2 = soup.find(
                "li",
                {"class": "job-details-jobs-unified-top-card__job-insight"},
            )
            tags_span = data2.span.find_all("span")
            details["workplace_type"] = tags_span[0].text.strip()
            details["senioridade"] = tags_span[-1].text.strip()
        except:
            ...

        # hirer-information
        try:
            hirer_information = soup.find(
                "div", {"class": "hirer-card__hirer-information"}
            )
            details["recrutador"] = hirer_information.a["href"]
        except:
            ...

        # jobs_description
        jobs_description = soup.find("div", {"class": "jobs-description-content__text"})
        details["jobs_description"] = jobs_description.div.get_text(" ", strip=True)

        return details

    def skills(self, source):
        skills = []
        soup = BeautifulSoup(source, "html.parser")

        look_for = re.compile(r"^job-details-skill-match-status-list__")
        lis_tag = soup.find_all("li", {"class": look_for})
        for div_tag in lis_tag:
            divs = div_tag.div.find_all("div")
            skills.append(divs[1].text.strip())

        return ";".join(skills)


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

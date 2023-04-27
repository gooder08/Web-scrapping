import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint


def get_city(tag):
    if "Москва" in tag:
        return "Москва"
    if "Санкт-Петербург" in tag:
        return "Санкт-Петербург"


if __name__ == "__main__":
    headers = Headers(browser="firefox", os="win")

    req = requests.get(
        "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2",
        headers=headers.generate(),
    )
    soup = BeautifulSoup(req.text, "lxml")
    tag_vacancies = soup.find_all("div", class_="vacancy-serp-item-body__main-info")

    vac = {}
    n = 0

    for tag_vacancy in tag_vacancies:
        n += 1
        tag_link = tag_vacancy.find("a", class_="serp-item__title")["href"]
        req1 = requests.get(tag_link, headers=headers.generate())
        des_position_soup = BeautifulSoup(req1.text, "lxml")
        tag_zp = des_position_soup.find(
            "span", class_="bloko-header-section-2 bloko-header-section-2_lite"
        )
        tag_city = tag_vacancy.find(
            "div", {"data-qa": "vacancy-serp__vacancy-address"}, class_="bloko-text"
        )
        tag_position = tag_vacancy.find("a", class_="serp-item__title")
        tag_company = tag_vacancy.find(
            "a",
            {"data-qa": "vacancy-serp__vacancy-employer"},
            class_="bloko-link bloko-link_kind-tertiary",
        )
        tag_position_description = des_position_soup.find(
            "div", class_="g-user-content"
        )
        if "Django" and "Flask" in tag_position_description.text:
            vac[f"Vacancy {n}:"] = {
                "Должность:": tag_position.text.replace("\xa0", " "),
                "Компания:": tag_company.text.replace("\xa0", " "),
                "Город:": get_city(tag_city.text),
                "ЗП:": tag_zp.text.replace("\xa0", " "),
                "Ссылка:": tag_link,
            }
        else:
            continue

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(vac, file, indent=2, sort_keys=False, ensure_ascii=False)

    pprint(vac)

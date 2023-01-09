from bs4 import BeautifulSoup


def parser_sciname_page(content):
    soup = BeautifulSoup(content, "html.parser")
    name_soup = soup.find("span", class_="name")
    output = {}
    output["name"] = name_soup.get_text()
    output["genus"] = name_soup.find("i", class_="genus").string
    output["species"] = name_soup.find("i", class_="species").string
    output["authorship"] = name_soup.find("span", class_="authorship").string
    return output

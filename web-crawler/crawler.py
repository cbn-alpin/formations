import requests

from utils import parser_sciname_page


scinames_identifiers = ["tro-26604083", "tro-26616988", "tro-26604085"]

scinames_infos = []
for identifier in scinames_identifiers:
    print(f"Working on {identifier}...")
    url = f"http://www.theplantlist.org/tpl1.1/record/{identifier}"
    page = requests.get(url)
    infos = parser_sciname_page(page.content)
    scinames_infos.append(infos)

headers = scinames_infos[0].keys()
with open("scinames.tsv", "w") as file_handler:
    print("\t".join(headers), file=file_handler)
    for output in scinames_infos:
        print("\t".join(output.values()), file=file_handler)

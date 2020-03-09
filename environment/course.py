from json import load, dump
from re import sub
from string import capwords
from typing import Union

from utils import prefixes, opendata
from utils.progress_bar import ProgressBar


def fetch(output: Union[str, bytes, int]) -> None:
    with open(output, 'w') as writer:
        json_form = opendata.fetch('/course/catalog/filter/*/*/*')
        dump(json_form, writer, indent=4)


def parse(target: Union[str, bytes, int], output: Union[str, bytes, int]) -> None:
    cpc_p, cpc_ns, cpc_link = prefixes.CPC
    rdf_p, rdf_ns, _ = prefixes.RDF
    schema_p, schema_ns, _ = prefixes.SCHEMA
    dbr_p, dbr_ns, _ = prefixes.DBPEDIA_RESOURCE
    xsd_p, xsd_ns, _ = prefixes.XMLSCHEMA

    careers = {
        'UGRD': '<https://www.concordia.ca/academics/undergraduate.html>',
        'GRAD': '<https://www.concordia.ca/academics/graduate.html>',
        'CCCE': '<https://www.concordia.ca/cce.html>',
        'PDEV': '<https://www.concordia.ca/students/gradproskills.html>'
    }

    courses_seen = set()

    with open(output, 'w') as writer:

        writer.write(f'{cpc_p}\n{rdf_p}\n{schema_p}\n{dbr_p}\n{xsd_p}')

        with open(target, 'r') as reader:
            json_form = load(reader)
            progress_bar = ProgressBar(len(json_form))

            for item in json_form:
                progress_bar.console_update()
                if item['ID'] in courses_seen:
                    continue

                courses_seen.add(item['ID'])
                subject = f'<{cpc_link}{item["ID"]}>'
                turtle_form = list()
                turtle_form.append(f'\n\t{rdf_ns}:type {schema_ns}:Course')
                turtle_form.append(f'\n\t{schema_ns}:courseCode \"{item["subject"]}{item["catalog"]}\"')
                turtle_form.append(f'\n\t{schema_ns}:numberOfCredits \"{item["classUnit"]}\"^^{xsd_ns}:float')

                title = sub('["\']', '\'', item['title'])
                title = title.lower()
                title = capwords(title)

                turtle_form.append(f'\n\t{schema_ns}:name \"{title}\"')
                turtle_form.append(f'\n\t{schema_ns}:isPartOf {careers[item["career"]]}')

                if item['prerequisites']:
                    prerequisites = sub('( ){2,}', ' ', item['prerequisites'])
                    prerequisites = sub('[\r\n]+', '', prerequisites)
                    turtle_form.append(f'\n\t{schema_ns}:coursePrerequisites \"{prerequisites}\"')

                turtle_form.append(f'\n\t{schema_ns}:provider {dbr_ns}:Concordia_University')

                properties = ' ;'.join(turtle_form)

                writer.write(f'\n\n{subject}{properties} .')


if __name__ == '__main__':
    target = '../assets/Courses'
    fetch(f'{target}_Raw.json')
    parse(f'{target}_Raw.json', f'{target}.ttl')
